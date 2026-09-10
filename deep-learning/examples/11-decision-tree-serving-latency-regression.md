---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: decision-tree
scenario: a deployed model's p99 serving latency regressed sharply, with the cause not yet isolated
---

## Triage Matrix

Formalizes `references/serving-architecture.md`'s "Latency has parts"
decomposition (`total = queueing + batching wait + compute + network +
pre/post-processing`) into a trigger-to-strategy mapping, so a latency
regression is decomposed before anything is optimized:

| Trigger | Resolution Strategy |
|---|---|
| Regression coincides with a traffic increase and per-replica utilization pushed above roughly 80% | Queueing delay growing nonlinearly with utilization - add replica capacity/headroom, not a model or code change, per "Utilization above roughly 80% causes queueing delay to grow sharply" |
| Regression coincides with a change to the dynamic-batching timeout or max batch size | Re-derive the batching timeout from the latency budget per "State the budget first" - a timeout set by default rather than from the budget is the cause, not the model |
| Regression coincides with longer input sequences/images, and profiled GPU compute time itself increased | Compute-bound regression - consider quantization, compilation, or right-sizing per "Making the model cheaper", each measured against the production distribution, not a benchmark |
| Regression appears after a routine redeploy with no traffic, batching, or input-size change, and profiled GPU compute time is unchanged | Check the non-model legs: pre/post-processing (tokenization, serialization), network, and cold-start/warmup time on the new replicas - these are "invisible if only GPU time is profiled" |
| Regression is isolated to autoregressive/generation requests with long context, other request types unaffected | KV cache memory limiting concurrency, not compute - size the cache explicitly per the KV-caching guidance rather than treating it as a generic compute problem |

## Selected Branch

Reported case: p99 latency for the tagging model doubled (180ms to 360ms)
immediately after a routine base-image rebuild that updated several
dependency versions; traffic volume and the batching config are unchanged
from before the rebuild; a quick GPU profiler trace shows compute time per
request is identical (41ms) to the pre-rebuild baseline. This matches the
fourth row: no traffic, batching, or input-size change, and compute time
itself is unchanged, pointing at the non-model legs rather than the model.

## End-to-End Execution Script

1. Measure each term in `total = queueing + batching wait + compute +
   network + pre/post-processing` separately rather than re-profiling GPU
   time again, per "Latency has parts"' warning that pre/post-processing is
   "frequently comparable to model compute for small models, and invisible
   if only GPU time is profiled."
2. Instrumented the request path: queueing 4ms (unchanged), batching wait
   6ms (unchanged), compute 41ms (unchanged), network 3ms (unchanged),
   pre/post-processing 301ms (up from 95ms pre-rebuild) - the regression is
   entirely in pre/post-processing.
3. Diffed the base-image rebuild's dependency changes and found the
   tokenizer library was bumped to a new major version whose default
   tokenizer backend changed from a compiled fast tokenizer to a pure-Python
   fallback, because the new image's build no longer includes the compiled
   extension's build dependency.
4. Fix: pin the tokenizer library's fast-tokenizer extra explicitly in the
   image build (`pip install "tokenizers[fast]==<pinned version>"`) rather
   than relying on it being pulled in transitively, and add a startup-time
   assertion that the fast backend loaded (`tokenizer.is_fast`) so a future
   image change that silently drops it fails at deploy time instead of
   showing up as a latency regression days later.
5. Rebuild the image with the pinned fast tokenizer, redeploy to a canary,
   and re-measure the same decomposition.

## Fallback Safeguards

If the pre/post-processing measurement had instead come back unchanged and
the regression were still unexplained, the next check would be cold-start
and warmup time specifically - a routine redeploy that increases the
compiled-graph warmup cost per replica can produce a similar-looking p99
regression under normal-looking average compute time, since warmup cost
shows up as tail latency on freshly-started replicas rather than in a
steady-state average. If the trigger turns out to have been misclassified
entirely (for instance, if utilization had in fact crept up gradually over
the same period as an unrelated coincidence), re-triage against the first
row and check replica utilization directly before continuing to chase the
non-model legs.
