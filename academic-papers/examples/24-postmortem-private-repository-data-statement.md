---
role: Site Reliability / Principal Research Scientist
skill: academic-papers
archetype: postmortem
incident: A posted preprint's data-availability statement pointed to a code/data repository that was still private, blocking reviewers and readers for days
---

## 1. Incident Symptom & Alert Payload

Automated bounce notification from the preprint server's link-checker,
plus a reviewer complaint forwarded by the editor:

```
[LINK-CHECK FAILED] arXiv:2501.xxxxx
checked_url: https://github.com/collab-name/analysis-release
http_status: 404
checked_at: 2025-01-14T03:00:00Z
note: repository not found or not publicly accessible

--- forwarded reviewer message, 2025-01-15 ---
"The data-availability statement (Sec. 8) points to
github.com/collab-name/analysis-release for the reduction code, but the
link returns a 404. I cannot assess the reproducibility claim in Sec. 8
without it. Please advise."
```

The repository existed but was still set to private on GitHub - the
public URL had been written into the manuscript before the release step
that makes it public was actually completed.

## 2. Immediate Triage & Blast-Radius Mitigation

The corresponding author checked the repository's visibility setting
directly and confirmed it was private, not deleted or moved - the fastest
safe mitigation was to flip visibility to public immediately, which took
effect within minutes and required no manuscript changes. Per
`references/artifact-packaging-for-release.md`'s "verify against a clean
checkout" step, the author then opened the now-public URL in a logged-out
browser session to confirm an outside reader could actually reach it (not
just that the toggle had been flipped), and replied to both the reviewer
and the editor confirming the link was live, closing the window during
which the repository was unreachable at just under 36 hours from the first
bounce notification.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the reviewer get a 404 on the data-availability link?**
   Because the GitHub repository the URL points to was still set to
   private visibility when the preprint was posted.
2. **Why was the repository still private at posting time?** Because
   "make the repository public" was the last step in the release
   checklist (`references/artifact-packaging-for-release.md`'s ordered
   steps: scope, reproduce, pin environment, write README, then license
   and publish), and the corresponding author posted the preprint before
   completing that last checklist step, believing the repository was
   "basically ready" and treating the visibility toggle as a formality
   rather than a required, trackable step.
3. **Why was the manuscript's data-availability statement already
   pointing at the final public URL before the repository was actually
   public?** Because the URL is stable across the private-to-public
   transition (GitHub repository URLs don't change when visibility
   changes), so writing the URL into the manuscript early "to save a
   later edit" created no local error - the mismatch only became visible
   to someone outside the collaboration, who has no way to check
   visibility before clicking the link.
4. **Why did no internal check catch the mismatch before the preprint
   was posted?** Because the pre-posting checklist for this collaboration
   checks that the manuscript's citation and formatting are complete, but
   has no step that verifies each externally-facing URL in the manuscript
   (data-availability statement, code links) actually resolves for a
   logged-out, non-collaboration reader.
5. **Why does the checklist not include an external-reachability check for
   these links?** Because the checklist was written when the collaboration
   only ever released data/code well after posting, with the availability
   statement added retroactively in a later revision - the workflow of
   writing the final URL into the manuscript *before* the release step
   completes is newer than the checklist and was never incorporated into
   it.

Root cause: the release-readiness checklist verifies manuscript content
but not the live reachability of externally-facing links the manuscript
promises, and the release step that makes a repository public is treated
as an informal formality rather than a tracked, verified checklist item
completed before posting.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/tools/pre_post_check.sh
+++ b/tools/pre_post_check.sh
@@ -1,5 +1,17 @@
 #!/bin/sh
 set -e
+
+# Verify every externally-facing URL in the data-availability statement
+# actually resolves for a logged-out reader before the preprint is posted
+# (see postmortem: private-repository data statement).
+URLS=$(grep -oE 'https://[^ }]+' sections/data_availability.tex)
+for url in $URLS; do
+  status=$(curl -s -o /dev/null -w "%{http_code}" -H "Cache-Control: no-cache" "$url")
+  if [ "$status" != "200" ]; then
+    echo "ERROR: $url returned HTTP $status (must be 200 for a logged-out" \
+         "reader) - do not post until the repository is public." >&2
+    exit 1
+  fi
+done
 
 latex_build.sh paper.tex
```

```diff
--- a/docs/release-checklist.md
+++ b/docs/release-checklist.md
@@ -3,4 +3,7 @@
 - [ ] README documents install, reproduction command, and exclusions
 - [ ] License attached to code and data
 - [ ] Repository visibility set to public
-- [ ] Manuscript's data-availability statement matches the final URL
+- [ ] Manuscript's data-availability statement matches the final URL
+- [ ] `tools/pre_post_check.sh` run and passing (confirms every URL in the
+      data-availability statement returns HTTP 200 for a logged-out
+      reader) - required before the preprint is posted, not after
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: treating "make the repository public" as the
final, low-risk step of a long checklist is a reasonable simplification
under normal conditions - it only fails when the manuscript's URL is
written in before that step is confirmed complete, which nothing flagged
as risky at the time.

**What worked:** the fix itself was nearly instantaneous once diagnosed -
flipping a visibility toggle - and verifying with a logged-out session
before declaring the incident closed caught the difference between "the
author believes it's public" and "an outside reader can actually reach
it."

**What didn't work:** the collaboration's release checklist checked
manuscript content and had no step that ever made an outbound request to
confirm a promised link actually resolves, so a private repository and a
public one looked identical from inside the manuscript-review process.

**Preventative monitoring rule:** `tools/pre_post_check.sh` blocks
(non-zero exit) posting any preprint where more than 0% of the URLs in the
data-availability statement fail to return HTTP 200 for a logged-out
request, run as a required pre-posting gate rather than an optional
convenience script.
