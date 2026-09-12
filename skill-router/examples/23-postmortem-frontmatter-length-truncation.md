---
role: Site Reliability / Principal Skill-Router Maintainer
skill: skill-router
archetype: postmortem
incident: An edit to SKILL.md's description frontmatter pushed it past the platform's character limit, silently truncating the routing bullet so a real trigger phrase stopped matching
---

## 1. Incident Symptom & Alert Payload

```
[User-reported session transcript, 2025-03-22]
User: "can you help me manage my BibTeX file for this paper?"
Assistant: (no skill mentioned; proceeded without invoking academic-papers)

--- platform frontmatter-loader diagnostic, retrieved after the report ---
file: skill-router/SKILL.md
frontmatter_field: description
raw_length_chars: 1142
platform_limit_chars: 1024
loader_behavior: TRUNCATE at limit, no error surfaced to skill author
truncated_content_ends: "...or responding to referee rep"
  (cuts off mid-word; "reports" and everything after, including the
  BibTeX-management clause added earlier that day, never loaded)
```

The frontmatter had been edited that morning to add a clause naming
"managing a BibTeX file" more explicitly - a legitimate, wanted addition -
but the resulting description exceeded the platform's silent 1024-
character truncation limit for that field.

## 2. Immediate Triage & Blast-Radius Mitigation

The router maintainer's first action was to count the exact character
length of the live `description` field (`wc -m` against the frontmatter
block) to confirm the truncation theory rather than guessing at the cause,
since several edits had landed that morning and any one of them could have
been responsible. Once confirmed, the fix was to trim the description back
under the limit immediately - removing lower-priority clarifying phrases
rather than the newly-added BibTeX clause, since re-losing the very trigger
that had just failed would not resolve the report. The trimmed frontmatter
was verified locally (character count and a manual re-read of the loaded
field) before being treated as resolved.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the BibTeX-management request fail to trigger
   `academic-papers`?** Because the exact clause naming "managing a BibTeX
   file" fell after the platform's 1024-character truncation point in the
   `description` frontmatter field, so the loaded, in-memory routing text
   never contained it at all - the router had no way to match against text
   it never received.
2. **Why did the description field exceed the limit in the first place?**
   Because the field accumulates clauses over time as new trigger phrasing
   is added for better routing accuracy, and the morning's edit added a
   new clause without first checking the resulting total length against
   the platform's documented limit - the edit was reviewed for content
   accuracy, not for length.
3. **Why wasn't the length checked before merging that edit?** Because
   `scripts/validate_skill_bundle.py`, this bundle's own automated check,
   validates that required files and README sections exist but has no
   check on frontmatter field length against the platform's actual limit
   - the length constraint exists at the platform layer, not anywhere
   enforced in this repository's own tooling.
4. **Why did the platform silently truncate instead of rejecting the
   oversized field outright?** Because the platform's frontmatter loader
   is designed to always produce a usable (if incomplete) skill definition
   rather than fail closed on a malformed one - a design choice that
   avoids one failure mode (the skill not loading at all) at the cost of
   introducing a much quieter one (the skill loading with silently
   missing content).
5. **Why did nobody notice the truncation between the morning's edit and
   the user's report?** Because there is no automated diff-time or
   post-merge check that reads the field back through the same loading
   path the platform actually uses and compares it against the
   as-authored source - the only way to notice a truncation is to
   manually re-read the *loaded* field character-for-character, which
   nobody did after this specific edit.

Root cause: this repository has no automated check on `description`
frontmatter length against the platform's actual 1024-character limit, so
an otherwise-correct content edit silently exceeded it, and the
platform's fail-open (truncate rather than reject) loading behavior meant
the failure produced no error anywhere - only a real user request landing
on the truncated portion surfaced it.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/skill-router/scripts/validate_skill_bundle.py
+++ b/skill-router/scripts/validate_skill_bundle.py
@@ -40,6 +40,7 @@ REQUIRED_README_SECTIONS = [
     "Helper Scripts",
 ]
+DESCRIPTION_FRONTMATTER_LIMIT = 1024
 
 def check_readme_sections(readme_text):
     problems = []
     for section in REQUIRED_README_SECTIONS:
         if section not in readme_text:
             problems.append(f"README missing required section: {section!r}")
     return problems
+
+
+def check_description_length(skill_md_text):
+    description = extract_frontmatter_field(skill_md_text, "description")
+    if len(description) > DESCRIPTION_FRONTMATTER_LIMIT:
+        return [
+            f"description frontmatter is {len(description)} chars, "
+            f"exceeds the platform's {DESCRIPTION_FRONTMATTER_LIMIT}-char "
+            f"limit and will be silently truncated at load time"
+        ]
+    return []
```

```diff
--- a/skill-router/SKILL.md
+++ b/skill-router/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: skill-router
-description: Use at the start of any non-trivial task to silently check whether one of the user's domain skills (academic-papers, agile-development, deep-learning, hep-analysis) applies before proceeding. Consult this for any non-trivial software change (implement/fix/add/refactor/migrate/update, scoping, code review), PyTorch model/training/DataLoader/debugging tasks (architecture selection, parallelism, compute budgeting, ablation, data/evaluation strategy), HEP/CERN/ROOT/PyROOT/RDataFrame/uproot/cutflow/systematics/fit/limit tasks (detector subsystems, event reconstruction, Geant4 simulation), or reading/critiquing a paper, building a literature review, drafting a manuscript, managing a BibTeX file, or responding to referee reports and rebuttals in full detail
+description: Use at the start of any non-trivial task to silently check whether one of the user's domain skills (academic-papers, agile-development, deep-learning, hep-analysis) applies before proceeding. Consult this for any non-trivial software change, PyTorch/ML tasks, HEP/ROOT/RDataFrame/uproot tasks, or reading/writing a paper, managing a BibTeX file, or responding to referee reports
 ---
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the edit that pushed the field over the limit
was a genuine improvement to routing accuracy, reviewed for correctness
by someone with no way to know the platform's exact character limit or
that it fails open by truncating rather than rejecting.

**What worked:** counting the exact loaded character length as the first
diagnostic step, rather than guessing which recent edit was responsible,
identified the cause within minutes instead of requiring a bisection
across the morning's several unrelated edits.

**What didn't work:** because the platform truncates silently instead of
rejecting an oversized field, the failure produced no error, no log entry,
and no visible symptom anywhere until a real user's request happened to
depend on exactly the truncated portion - the gap could have persisted
indefinitely otherwise.

**Preventative monitoring rule:** `scripts/validate_skill_bundle.py` now
blocks (non-zero exit) any commit where the `description` frontmatter
field exceeds 100% of the platform's 1024-character budget, run as a
required pre-merge check on every `SKILL.md` change rather than relying on
a length limit that exists only in undocumented platform behavior.
