#!/usr/bin/env python3
"""Harness-level trigger and sibling-routing eval for the repo skills.

Runs each query through a real `claude -p` child that sees only the built-in
skills plus the seven repo skills (no user plugins, no user CLAUDE.md), and
records which skill, if any, the model invokes first. This avoids the problem
that `claude plugin eval` inherits every installed plugin, which pushes plugin
skill descriptions out of the listing.

Isolation: `--setting-sources project` drops user settings (and with them the
user's plugins and ~/.claude/skills). The seven repo skills are symlinked into
the child's project `.claude/skills/`, so they are listed under their bare
names as in a normal ~/.claude/skills install. Do not load them as a plugin
(`--plugin-dir`): on 2026-09-26 the namespaced `plugin:skill` entries triggered
far less often on Haiku (2/6 vs 5/6 runs on the same queries), so plugin mode
understates recall. The child is killed as soon as it calls the Skill tool.

Usage:
  python3 tests/routing_eval.py tests/trigger_queries.json --model haiku \
      --runs 2 -j 4 --out /tmp/routing.json

Query file: a JSON list of {"query", "expect_hep_analysis", optional "owner"
(expected skill name or null) and "also_ok" (list of acceptable skills)}.
Not a unit test: it calls the model and costs money. Needs the `claude` CLI.
"""

import argparse
import concurrent.futures
import json
import os
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ["academic-diagrams", "academic-papers", "agile-development",
          "ams-analysis", "deep-learning", "hep-analysis", "task-authoring"]


def make_workdir(root: pathlib.Path) -> pathlib.Path:
    work = root / "work"
    skills = work / ".claude" / "skills"
    skills.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        (skills / name).symlink_to(REPO / name)
    return work


def run_one(query, model, workdir, max_turns, timeout):
    cmd = ["claude", "-p", query, "--model", model,
           "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns),
           "--allowedTools", "Read", "Glob", "Grep", "Skill"]
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True)
    skill, tools, cost, error = None, [], None, None
    try:
        for line in proc.stdout:
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("type") == "assistant":
                for block in msg.get("message", {}).get("content", []):
                    if block.get("type") == "tool_use":
                        tools.append(block["name"])
                        if block["name"] == "Skill":
                            skill = block.get("input", {}).get("skill", "?")
                            break
                if skill:
                    proc.kill()
                    break
            elif msg.get("type") == "result":
                cost = msg.get("total_cost_usd")
                if msg.get("is_error"):
                    error = msg.get("subtype")
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        error = "timeout"
    if skill:
        skill = skill.split(":", 1)[-1]  # tolerate a namespaced name
    return {"skill": skill, "tools": tools, "cost_usd": cost, "error": error}


def grade(case, skill):
    hep = skill == "hep-analysis"
    trig_ok = hep == case["expect_hep_analysis"] or skill in case.get("also_ok", [])
    route_ok = None
    if "owner" in case:
        ok = {case["owner"], *case.get("also_ok", [])}
        route_ok = skill in ok
    return trig_ok, route_ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("queries")
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("-j", "--concurrency", type=int, default=4)
    ap.add_argument("--max-turns", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--out", help="write per-run results as JSON")
    args = ap.parse_args()

    cases = json.loads(pathlib.Path(args.queries).read_text())
    root = pathlib.Path(tempfile.mkdtemp(prefix="routing_eval_"))
    work = make_workdir(root)
    jobs = [(i, r) for i in range(len(cases)) for r in range(args.runs)]
    results = {}
    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        futs = {pool.submit(run_one, cases[i]["query"], args.model,
                            work, args.max_turns, args.timeout): (i, r)
                for i, r in jobs}
        for fut in concurrent.futures.as_completed(futs):
            results[futs[fut]] = fut.result()

    rows, recall, fp, route, route_n = [], [0, 0], [0, 0], 0, 0
    for i, case in enumerate(cases):
        for r in range(args.runs):
            res = results[(i, r)]
            trig_ok, route_ok = grade(case, res["skill"])
            bucket = recall if case["expect_hep_analysis"] else fp
            bucket[1] += 1
            if case["expect_hep_analysis"]:
                bucket[0] += trig_ok
            else:
                bucket[0] += not trig_ok
            if route_ok is not None:
                route_n += 1
                route += route_ok
            rows.append({"case": i, "run": r, "query": case["query"],
                         "expect_hep_analysis": case["expect_hep_analysis"],
                         "owner": case.get("owner"), **res,
                         "trigger_ok": trig_ok, "route_ok": route_ok})
            if not trig_ok or route_ok is False:
                print(f"MISS case {i:2d} run {r}: got {res['skill']!r} "
                      f"(owner {case.get('owner')!r}, err {res['error']}) "
                      f"{case['query'][:70]}")
    cost = sum(x["cost_usd"] or 0 for x in rows)
    print(f"model {args.model}, {args.runs} runs/case")
    print(f"hep-analysis recall: {recall[0]}/{recall[1]} runs")
    print(f"hep-analysis false triggers: {fp[0]}/{fp[1]} runs")
    if route_n:
        print(f"routing to owner: {route}/{route_n} runs")
    print(f"reported cost (runs that finished; killed runs report none): ${cost:.2f}")
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
