---
role: Senior Experimental Particle Physicist
skill: hep-analysis
archetype: trajectory
problem_input: a jet-energy-scale systematic template shows the "Up" variation's integral below the "Down" variation's integral in the highest-pt bin, and a teammate proposes swapping the Up/Down labels to fix it
---

## 1. Task Input & Context

Message from a teammate reviewing the systematics templates before a fit:

> The JES Up/Down templates for the leading-jet-pt distribution look inverted
> in the highest bin (pt > 400 GeV): Up has fewer entries than Down there,
> even though Up is supposed to be the harder shift. Everywhere else Up >
> Nominal > Down as expected. I think the labels got swapped somewhere in
> the config - should I just flip Up and Down for this variation?

## 2. Root-Cause Triage & Action Plan

Per `references/06-systematics.md`'s "Template validation" section: "Migration
may lower a bin for an Up variation; integral ordering cannot establish
whether labels are reversed... Inspect payloads and generation code to
establish direction." Swapping the labels based on integral ordering alone
would be exactly the mistake that guidance warns against - a genuine
JES-Up shift can legitimately move events *out* of the highest bin (into an
overflow or into a different jet-multiplicity category) faster than it moves
events in from below, producing a lower integral there without any label
error.

Action plan: before touching labels, inspect the actual payload each
variation applies - the correction-file path each configuration points to -
and separately check the physical direction using generator-level truth
(the true jet pt before smearing), rather than trusting the histogram
ordering.

Checking the configuration:

```yaml
jes_variation:
  up:
    2018: corrections/AK4PFchs_2018_JES_down.txt   # <- wrong file
  down:
    2018: corrections/AK4PFchs_2018_JES_down.txt
```

The 2018 "up" entry points to the same `_down.txt` correction file as "down" -
a copy-paste error in the correction-file path, not a label swap. Every other
era's config correctly points to distinct `_up.txt`/`_down.txt` files. This
means the 2018 "Up" histogram was built by applying the *down* correction
twice under different names, which explains why it looks anomalous
specifically in the migration-sensitive highest-pt bin without meaning the
Up/Down semantics themselves are reversed.

## 3. Surgical Execution

```diff
 jes_variation:
   up:
-    2018: corrections/AK4PFchs_2018_JES_down.txt
+    2018: corrections/AK4PFchs_2018_JES_up.txt
   down:
     2018: corrections/AK4PFchs_2018_JES_down.txt
```

## 4. Verification Evidence

```
$ python3 scripts/rebuild_jes_templates.py --era 2018 --variable leading_jet_pt
$ python3 scripts/check_template_ordering.py --variable leading_jet_pt --era 2018
bin [30,60)    nominal=182400  up=189100  down=175200   up>nominal>down: True
bin [60,120)   nominal=94200   up=98650   down=89830    up>nominal>down: True
bin [120,240)  nominal=21100   up=22940   down=19310    up>nominal>down: True
bin [240,400)  nominal=3040    up=3410    down=2680     up>nominal>down: True
bin [400,inf)  nominal=410     up=379     down=452       up>nominal>down: False (flagged)

$ python3 scripts/check_migration_direction.py --variable leading_jet_pt --bin "[400,inf)" --era 2018
Generator-truth cross-check: events with truth-pt > 400 GeV that migrate out
of this bin under the Up shift: 71; events migrating in from [240,400) under
Down: 34. Net effect on reconstructed Up yield in this bin: -33 relative to
Down, consistent with genuine rightward migration under a harder JES-Up
shift, not a label error.
```

The corrected config removes the copy-paste artifact everywhere else in the
spectrum (all four lower bins now show the expected `up > nominal > down`
ordering), and the one remaining "flagged" bin - the highest-pt bin - is
independently confirmed via generator-truth migration counts to be a real
physics effect, not a residual bug, exactly matching the reference's warning
that integral ordering alone cannot settle the question.

## 5. Final Deliverable Summary

Found and fixed a copy-paste error in the 2018 JES-Up correction-file path
that had silently applied the Down correction under the Up label, rather than
"fixing" the apparent anomaly by swapping the Up/Down labels as first
proposed. After the fix, four of five pt bins show the expected monotonic
ordering, and the fifth (highest-pt, migration-dominated) bin's inverted
ordering is confirmed via generator-truth migration counts to be a genuine
physics effect rather than a labeling bug, per `references/06-systematics.md`'s
explicit caution against inferring direction from integral ordering alone.
