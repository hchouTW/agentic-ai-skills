---
role: Principal Software Engineer
skill: agile-development
archetype: gated-pipeline
high_stakes_task: adding a required new field to a shared public API contract used by multiple external client integrations, without breaking any of them
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the request: the `POST /v2/shipments` endpoint must start
requiring a `carrier_account_id` field so a new multi-carrier billing feature
can attribute costs correctly. Six external partner integrations currently
call this endpoint without that field.

Gaps found before drafting anything, checked against
`references/risk-and-quality.md`'s "API and Interface Changes" guidance to
"preserve request and response contracts unless change is required and
approved" and "document deprecations and migration guidance for breaking
changes":
- No inventory existed yet of which of the six partners could supply
  `carrier_account_id` today versus which would need lead time.
- No decision had been made on backward compatibility: making the field
  required immediately would break all six partners' existing integrations
  the moment it shipped.
- This is exactly the kind of consequential, hard-to-reverse contract change
  `references/software-architecture.md`'s "Recording the decision" section
  says warrants a lightweight ADR ("changing a public contract" is named
  explicitly), and none existed yet.

**Gate:** proceed to Phase 2 only once every partner's current capability to
supply the new field is inventoried (not assumed), and the choice between an
immediately-required field versus a phased rollout is written down as a
decision to be made, not deferred silently.

## Phase 2: Draft Synthesis

Drafted a lightweight ADR per `references/software-architecture.md`'s
minimal structure (Context / Decision / Alternatives Considered /
Consequences / Status):

- **Context**: multi-carrier billing needs `carrier_account_id` on every
  shipment; six external partners currently omit it.
- **Decision**: add the field as optional in `v2` with a server-assigned
  default account attributed to "unallocated," track its adoption per
  partner, and only enforce it as required in a new `v3` endpoint version
  once all six partners have migrated - never make an existing field
  required in-place on a version already in external use.
- **Alternatives considered**: making it required immediately in `v2` behind
  a short deprecation notice (rejected - `references/risk-and-quality.md`
  explicitly calls preserving existing contracts the default, and a notice
  period does not change that four of six partners have no active
  development cycle scheduled in the next quarter to react to it); a
  separate new endpoint entirely (rejected as unnecessary duplication when
  versioning already solves this).
- **Consequences**: "unallocated" billing needs its own reconciliation
  report until adoption is complete; `v3` becomes the second live API
  version to support in parallel.
- **Status**: proposed, pending Phase 3 review below.

The migration guidance required by `references/risk-and-quality.md`'s "API
and Interface Changes" section was drafted alongside the ADR: a partner
changelog entry naming the new optional field, its default behavior when
omitted, and the planned `v3` timeline, rather than only an internal note.

**Gate:** proceed to Phase 3 only once the ADR has a Consequences section
that names a concrete operational cost (not just the technical change) and
the partner-facing migration guidance exists as a reviewable draft.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing: "an optional field with an
'unallocated' default is a safe, fully backward-compatible interim state for
every partner." Reviewing each partner's actual integration pattern found
this assumption **false** for one of the six: that partner's integration
parses the full JSON schema strictly and rejects any response containing a
field it does not recognize - so returning the new field in the *response*
body (needed so partners can confirm what was recorded) would break that one
partner's client immediately, even though the field is optional on the
*request* side.

As a result:
- Added a per-partner response-schema capability flag, so the new field is
  included in the response only for partners confirmed to tolerate additional
  fields, and omitted for the one that doesn't, until that partner
  upgrades its client.
- Updated the ADR's Consequences section to name this exclusion explicitly
  rather than treating "optional field" as uniformly safe for all six
  partners.
- Confirmed with that one partner's integration contact a target date to
  relax their strict-schema parsing, tracked as a named follow-up rather than
  an open-ended item.

**Gate:** ship only once the response-schema capability flag is implemented
and verified against a replay of that one partner's actual client rejecting
an unrecognized field before the fix and accepting the response after it -
this is the release criterion, not an intermediate one.
