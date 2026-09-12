---
role: Senior Platform / Developer-Experience Engineer
skill: skill-router
archetype: trajectory
problem_input: a request for help with a laptop's Wi-Fi dropping during video calls, with no domain-skill keyword present at all
---

## 1. Task Input & Context

A user asks: "My laptop's Wi-Fi keeps dropping every few minutes during video
calls, but wired ethernet is fine. Can you help me figure out why?" No code,
no physics, no manuscript, and no software-change verb anywhere in the
request - this is the case where none of the four rules have any surface
keyword to even false-positive on, unlike the "root cause of a CI failure"
carve-out case in example `03`.

## 2. Root-Cause Triage & Action Plan

Checked each rule in `SKILL.md` against the request in full:

- `academic-papers`: no paper, citation, or manuscript-writing task present.
- `agile-development`: no code, endpoint, migration, or dependency mentioned;
  "figure out why" is diagnostic language but not about a software change.
- `deep-learning`: no PyTorch, model, or training content.
- `hep-analysis`: no ROOT, physics, or detector content.

Per `SKILL.md`'s Behavior rule 4 ("If none of the rules apply, proceed
normally without mentioning this skill"), no domain skill is invoked. The
router does not manufacture a match by stretching "figure out why" into
`agile-development`'s debugging territory - that territory is specifically
"non-trivial software change," and diagnosing a home Wi-Fi network is not
one. Action plan: answer the networking question directly, using the
diagnostic pattern of narrowing scope before proposing a fix - the same
general discipline this collection's `agile-development` skill teaches for
software bugs, applied here without invoking that skill, since the subject
matter isn't code.

## 3. Surgical Execution

```
$ nmcli device wifi list
BSSID              SSID         CHAN  RATE       SIGNAL
AA:BB:CC:11:22:33  HomeNet-5G   149   866 Mbit/s  61
AA:BB:CC:11:22:44  HomeNet-5G   149   866 Mbit/s  38
```

Two access points broadcasting the same SSID on the same channel (149) with
overlapping signal strength is the classic cause of intermittent roaming
drops - the client repeatedly tries to hand off between them mid-call. Fix:
set the two APs to non-overlapping channels (149 and 44) rather than letting
them both claim the same one.

## 4. Verification Evidence

```
$ nmcli device wifi list
BSSID              SSID         CHAN  RATE       SIGNAL
AA:BB:CC:11:22:33  HomeNet-5G   149   866 Mbit/s  63
AA:BB:CC:11:22:44  HomeNet-5G   44    866 Mbit/s  41
$ ping -c 20 8.8.8.8 | tail -1
20 packets transmitted, 20 received, 0% packet loss, time 19042ms
```

After separating the channels, a 20-packet ping run during an active video
call shows zero loss, versus intermittent multi-second stalls before the
change.

## 5. Final Deliverable Summary

Confirmed no `SKILL.md` routing rule applied to a home-networking question
with zero domain-skill keywords present, and proceeded directly per Behavior
rule 4 rather than force-fitting it into `agile-development`'s debugging
territory. Diagnosed the Wi-Fi drops as a co-channel AP conflict and resolved
it by separating the two access points onto non-overlapping channels,
verified by a clean 20-packet ping run during an active call.
