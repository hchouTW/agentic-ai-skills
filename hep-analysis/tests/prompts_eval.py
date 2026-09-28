#!/usr/bin/env python3
"""Run the behavioral prompts in tests/prompts.md through fresh `claude -p` children.

Each run gets its own working directory (so runs cannot read each other's
scripts or plots) with the seven repo skills symlinked as project skills, and
`--setting-sources project` so no user plugins or CLAUDE.md leak in (see
routing_eval.py). By default the child is told to load hep-analysis first
("Haiku + skill", as in earlier VALIDATION.md passes). The routing prompts
(P11, N01, N02) run without that hint so the model has to route on its own.

The answers are saved for manual grading against the E/F items in prompts.md;
this script does not grade.

Usage:
  python3 tests/prompts_eval.py --model haiku --runs 2 -j 4 --out /tmp/prompts_run
  python3 tests/prompts_eval.py --only P05 P07 --runs 3 --out /tmp/p05_p07

Not a unit test: it calls the model and costs money. Needs the `claude` CLI.
"""

import argparse
import concurrent.futures
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
SKILLS = ["academic-diagrams", "academic-papers", "agile-development",
          "ams-analysis", "deep-learning", "hep-analysis", "task-authoring"]
ROUTING = {"P11", "N01", "N02"}
HINT = ("Load the hep-analysis skill (Skill tool) before answering. "
        "Work only in the current directory.\n\n")


def parse_prompts(path):
    """Return {id: prompt text} from the '### Pxx' blockquotes in prompts.md."""
    prompts, current = {}, None
    for line in path.read_text().splitlines():
        m = re.match(r"### ([PN]\d\d)\b", line)
        if m:
            current = m.group(1)
            prompts[current] = []
        elif current and line.startswith(">"):
            prompts[current].append(line[1:].strip())
        elif current and prompts[current] and not line.startswith(">"):
            current = None
    return {k: " ".join(v) for k, v in prompts.items()}


def run_one(pid, text, run, model, out, max_turns, timeout):
    work = out / f"{pid}_run{run}"
    skills = work / ".claude" / "skills"
    skills.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        link = skills / name
        if not link.exists():
            link.symlink_to(REPO / name)
    prompt = text if pid in ROUTING else HINT + text
    cmd = ["claude", "-p", prompt, "--model", model,
           "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns),
           "--allowedTools", "Read", "Glob", "Grep", "Skill", "Write", "Edit",
           "Bash(python3:*)"]
    skill_calls, reads, answer, cost, error = [], [], "", None, None
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True,
                              timeout=timeout)
        for line in proc.stdout.splitlines():
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("type") == "assistant":
                for block in msg.get("message", {}).get("content", []):
                    if block.get("type") != "tool_use":
                        continue
                    inp = block.get("input", {})
                    if block["name"] == "Skill":
                        skill_calls.append(inp.get("skill"))
                    elif block["name"] == "Read":
                        reads.append(inp.get("file_path", "").replace(str(REPO) + "/", ""))
            elif msg.get("type") == "result":
                answer = msg.get("result") or ""
                cost = msg.get("total_cost_usd")
                if msg.get("is_error"):
                    error = msg.get("subtype")
    except subprocess.TimeoutExpired:
        error = "timeout"
    res = {"id": pid, "run": run, "skills": skill_calls, "reads": reads,
           "cost_usd": cost, "error": error, "answer": answer}
    (work / "result.json").write_text(json.dumps(res, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--only", nargs="*", help="prompt ids, e.g. P01 P05")
    ap.add_argument("-j", "--concurrency", type=int, default=4)
    ap.add_argument("--max-turns", type=int, default=25)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--out", required=True, help="output directory")
    args = ap.parse_args()

    prompts = parse_prompts(HERE / "prompts.md")
    ids = args.only or sorted(prompts)
    out = pathlib.Path(args.out).resolve()
    jobs = [(pid, r) for pid in ids for r in range(args.runs)]
    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        futs = [pool.submit(run_one, pid, prompts[pid], r, args.model, out,
                            args.max_turns, args.timeout) for pid, r in jobs]
        results = [f.result() for f in futs]
    for res in results:
        print(f"{res['id']} run{res['run']}: skills={res['skills']} "
              f"refs={len([p for p in res['reads'] if 'references/' in p])} "
              f"err={res['error']} chars={len(res['answer'])}")
    cost = sum(r["cost_usd"] or 0 for r in results)
    print(f"model {args.model}; reported cost ${cost:.2f}; answers in {out}")
    (out / "summary.json").write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
