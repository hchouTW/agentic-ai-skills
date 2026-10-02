

## Addendum 3 (2026-10-02): cosmic-ray databases, sources S50-S53 and claims C125-C130

Two compiled-data resources were added as Tier 6 sources: CRDB at LPSC (S50 website, S51 its four papers) and the ASI SSDC Cosmic Ray Database (S52 its page, **not verified**; S53 a 2017 proceedings). Please check: (a) is Tier 6 and `third_party_context` the right class for a database's statements about itself, (b) are the CRDB-conversion and combination statements (C127) worded narrowly enough, (c) is it right to keep S52 empty of any content claim.

| ID | Src | Scope | Strength | Support | Num | Claim | Verdict |
|---|---|---|---|---|---|---|---|
| C125 | S50 | CRDB scope, interfaces and size on 2026-10-02 | page | third_party_context | yes | CRDB (LPSC) scope and size: it compiles cosmic-ray data and meta-data from 10^6 to 10^21 eV, namely leptons (e-, e+, e- + e+, e+/(e- + e+) and e+/e-), nuclei (fluxes and… |  |
| C126 | S50 | CRDB data-preparation and query conventions | page | third_party_context | yes | CRDB data-preparation conventions (Caveats/Tips page): if the publication gives only a mean energy, E_BIN_L = E_BIN_U = E_MEAN; if it gives bin edges only, E_MEAN is the… |  |
| C127 | S50 | CRDB combination, conversion and unit rules | page | third_party_context | yes | CRDB combinations, energy conversions and units (Caveats/Tips page): native data are stored as published and combined data (ratios or products of native data of the same… |  |
| C128 | S50 | CRDB REST and Python access | page | third_party_context | yes | CRDB REST interface and Python library (REST/CRDB.py page): the Python library is installed with 'pip install crdb', returns structured Numpy arrays from keyword queries… |  |
| C129 | S51 | CRDB versions and growth, 2014-2026 | abstract+metadata | third_party_context | yes | History and growth of CRDB as stated in the abstracts of its papers: the 2014 paper (Maurin, Melot, Taillet, A&A 569, A32, arXiv:1302.5525) describes a new online databa… |  |
| C130 | S53 | ASI SSDC Cosmic Ray Database as described in 2017 | abstract+metadata | third_party_context | yes | The ASI Cosmic Ray Database (proceedings S53, abstract): a cosmic-ray database was under development at the ASI Space Science Data Center (a multi-mission science operat… |  |
