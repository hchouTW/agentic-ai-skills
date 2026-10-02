#!/usr/bin/env python3
"""Fresh-model behavior eval for the T-prompts in tests/prompts.md, with a blind scorer.

Purpose: measure whether task-authoring changes the task document a model writes, without the
scorer being able to tell which arm (baseline or skill) wrote a plan.

What it does:
  run    - runs each H-prompt in isolated `claude -p` children, read-only (Read/Glob/Grep
           over a fixture repository copy), in two arms: `baseline` (no skill visible) and `skill`
           (skill symlinked as a project skill and the child told to read SKILL.md).
           Saves each plan plus the files the child read.
  score  - one scorer child per prompt scores every rubric bullet P/~/F for the
           shuffled plans of that prompt. --blind redacts skill mentions first and also
           asks the scorer to guess each plan's arm, to check that the blinding held.
  report - per-bullet table (baseline / skill) for one or two score files, the scorer's
           arm-guess accuracy, and how many skill references each skill run read.

Usage (costs money; needs the `claude` CLI):
  python3 tests/behavior_eval.py run --model haiku --runs 3 -j 6 --out RUNDIR
  python3 tests/behavior_eval.py score RUNDIR --blind --out RUNDIR/blind.json
  python3 tests/behavior_eval.py score RUNDIR --out RUNDIR/open.json
  python3 tests/behavior_eval.py report RUNDIR RUNDIR/open.json RUNDIR/blind.json

Isolation follows hep-analysis/tests/routing_eval.py: `--setting-sources project`
drops user settings, plugins and the user CLAUDE.md. Runs cannot edit or execute
anything, so rubric bullets are scored on the written task and message.
"""

import argparse
import concurrent.futures
import json
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
FIXTURE = SKILL_DIR / "tests" / "fixtures" / "shop_repo"
PROMPTS_MD = SKILL_DIR / "tests" / "prompts.md"
ARMS = ("baseline", "skill")

FRAME = (
    "The working directory is a small repository. You may read it but not change it. "
    "The user asked:\n\n{prompt}\n\n"
    "Reply with '## Task document' (the full document you would hand over) followed by "
    "'## Message to user' (the exact message you would send at the end of this turn)."
)
SKILL_PREFIX = (
    "Before answering, read .claude/skills/task-authoring/SKILL.md and follow it, "
    "loading the references it points you to.\n\n"
)
SCORE_FRAME = """You are scoring plans written by different AI assistants for the same task.

Task given to each assistant:
{prompt}

Rubric (score each bullet separately):
{rubric}

Score every bullet for every plan as P (pass), ~ (partial) or F (fail), each with a
short quote from the plan as justification.{guess}

Reply with only a JSON object, no prose, of the form
{{"<plan id>": {{"a": {{"score": "P", "why": "..."}}, "b": ...{guess_json}}}, ...}}

{plans}"""
GUESS = ("\nSome assistants followed a written engineering guideline and some did not. "
         "For each plan also guess which: \"guideline\", \"none\" or \"unsure\".")

# Words that name the skill or its files. Replaced by a neutral phrase in blind mode.
REDACT = [
    r"\.claude/skills/[\w./-]*",
    r"\btask[- ]authoring\b(?:\s+skill)?",
    r"\b(?:references|assets|scripts)/[\w.-]+\.(?:md|py)\b",
    r"\b[\w-]+-(?:discipline|playbook|framing|quality|and-done|and-estimation|architecture|guidelines)(?:\.md)?\b",
    r"\bSKILL(?:\.md)?\b",
    r"\b(?:the\s+)?Code File Requirement\b",
    r"\b(?:the\s+)?(?:Core Workflow|Decision Rules|Quick Checklists?|Before Reporting Done)\b",
    r"\bimplementation[- ]discipline\b",
    r"\b(?:the\s+)?skill(?:'s)?\b",
]
NEUTRAL = "the guidelines"


def redact(text):
    """Replace skill names, file paths and section names with a neutral phrase."""
    for pat in REDACT:
        text = re.sub(pat, NEUTRAL, text, flags=re.I)
    text = re.sub(rf"\b(?:the\s+)+{NEUTRAL}", NEUTRAL, text, flags=re.I)
    return re.sub(rf"{NEUTRAL}(?:'s)?(?:[ ,]+{NEUTRAL}(?:'s)?)+", NEUTRAL, text)


def load_prompts(path=PROMPTS_MD):
    """Return [{id, fixture, prompt, rubric, bullets}] for the T-rows of the prompts table."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(T\d+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", line)
        if not m:
            continue
        pid, fixture, prompt, rubric = m.groups()
        bullets = re.findall(r"\(([a-z])\)", rubric)
        rows.append({"id": pid, "fixture": fixture, "prompt": prompt, "rubric": rubric, "bullets": bullets})
    return rows


def claude(prompt, model, cwd, tools, timeout, max_turns=40):
    cmd = ["claude", "-p", prompt, "--model", model, "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
           *(["--allowedTools", *tools] if tools else [])]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    result, reads, cost, error = "", [], None, None
    for line in proc.stdout.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") != "tool_use":
                    continue
                if block["name"] == "Read":
                    reads.append(block.get("input", {}).get("file_path", ""))
                elif block["name"] == "Skill":  # loads SKILL.md without a Read call
                    reads.append(f"Skill:{block.get('input', {}).get('skill', '?')}/SKILL.md")
        elif msg.get("type") == "result":
            result = msg.get("result") or ""
            cost = msg.get("total_cost_usd")
            if msg.get("is_error"):
                error = msg.get("subtype")
    return {"text": result, "reads": reads, "cost_usd": cost, "error": error}


TEMPLATE = """# Task template (this repository)

## Summary
One or two sentences.

## Steps
Numbered list.

## Done when
Checklist of observable results.

## Risk
Who or what could be hurt, and the rollback.

## Owner
Team or person.
"""


def make_workdirs(root):
    """One work directory per (fixture, arm): a copy of the fixture repo, skill linked for the skill arm."""
    dirs = {}
    for fixture in ("shop", "tmpl"):
        for arm in ARMS:
            work = root / f"{fixture}_{arm}"
            shutil.copytree(FIXTURE, work)
            if fixture == "tmpl":
                (work / "docs").mkdir()
                (work / "docs" / "TASK_TEMPLATE.md").write_text(TEMPLATE)
            if arm == "skill":
                (work / ".claude" / "skills").mkdir(parents=True)
                (work / ".claude" / "skills" / "task-authoring").symlink_to(SKILL_DIR)
            dirs[(fixture, arm)] = work
    return dirs


def cmd_run(args):
    prompts = [p for p in load_prompts() if not args.only or p["id"] in args.only]
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    dirs = make_workdirs(pathlib.Path(tempfile.mkdtemp(prefix="behavior_eval_")))
    arms = args.arms or ARMS
    jobs = [(p, arm, r) for p in prompts for arm in arms for r in range(args.runs)]

    def one(job):
        p, arm, r = job
        done = out / f"{p['id']}_{arm}_{r}.json"
        if done.exists():  # resume: keep finished runs, redo empty or errored ones
            old = json.loads(done.read_text())
            if old["text"] and not old["error"]:
                return old
        body = FRAME.format(prompt=p["prompt"])
        if arm == "skill":
            body = SKILL_PREFIX + body
        res = claude(body, args.model, dirs[(p["fixture"], arm)], ["Read", "Glob", "Grep"], args.timeout)
        rec = {"id": p["id"], "arm": arm, "run": r, "model": args.model, **res}
        (out / f"{p['id']}_{arm}_{r}.json").write_text(json.dumps(rec, indent=1))
        return rec

    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        for rec in pool.map(one, jobs):
            flag = f" ERROR {rec['error']}" if rec["error"] or not rec["text"] else ""
            print(f"{rec['id']} {rec['arm']:8} run {rec['run']}: {len(rec['text'])} chars, "
                  f"{len(rec['reads'])} reads{flag}")
    return 0


def load_runs(rundir):
    return [json.loads(f.read_text()) for f in sorted(pathlib.Path(rundir).glob("T*_*_*.json"))]


def cmd_score(args):
    runs = load_runs(args.rundir)
    if args.only:
        runs = [r for r in runs if r["id"] in args.only]
    prompts = {p["id"]: p for p in load_prompts()}
    work = pathlib.Path(tempfile.mkdtemp(prefix="behavior_score_"))

    def one(pid):
        mine = [r for r in runs if r["id"] == pid]
        rng_local = random.Random(f"{args.seed}-{pid}")
        ids = rng_local.sample(range(100, 1000), len(mine))
        rng_local.shuffle(mine)
        key, blocks = {}, []
        for plan_id, rec in zip(ids, mine):
            text = redact(rec["text"]) if args.blind else rec["text"]
            key[str(plan_id)] = f"{rec['arm']}_{rec['run']}"
            blocks.append(f"=== plan {plan_id} ===\n{text}\n")
        body = SCORE_FRAME.format(
            prompt=prompts[pid]["prompt"], rubric=prompts[pid]["rubric"],
            guess=GUESS if args.blind else "",
            guess_json=', "guess": "guideline"' if args.blind else "",
            plans="\n".join(blocks))
        res = claude(body, args.model, work, [], args.timeout, max_turns=2)
        m = re.search(r"\{.*\}", res["text"], re.S)
        try:
            scores = json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError:
            scores = {}
        # Scorers sometimes write the id as "plan 123"; keep only the digits.
        scores = {re.sub(r"\D", "", k): v for k, v in scores.items()}
        if not scores:
            print(f"{pid}: scorer returned no JSON ({res['error']})", file=sys.stderr)
        return pid, {"key": key, "scores": scores}

    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        result = dict(pool.map(one, sorted({r["id"] for r in runs}, key=lambda s: int(s[1:]))))
    out = pathlib.Path(args.out)
    if args.only and out.exists():  # rescoring some prompts: keep the others
        old = json.loads(out.read_text())["prompts"]
        result = {**old, **result}
    out.write_text(json.dumps({"blind": args.blind, "prompts": result}, indent=1))
    print(f"wrote {args.out}")
    return 0


def tally(score_file, prompts):
    """Return {(pid, bullet): {arm: "PP~"}} and arm-guess counts."""
    data = json.loads(pathlib.Path(score_file).read_text())
    cells, guesses = {}, {"right": 0, "wrong": 0, "unsure": 0}
    for pid, block in data["prompts"].items():
        by_label = {}
        scores = {re.sub(r"\D", "", k): v for k, v in block["scores"].items()}
        for plan_id, label in block["key"].items():
            by_label[label] = scores.get(plan_id, {})
        for bullet in prompts[pid]["bullets"]:
            for arm in ARMS:
                labels = sorted(l for l in by_label if l.startswith(arm))
                marks = "".join(str((by_label[l].get(bullet) or {}).get("score", "?"))[:1]
                                for l in labels)
                cells.setdefault((pid, bullet), {})[arm] = marks
        for label, s in by_label.items():
            g = s.get("guess")
            if g is None:
                continue
            truth = "guideline" if label.startswith("skill") else "none"
            guesses["unsure" if g == "unsure" else "right" if g == truth else "wrong"] += 1
    return cells, guesses, data["blind"]


def cmd_report(args):
    prompts = {p["id"]: p for p in load_prompts()}
    tables = [tally(f, prompts) for f in args.scores]
    heads = ["blind" if t[2] else "open" for t in tables]
    print("| Prompt | " + " | ".join(f"{h} (baseline / skill)" for h in heads) + " |")
    print("|---" * (len(tables) + 1) + "|")
    for key in sorted(tables[0][0], key=lambda k: (int(k[0][1:]), k[1])):
        cols = [f"{t[0].get(key, {}).get('baseline', '')} / {t[0].get(key, {}).get('skill', '')}"
                for t in tables]
        print(f"| {key[0]} ({key[1]}) | " + " | ".join(cols) + " |")
    agree = total = 0
    if len(tables) == 2:
        for key, v in tables[0][0].items():
            for arm in ARMS:
                for x, y in zip(v[arm], tables[1][0].get(key, {}).get(arm, "")):
                    if "?" in (x, y):
                        continue
                    total += 1
                    agree += x == y
        print(f"\nopen-vs-blind agreement per bullet verdict: {agree}/{total}")
    for t, h in zip(tables, heads):
        if t[2]:
            print(f"{h} scorer arm guesses: {t[1]}")
    runs = [r for r in load_runs(args.rundir) if r["arm"] == "skill"]
    if runs:
        n_ref = [len({p for p in r["reads"] if "/references/" in p}) for r in runs]
        read_skill = sum(any(p.endswith("SKILL.md") for p in r["reads"]) for r in runs)
        print(f"skill runs that read SKILL.md: {read_skill}/{len(runs)}; "
              f"distinct references read per run: min {min(n_ref)}, max {max(n_ref)}, "
              f"mean {sum(n_ref) / len(n_ref):.1f}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--model", default="haiku")
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--only", nargs="*", help="prompt ids, e.g. T1 T6")
    r.add_argument("--arms", nargs="*", choices=ARMS)
    r.add_argument("-j", "--concurrency", type=int, default=6)
    r.add_argument("--timeout", type=int, default=600)
    r.add_argument("--out", required=True)
    s = sub.add_parser("score")
    s.add_argument("rundir")
    s.add_argument("--blind", action="store_true")
    s.add_argument("--model", default="sonnet")
    s.add_argument("--seed", default="0")
    s.add_argument("--only", nargs="*", help="rescore these prompt ids, merging into --out")
    s.add_argument("-j", "--concurrency", type=int, default=5)
    s.add_argument("--timeout", type=int, default=900)
    s.add_argument("--out", required=True)
    p = sub.add_parser("report")
    p.add_argument("rundir")
    p.add_argument("scores", nargs="+")
    args = ap.parse_args()
    return {"run": cmd_run, "score": cmd_score, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
