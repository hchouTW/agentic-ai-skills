---
role: Principal Platform / Developer-Experience Engineer
skill: skill-router
archetype: gated-pipeline
high_stakes_task: adding a new devops-infrastructure routing rule to SKILL.md without creating a keyword collision with an existing rule
---

## Phase 1: Input Extraction & Gap Formulation

The collection is adding a fifth domain skill, `devops-infrastructure`
(Terraform, Kubernetes manifests, CI/CD pipeline configuration, Docker), and
it needs a routing-rule bullet in `SKILL.md`. Extracted candidate trigger
vocabulary from the new skill's own scope: "Terraform", "Kubernetes",
"Docker", "CI/CD", "infrastructure as code", "pipeline".

Note first that `scripts/validate_skill_bundle.py` has no automated keyword-
collision checker of its own - `ROUTING_ENTRY_RE` only extracts each rule's
bolded skill name to confirm it parses and has an installed sibling folder,
it does not compare rule *bodies* against each other. Any collision check
here is a manual grep against the five existing bullets' actual text, not a
built-in gate.

**Gate:** proceed to Phase 2 only once every candidate trigger word above has
been grepped, individually and case-insensitively, against the full current
text of `SKILL.md`, and each result (match or no match) is recorded - not
just asserted clean from memory.

## Phase 2: Draft Synthesis

Ran the collision check named in Phase 1's gate:

```
$ for kw in Terraform Kubernetes Docker "CI/CD" "infrastructure as code" pipeline; do
    echo "=== $kw ==="; grep -n -i "$kw" SKILL.md
  done
=== Terraform ===
=== Kubernetes ===
=== Docker ===
=== CI/CD ===
=== infrastructure as code ===
=== pipeline ===
36:  Expert comparison plus key takeaways), Execution Trajectory, Gated Pipeline,
46:  (DDP vs. ZeRO/FSDP vs. tensor/pipeline/sequence), compute and cost
52:  C++, PyROOT, RDataFrame, uproot/awkward columnar pipelines, ntuples, event
```

Four of six candidates are clean. "pipeline" hits three lines: line 36 is
this document's own archetype name ("Gated Pipeline") - not a routing
collision, since it's this file's meta-vocabulary about example shapes, not
a rule about triggering a skill - but lines 46 and 52 are real: `deep-
learning`'s own bullet already uses "pipeline" for parallelism strategy
(`tensor/pipeline/sequence`), and `hep-analysis`'s already uses it for
columnar data pipelines. "Pipeline" alone is genuinely overloaded across
this collection and cannot be claimed as a distinguishing keyword by itself.
Drafted a first bullet that names the ambiguity explicitly instead of
pretending the word is free to claim outright:

```
- **devops-infrastructure** - CI/CD pipeline configuration, Docker/Kubernetes
  manifests, and Terraform/infrastructure-as-code definitions. Covers
  designing and reviewing deployment pipelines, container build steps, and
  cluster configuration. "Pipeline" alone is ambiguous in this collection -
  not for a PyTorch pipeline-parallelism strategy (see `deep-learning`) or a
  HEP columnar-data pipeline (see `hep-analysis`); look for CI/CD, Docker,
  Kubernetes, or Terraform language specifically.
```

**Gate:** proceed to Phase 3 only once every non-clean hit from Phase 1's
grep has either zero remaining collision or an explicit carve-out naming the
colliding rule(s) by name - "pipeline" now has one; nothing else did.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption behind Phase 2's gate: "checking the original
candidate keyword list is enough - the draft itself introduces no new
collision." Re-grepped the *drafted bullet's own full text* (not the
original six-word candidate list) against `SKILL.md`, since the draft's own
prose ("container build steps") is new text that was never checked:

```
$ grep -n -i "build" SKILL.md /tmp/draft_v1.txt
/tmp/draft_v1.txt:3:  designing and reviewing deployment pipelines, container build steps, and
SKILL.md:55:  Combine, CMake/root-config builds, and HEP plotting. Also the detector and
```

A real, previously-unchecked collision: `hep-analysis`'s existing bullet
already says "CMake/root-config builds," and the draft's own "container
build steps" phrase was never run against the other three rules, only the
original candidate list was. This is exactly the assumption that needed
stress-testing - a fixed candidate-keyword list, checked once at the start,
misses collisions introduced by the draft's *own* explanatory prose written
in Phase 2. Fixed by adding a second carve-out to the bullet, matching the
convention of the first:

```
- **devops-infrastructure** - CI/CD pipeline configuration, Docker/Kubernetes
  manifests, and Terraform/infrastructure-as-code definitions. Covers
  designing and reviewing deployment pipelines, container build steps, and
  cluster configuration. "Pipeline" alone is ambiguous in this collection -
  not for a PyTorch pipeline-parallelism strategy (see `deep-learning`) or a
  HEP columnar-data pipeline (see `hep-analysis`); look for CI/CD, Docker,
  Kubernetes, or Terraform language specifically. Also not for a HEP
  analysis's own CMake/ROOT build system - see `hep-analysis` for that.
```

Also confirmed `extract_routed_skill_names()` in
`scripts/validate_skill_bundle.py` actually parses this final bullet
correctly, rather than assuming its `- **name**` regex handles a multi-word
hyphenated skill name:

```
$ python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('vsb', 'scripts/validate_skill_bundle.py')
vsb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vsb)
draft = open('SKILL.md').read() + '''
- **devops-infrastructure** - CI/CD pipeline configuration, Docker/Kubernetes
  manifests, and Terraform/infrastructure-as-code definitions.
'''
print(vsb.extract_routed_skill_names(draft))
"
['academic-papers', 'agile-development', 'deep-learning', 'hep-analysis', 'devops-infrastructure']
```

**Gate:** merge only once the drafted bullet's own full text (not just the
original candidate keywords) has been re-grepped against all five existing
bullets with every hit either clean or explicitly carved out, and
`extract_routed_skill_names()` is confirmed - by actually running it, as
above, not assumed - to parse the new bullet and yield the new skill name.
This is the actual merge criterion, not an intermediate one.
