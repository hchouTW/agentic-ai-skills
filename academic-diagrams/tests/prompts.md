# Behavior test prompts (academic-diagrams)

Fresh-model prompts with expected behaviors, used to check how often the skill changes what a
model does (open item in `TODO.md`). They are the ten prompts of the 2026-09-21 manual run,
written out with small concrete inputs so every run sees the same task.

Each prompt runs in a fresh `claude -p` session in two arms: **skill** (prefixed with
`/academic-diagrams`) and **baseline** (no skills). A separate grader model, not told the arm,
scores each answer against the "Must" and "Must not" lists: PASS if every Must holds and no
Must-not occurs, PARTIAL if one Must is missed and no Must-not occurs, FAIL otherwise.
Answers cannot render anything (no shell), so the graders judge the source text only.

Each prompt is delimited by `=== PROMPT` / `=== END`.

---

## D01 — Methods text to workflow

=== PROMPT
Turn this Methods paragraph into a workflow diagram for a paper.

"Events are selected with a single-muon trigger. We require exactly one muon with pT > 27 GeV
and at least two jets, one of which is b-tagged. The dominant backgrounds, ttbar and Z+jets,
are modelled with simulation; the multijet background is estimated from data. A BDT is trained
to separate signal from background and its output is fitted to extract the signal strength."
=== END

- Must: give a source in an editable text format (Mermaid, DOT, TikZ, ...), with a caption or a stated edge meaning.
- Must: show the data-driven multijet estimate separately from the simulated backgrounds.
- Must: flag that "Z+jets" is ambiguous or that the signal model is not stated, instead of silently picking one.
- Must not: add steps or tools the paragraph does not mention (e.g. a named generator, parton shower, unfolding) as facts.

## D02 — LHC-style event processing

=== PROMPT
Draw a conceptual diagram of how collider data and simulation each get from the detector or generator to a physics result. One figure for a thesis introduction.
=== END

- Must: keep the data chain and the simulation chain as parallel paths that meet at reconstruction/analysis, not one linear chain.
- Must: state that it is conceptual, not a specific experiment's software.
- Must not: name experiment-specific software or detector components as facts.

## D03 — Signal/control regions and simultaneous fit

=== PROMPT
I have a signal region and two control regions (one for ttbar, one for W+jets) and I fit all three simultaneously for the signal strength. Draw the analysis-region structure and how the fit connects them.
=== END

- Must: show the regions feeding one shared fit with shared parameters (signal strength and/or normalisation factors), not three independent fits.
- Must: use a stated meaning for the arrows.
- Must not: include a validation region inside the fit unless the user said so.

## D04 — Hierarchical Bayesian model to plates

=== PROMPT
Draw plate notation for this model: y_ij ~ Normal(theta_j, sigma^2) for i = 1..n observations in group j = 1..J; theta_j ~ Normal(mu, tau^2); mu ~ Normal(0, 10^2); tau ~ HalfCauchy(5); sigma is known and fixed at 0.5.
=== END

- Must: put y_ij inside the nested n and J plates, observed (shaded or otherwise marked), and theta_j inside the J plate only.
- Must: draw mu and tau as random variables (they have priors), and sigma as a fixed constant (not a random node).
- Must not: draw mu or tau as bare fixed hyperparameters.
- Must not: invent a "Figure 1" label or number.

## D05 — Causal DAG from stated assumptions

=== PROMPT
Draw the causal DAG for these assumptions only: genotype G affects smoking S and lung cancer C directly; smoking affects tar T; tar affects lung cancer; age A affects smoking and lung cancer. G is unmeasured. Nothing else.
=== END

- Must: contain exactly the six stated edges (G->S, G->C, S->T, T->C, A->S, A->C) and no others, with G marked as unmeasured/latent.
- Must: any identification remark is correct: with G unmeasured and a G->C edge, S->C effect via T cannot be read off by adjusting for G; do not claim G must be controlled while also saying it is unmeasured.
- Must not: add extra variables or edges (e.g. S->C direct, income, diet).

## D06 — MCMC to flowchart

=== PROMPT
Make a flowchart of random-walk Metropolis-Hastings sampling for a paper's appendix.
=== END

- Must: include the propose, accept/reject decision, record-sample step and a loop back, with an explicit stopping criterion or iteration count.
- Must: be valid editable source (Mermaid/DOT/TikZ) with labels that do not rely on unsupported syntax.
- Must not: show the accept/reject decision as a node with one outgoing edge.

## D07 — Repository to architecture

=== PROMPT
Draw an architecture diagram for this repository. I can't give you the files; this is the listing.

skillbox/
  SKILL.md                (links to 12 files under references/, 2 of them in other skills)
  references/             (10 markdown files: api.md, auth.md, cache.md, cli.md, config.md, errors.md, logging.md, models.md, queue.md, style.md)
  scripts/                (3 python files: build.py, lint.py, deploy.py)
  tests/                  (4 python files)
=== END

- Must: any file count in a node label matches the listing (10 references, 3 scripts, 4 tests), not 12 or 13.
- Must: state that it was drawn from the listing only and that dependencies between components are not known/not drawn as facts.
- Must not: invent runtime services, databases or call edges between scripts.

## D08 — Multi-agent system

=== PROMPT
Draw the architecture of a multi-agent research assistant: a planner agent splits a question into sub-questions, search agents fetch papers, a reader agent summarises them, and a writer agent produces the final report. Shared memory stores intermediate notes.
=== END

- Must: distinguish data flow from control flow (different line styles or a legend).
- Must: include the shared memory and the four named agents.
- Must: list assumptions or open questions (e.g. who triggers the search agents, whether there is a critic/verifier).
- Must not: add an orchestrator, critic or tool the user did not mention as a stated fact.

## D09 — Transformer code to figure

=== PROMPT
Draw the block structure of this decoder layer for a paper.

class Block(nn.Module):
    def forward(self, x, mask):
        x = x + self.drop(self.attn(self.ln1(x), mask=mask))
        x = x + self.drop(self.mlp(self.ln2(x)))
        return x
=== END

- Must: show pre-norm order (LayerNorm before attention and before MLP, inside each residual branch) with two residual connections.
- Must: show the causal/attention mask as an input to attention only and dropout on each branch output.
- Must not: draw post-norm or add cross-attention.

## D10 — Same figure in two formats

=== PROMPT
I need a simple three-stage figure (data preparation -> model training -> evaluation) once as Mermaid for my README and once as TikZ for my paper.
=== END

- Must: give both a Mermaid and a TikZ source with the same three stages in the same order.
- Must: declare the TikZ libraries or packages it needs.
- Must not: claim either was rendered or compiled (no tools were available).
