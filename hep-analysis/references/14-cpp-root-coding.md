# C++, ROOT, and RDataFrame Coding Patterns

Use this reference for concrete C++/ROOT code, not for the statistical treatment of
pipelines (see [Data pipelines](02-data-pipelines.md) for I/O, ownership, and
performance concerns at the design level).

## Choosing an event-loop API

- `ROOT::RDataFrame`: default for new columnar event processing. Declarative filters
  and defines, multithreading, snapshots, and cutflow reports.
- `TTreeReader`: use when manual event-loop control is required, branch structures are
  awkward for RDataFrame, the code integrates into existing manual-loop code, or
  step-by-step debugging of event iteration is needed.
- `SetBranchAddress`: legacy maintenance only. Validate addresses and object lifetimes
  carefully; a dangling or reused address is a common source of silently wrong values.

```cpp
TTreeReader reader(tree);
TTreeReaderValue<float> pt(reader, "pt");

while (reader.Next()) {
    if (*pt > 25.0f) {
        // fill objects
    }
}
```

## RDataFrame patterns

Basic filter and histogram:

```cpp
ROOT::RDataFrame df("Events", "input.root");

auto selected = df.Filter("pt > 25.0", "pt selection");
auto h = selected.Histo1D(
    {"h_pt", "p_{T};p_{T} [GeV];Events", 50, 0.0, 200.0},
    "pt"
);
```

Multiple input files:

```cpp
std::vector<std::string> files = {"a.root", "b.root"};
ROOT::RDataFrame df("Events", files);
```

Named cutflow, booked before materialization:

```cpp
auto df1 = df.Filter("nMuon >= 2", "at least two muons");
auto df2 = df1.Filter("Muon_pt[0] > 25.0", "leading muon pt");
auto report = df2.Report();  // book everything before .GetValue()/.Print()
report->Print();
```

Weighted histogram:

```cpp
auto dfw = df.Define("weight", "genWeight * pileupWeight");
auto h = dfw.Histo1D(
    {"h_mass", "Mass;m [GeV];Weighted events", 60, 60.0, 120.0},
    "mass",
    "weight"
);
```

Reusable helper functions operate on `ROOT::RDF::RNode`:

```cpp
ROOT::RDF::RNode add_columns(ROOT::RDF::RNode df) {
    return df.Define("abs_eta", "std::abs(eta)");
}
```

Lazy execution: book every action, then trigger by accessing results once, in one
place, to avoid duplicating the event scan:

```cpp
auto n = df.Count();
auto h = df.Histo1D({"h", "x;x;Events", 50, 0, 1}, "x");

std::cout << "Events: " << *n << "\n";
h->Write();
```

## Input and object safety

Validate every file, tree, and branch before building a large workflow, and fail with
a message naming the file/object that failed rather than producing silent empty
output:

```cpp
auto file = std::unique_ptr<TFile>(TFile::Open(path.c_str(), "READ"));
if (!file || file->IsZombie()) {
    throw std::runtime_error("Could not open file: " + path);
}
auto* tree = file->Get<TTree>(treeName.c_str());
if (!tree) {
    throw std::runtime_error("Missing tree: " + treeName);
}
if (!tree->GetBranch("pt")) {
    throw std::runtime_error("Missing branch pt");
}
```

## Histogram construction

```cpp
TH1D h("h_muon_pt", "Muon p_{T};p_{T} [GeV];Events", 50, 0.0, 200.0);
h.Sumw2();  // before filling manually with weights
```

Use explicit axis titles and units; check entries and integrals before scaling,
dividing, or fitting; state the underflow/overflow policy when reporting integrals.
See [Histograms and uncertainties](04-histograms-efficiencies.md) for the statistical
treatment of sumw/sumw2 and covariance.

## Plotting

```cpp
gROOT->SetBatch(kTRUE);  // required for non-interactive/batch plotting jobs

TCanvas c("c", "c", 800, 600);
h.Draw("HIST");
c.SaveAs("plot.pdf");
```

Include luminosity, sqrt(s), and region/channel labels; use ratio panels for data/MC;
mask blinded data in both the main panel and any ratio (see
[Analysis design](01-analysis-design.md) for blinding rules and
[Histograms and uncertainties](04-histograms-efficiencies.md) for ratio/pull
statistics).

## Style

- Default to C++17. Prefer RAII and standard-library containers; prefer `std::string`
  over `TString` unless a ROOT API specifically requires ROOT string behavior.
- Naming: Google C++ style — `snake_case` variables/params, `PascalCase`
  types/functions, `kPascalCase` static constants, `trailing_underscore_` members,
  `ALL_CAPS` only for macros. Standard HEP abbreviations (`pt`, `eta`, `phi`, `met`,
  `pu`, `sf`, `mc`) are fine. See [Code conventions](18-code-conventions.md) for the
  full naming and documentation convention, and
  [C++ design guidelines](19-cpp-balanced-design-guidelines.md) for class/struct/
  ownership choices beyond ROOT-specific idioms.
- Use meaningful, descriptive physics names (`event_weight`, `signal_yield`,
  `mass_window`, `fit_range`) for histograms, canvases, and functions.

## Build

Single-file program:

```bash
c++ -std=c++17 -O2 -Wall -Wextra analysis.cpp $(root-config --cflags --libs) -o analysis
```

Compiled macro:

```bash
root -l -q 'analysis.C+("input.root")'
```

For CMake-based projects, see [Build setup](15-cmake-and-build.md).

## Review checklist

- Cuts, weights, binning, labels, and object definitions are preserved.
- Data and simulation branches are handled separately where needed.
- ROOT object ownership and file lifetimes are explicit.
- Batch mode is enabled for non-interactive plotting jobs.
- A cutflow or equivalent event-count validation exists.
- All RDataFrame actions are booked before `.GetValue()`/`.Report()`/writing output.
