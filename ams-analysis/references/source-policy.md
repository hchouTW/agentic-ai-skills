# Source Policy and Evidence Rules

## When to read this file

Read when quoting any AMS result or performance value, when a question contains "latest", "current", "has AMS published", "is this paper real", or when interpreting a result. Canonical home for source tiers, the evidence-ledger schema, currency checks, conflict resolution, citation placement, and unsupported-claim behavior. The populated ledger is [source-index](source-index.md).

## Contents

1. [Source tiers](#source-tiers)
2. [Evidence ledger schema](#evidence-ledger-schema)
3. [Source-review procedure](#source-review-procedure)
4. [Currency checks ("latest")](#currency-checks-latest)
5. [Conflicts between sources](#conflicts-between-sources)
6. [Citation placement](#citation-placement)
7. [Result interpretation](#result-interpretation)
8. [Unsupported-claim behavior](#unsupported-claim-behavior)
9. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Source tiers

| Tier | Class | Use |
|---|---|---|
| 1 | Peer-reviewed AMS Collaboration papers and supplements | AMS results, methods, performance in that analysis |
| 2 | Official AMS detector papers, website, technical documents, formal data releases | Detector description, geometry, mechanism |
| 3 | Public conference material or theses by AMS authors | Labeled "less formal or potentially outdated"; **preliminary** unless a paper says otherwise |
| 4 | PDG, authoritative textbooks, peer-reviewed methodology papers | General principles (kinematics, statistics, unfolding) |
| 5 | Other experiments | Methodological comparison only; never AMS practice |
| 6 | Reviews, press, slides, secondary articles, encyclopedias | Navigation only; secondary-only evidence must be labeled |

## Evidence ledger schema

Every quantitative claim entering an answer or this skill needs a ledger row:

```yaml
claim_id: null
claim: null
claim_type: detector_fact | performance_number | analysis_method | published_result | general_method
source_title: null
collaboration_or_author: null
publication_date: null
doi_or_url: null
source_tier: 1
location_in_source: section/page/figure/table
supported_scope: null      # species, energy/rigidity range, selection, period, CL, detector configuration
known_limitations: null
last_verified: YYYY-MM-DD
```

A number without its context (species, range, selection, period, CL, configuration) must not be quoted. `source-index` records the verification level actually achieved: `full-text`, `abstract+metadata`, `metadata-only`, or `not-opened`; a claim's strength never exceeds it.

## Source-review procedure

1. Open the primary document; do not rely on search snippets or citation aggregators.
2. Separate **publication date** from the **data-taking interval**.
3. Check errata, supplementary material, and later superseding publications.
4. Record whether a conference claim is preliminary.
5. When several AMS results coexist (e.g. different rigidity ranges, periods, track configurations), explain which question each answers rather than retaining only the newest number.
6. Paraphrase; do not copy long copyrighted passages.

## Currency checks ("latest")

Triggers: "latest", "most recent", "current", "has AMS published", "as of", any result or hardware-status claim that may have changed after the skill's last verification (**2026-09-20**).

Procedure: (1) search INSPIRE-HEP with the collaboration filter and date sort (metadata, not a snippet); (2) open the AMS results page and the journal record; (3) report publication date, data period, formal status (peer-reviewed / preprint / conference); (4) check for supplements and superseding papers; (5) state the verification date. If browsing is unavailable: state the verification limitation and the skill's last-verified date; do not claim currency; give the last known result with its date as "as of the last check".

## Conflicts between sources

Prefer the newer primary analysis, and explain the difference in definition, period, selection, or calibration (e.g. rigidity vs energy binning, track configuration, data-taking period, reconstruction version). A conflict between Tier 1 and Tier 3/6 resolves to Tier 1; a Tier 1 conflict with another Tier 1 is explained, not averaged.

## Citation placement

Put the citation next to the claim (S-number from [source-index](source-index.md), plus paper and year), not at the end of the answer. General methods carry Tier 4 references; proposals are labeled as proposals and not cited as AMS practice. Formatting alone earns nothing: the cited source must support the specific claim.

## Result interpretation

Separate: **direct measurement** (flux, ratio, fraction and their uncertainties) from **model interpretation** (dark matter, pulsar, propagation, source-term fits). State what the measurement excludes and what it does not. Reject unsupported extrapolation beyond the measured rigidity/energy range, period, and species. A fit of a functional form in a paper is a description, not a proof of mechanism. Agreement between measurements is consistency, not proof.

## Unsupported-claim behavior

- **Fabricated or unverifiable citation:** say it could not be verified; report what a search found (or that nothing matched); do not confirm it and do not "fill in" its content; offer the closest verified papers.
- **Citation dated after the verification date** (or with an implausible volume/page): treat as likely nonexistent, say so, and still do not summarize it.
- **Ambiguous "the 2015 paper":** ask whether the publication year or the data-taking year is meant, and offer the candidate record from [source-index](source-index.md).
- **Unpublished claim:** classify as conference/preliminary/rumor; never state as an established result; never supply counts.
- **Missing performance number:** say which source class would contain it and what context is needed; do not estimate.
- **Internal AMS detail requested** (pass, trigger bit, good-run rule, calibration constants, internal notes): state that it is not public; offer a generic recommendation and list the missing evidence.
- **Old result vs new:** distinguish; do not mix definitions.

## Failure modes

- Citing search snippets; citing a paper not opened without stating so.
- Quoting a headline number without species/range/selection/period.
- Presenting a Tier 3 or 6 statement as a result; "latest" answered from memory.
- Attributing a general method to AMS because the paper is about AMS.
- Averaging or merging results with different definitions.

## Required source classes

This file itself: no AMS numbers. Evidence for the procedure: INSPIRE-HEP and journal records (Tier 1/2 for AMS); PDG (Tier 4).

## Questions to ask the user

Is browsing available for a current check? Which specific result, species, range, and period? Do you have a DOI or arXiv number for the paper in question? Is this for a public paper or an internal note?
