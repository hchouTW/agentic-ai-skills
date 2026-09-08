# Code Style, Naming, and File Documentation

Match the repository's existing conventions first wherever this analysis code lives.
Use the following as a default when no repository convention exists.

## Naming

- **C++ / ROOT macros**: Google C++ style — `snake_case` variables/params,
  `PascalCase` types/functions, `kPascalCase` static constants,
  `trailing_underscore_` members, `ALL_CAPS` only for macros. Descriptive physics
  names: `event_weight`, `signal_yield`, `mass_window`, `fit_range`, `mass_hist`,
  `fit_result`. Standard HEP abbreviations (`pt`, `eta`, `phi`, `met`, `pu`, `sf`,
  `mc`) are fine.
- **Python**: Google/PEP 8 — `snake_case` functions/vars, `PascalCase` classes,
  `UPPER_SNAKE_CASE` constants, `_leading_underscore` for private helpers.
- For C++ design choices beyond naming (class vs. struct vs. free function,
  ownership, RAII, composition vs. inheritance), see
  [C++ design guidelines](19-cpp-balanced-design-guidelines.md).

## Comments

Reserve comments for non-obvious logic: physics/statistical assumptions,
weight/normalization choices, fit models and ranges, ROOT object ownership/lifetime,
and edge cases. Do not comment `// open file` or `// loop over events` — the code
already says that.

## File-level documentation requirement

When creating or modifying any code file (C++ source/headers, ROOT macros, PyROOT/
uproot scripts, CMake files, config loaders), include a short introductory comment
block at the top of the file (`//` or `/* */` for C++/ROOT macros, `#` for
Python/CMake, a module docstring `"""..."""` for Python scripts) covering:

- **Purpose** — why the file exists, e.g. "dimuon selection + mass histogram" or "JES
  systematics check".
- **What the code does** — the main behavior: selections, histograms produced, fit
  model, or inspection performed.
- **Usage notes, dependencies, or assumptions** — build/run command, expected input
  format and tree/branch names, units, weight conventions, ROOT version, and any
  preconditions.

For existing files, add the explanation if it is missing, or update it if it is
incomplete or outdated. Keep it proportional to the file and do not let it drift from
the code — this complements the inline-comment guidance above, it does not replace it.

## Review checklist

Inputs/trees validated; branch names validated/documented; units explicit; selections
named and traceable; weights applied exactly once; data/MC paths separate where
needed; histograms have names and axis labels; empty histograms handled safely; fit
status/covariance checked; output files closed cleanly; scripts runnable from the
command line; build/run commands documented; tests/validation run or their absence
stated with a reason.
