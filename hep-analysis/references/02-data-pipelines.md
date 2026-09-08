# Data Pipelines, ROOT, and Columnar Processing

## Select an appropriate interface

Follow the existing project. RDataFrame suits new ROOT-native pipelines; uproot/awkward suits Python jagged-array processing; TTreeReader may remain appropriate for existing manual loops. Do not rewrite a RooFit model merely to standardize style. Inspect installed versions and the actual schema rather than assuming another NanoAOD production's branch names.

## Audit inputs

For every file, check successful opening, required trees/objects, entries, branches, types, and jagged-array structure. Do not silently skip failed remote files and report a complete sample. Bound retries and record failed files in the manifest. Run a small schema smoke test before reading the full production, and request only required branches.

Use chunked reads such as `uproot.iterate(..., expressions=..., step_size="100 MB", library="ak")` where appropriate. Merge sumw, sumw2, and cutflows across chunks and verify that changing chunk size preserves results. See the [official uproot guide](https://uproot.readthedocs.io/en/latest/basic.html).

Check multiplicities before indexing `[:, 0]`. Object masks and event masks act on different axes. Object-level histograms require deliberate broadcasting of event weights and treatment of correlations from multiple objects in one event. Define behavior for empty lists, missing values, NaNs, and insufficient multiplicity.

```python
# Adaptation pattern: requires awkward; Muon_pt is in GeV and weight is defined.
import awkward as ak
has_muon = ak.num(arrays["Muon_pt"], axis=1) > 0
muons = arrays["Muon_pt"][has_muon]
weights = arrays["weight"][has_muon]
leading_pt = muons[:, 0]  # Leading only if the schema guarantees pT ordering.
```

## RDataFrame and C++

Book related actions before triggering evaluation or writing results to reduce repeated event scans. Name filters. Count/Report are unweighted; compute sums of weight and weight squared at each selection node for a weighted cutflow. Filter empty collections or define an explicit alternative before accessing their first elements.

Manage ROOT ownership explicitly. Histograms that must outlive an input TFile need appropriate cloning/detachment and ownership. Check zombie files, null pointers, branch types, and dictionary warnings. Multithreaded helpers must not share mutable event state. Derive smearing seeds from stable event identifiers and source labels rather than scheduling order.

Avoid SetBranchAddress bindings to expired local storage. Snapshot branch selection, output tree names, and compression form part of the output contract. If event order changes, compare by stable event keys rather than row index.

## Performance and preservation

Measure I/O, decompression, selection, correction lookup, and histogramming separately before optimizing. Bound memory per worker and avoid oversubscription from Python workers multiplied by ROOT threads. Distributed merges must compare expected and processed files/counts and prevent duplicate outputs from retries.

Preserve input manifests, commits and uncommitted diffs, configuration checksums, software versions, calibration payload checksums, seed strategies, commands, and failed-file lists. Do not include authentication tokens or credentials in manifests.
