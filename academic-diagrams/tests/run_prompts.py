#!/usr/bin/env python3
"""Run tests/prompts.md in fresh `claude -p` sessions, with and without the skill,
and grade the answers blind with a separate model.

Arms:
  skill     the prompt is prefixed with "/academic-diagrams"; the skill is the only
            repo skill available (symlinked as a project skill)
  baseline  no repo skills available
Both arms run with `--setting-sources project` (no user skills, plugins or
CLAUDE.md) and without network tools, so nothing the answer states was looked up.

The grader sees the prompt, the Must / Must-not lists and the answer (with skill
names masked), not the arm, and returns PASS / PARTIAL / FAIL per the rule in
tests/prompts.md.

Usage:
  python3 tests/run_prompts.py --model sonnet --runs 1 --out /tmp/ad_runs
  python3 tests/run_prompts.py --only A07,A08 --arms skill --model haiku --out /tmp/x
  python3 tests/run_prompts.py --grade-only --out /tmp/ad_runs   # re-grade saved answers

Not a unit test: it calls the model and costs money. Needs the `claude` CLI.
"""

import argparse
import concurrent.futures
import json
import pathlib
import re
import subprocess
import sys
import tempfile

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
PROMPTS = SKILL_DIR / "tests" / "prompts.md"
NO_NETWORK = ["WebSearch", "WebFetch", "Bash"]
# The CLI returns a usage/spend-limit notice as an ordinary, non-error result.
LIMIT_RE = re.compile(r"hit your (monthly spend|usage|session) limit|usage limit reached", re.I)


def load_cases():
    text = PROMPTS.read_text(encoding="utf-8")
    cases = []
    for block in re.split(r"\n## ", text)[1:]:
        cid = block.split(" ", 1)[0]
        m = re.search(r"=== PROMPT\n(.*?)\n=== END\n(.*)", block, re.S)
        if not m:
            continue
        rubric = m.group(2).split("\n## ")[0].strip()
        cases.append({"id": cid, "prompt": m.group(1).strip(), "rubric": rubric})
    return cases


def make_workdirs(root: pathlib.Path):
    skill = root / "skill"
    (skill / ".claude" / "skills").mkdir(parents=True)
    (skill / ".claude" / "skills" / "academic-diagrams").symlink_to(SKILL_DIR)
    baseline = root / "baseline"
    baseline.mkdir()
    return {"skill": skill, "baseline": baseline}


def run_answer(prompt, arm, model, workdir, max_turns, timeout):
    text = f"/academic-diagrams {prompt}" if arm == "skill" else prompt
    cmd = ["claude", "-p", text, "--model", model, "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
           "--allowedTools", "Read", "Glob", "Grep", "Skill",
           "--disallowedTools", *NO_NETWORK]
    try:
        out = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return {"answer": "", "error": "timeout", "reads": [], "cost_usd": None}
    answer, reads, cost, error = "", [], None, None
    for line in out.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "assistant":
            for block in msg.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block["name"] == "Read":
                    reads.append(pathlib.Path(block["input"].get("file_path", "")).name)
        elif msg.get("type") == "result":
            answer = msg.get("result") or ""
            cost = msg.get("total_cost_usd")
            if msg.get("is_error"):
                error = msg.get("subtype")
    if LIMIT_RE.search(answer[:300]):
        error = "usage_limit"
    return {"answer": answer, "error": error, "reads": reads, "cost_usd": cost}


GRADER = """You are grading an answer to a user request against a fixed rubric.
Grade only what the answer says; do not reward length or style.

Rule: PASS if every "Must" item holds and no "Must not" item occurs. PARTIAL if
exactly one "Must" item is missed and no "Must not" item occurs. FAIL otherwise.

<request>
{prompt}
</request>

<rubric>
{rubric}
</rubric>

<answer>
{answer}
</answer>

Reply with JSON only, no prose, in this shape:
{{"items": [{{"item": "<short name>", "met": true, "why": "<one line>"}}], "verdict": "PASS|PARTIAL|FAIL"}}
"""


def mask(answer):
    return re.sub(r"academic-diagrams|academic-diagrams skill|the skill", "[source]", answer, flags=re.I)


def grade(case, answer, grader_model, timeout):
    prompt = GRADER.format(prompt=case["prompt"], rubric=case["rubric"], answer=mask(answer))
    cmd = ["claude", "-p", prompt, "--model", grader_model, "--setting-sources", "project",
           "--output-format", "json", "--max-turns", "1", "--tools", ""]
    with tempfile.TemporaryDirectory() as empty:
        try:
            out = subprocess.run(cmd, cwd=empty, capture_output=True, text=True, timeout=timeout).stdout
            result = json.loads(out).get("result", "")
            if LIMIT_RE.search(result[:300]):
                return {"verdict": "ERROR", "items": [], "error": "usage_limit"}
            return json.loads(re.search(r"\{.*\}", result, re.S).group(0))
        except (subprocess.TimeoutExpired, json.JSONDecodeError, AttributeError) as exc:
            return {"verdict": "ERROR", "items": [], "error": repr(exc)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--grader", default="opus")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--arms", default="skill,baseline")
    ap.add_argument("--only", help="comma-separated prompt ids, e.g. A07,A08")
    ap.add_argument("-j", "--concurrency", type=int, default=4)
    ap.add_argument("--max-turns", type=int, default=15)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--out", required=True, help="directory for answers.json and grades.json")
    ap.add_argument("--grade-only", action="store_true", help="re-grade saved answers")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cases = load_cases()
    if args.only:
        wanted = set(args.only.split(","))
        cases = [c for c in cases if c["id"] in wanted]
    by_id = {c["id"]: c for c in cases}

    answers_path = out / "answers.json"
    if args.grade_only:
        answers = json.loads(answers_path.read_text())
    else:
        dirs = make_workdirs(pathlib.Path(tempfile.mkdtemp(prefix="ad_prompts_")))
        jobs = [(c["id"], arm, r) for c in cases for arm in args.arms.split(",") for r in range(args.runs)]
        answers = []
        with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
            futs = {pool.submit(run_answer, by_id[cid]["prompt"], arm, args.model, dirs[arm],
                                args.max_turns, args.timeout): (cid, arm, r) for cid, arm, r in jobs}
            for fut in concurrent.futures.as_completed(futs):
                cid, arm, r = futs[fut]
                answers.append({"id": cid, "arm": arm, "run": r, "model": args.model, **fut.result()})
        answers.sort(key=lambda a: (a["id"], a["arm"], a["run"]))
        answers_path.write_text(json.dumps(answers, indent=1, ensure_ascii=False))

    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        futs = {pool.submit(grade, by_id[a["id"]], a["answer"], args.grader, args.timeout): i
                for i, a in enumerate(answers) if a["id"] in by_id and not a.get("error")}
        for fut in concurrent.futures.as_completed(futs):
            answers[futs[fut]]["grade"] = fut.result()
    (out / "grades.json").write_text(json.dumps(answers, indent=1, ensure_ascii=False))

    table = {}
    for a in answers:
        verdict = a["error"].upper() if a.get("error") else a.get("grade", {}).get("verdict", "?")
        table.setdefault(a["id"], {}).setdefault(a["arm"], []).append(verdict)
    arms = args.arms.split(",")
    print("id    " + "  ".join(f"{arm:<16}" for arm in arms))
    for cid in sorted(table):
        print(f"{cid:<6}" + "  ".join(f"{'/'.join(table[cid].get(arm, [])):<16}" for arm in arms))
    for arm in arms:
        v = [x for cid in table for x in table[cid].get(arm, [])]
        print(f"{arm}: PASS {v.count('PASS')}, PARTIAL {v.count('PARTIAL')}, FAIL {v.count('FAIL')}, "
              f"other {len(v) - v.count('PASS') - v.count('PARTIAL') - v.count('FAIL')}")
    cost = sum(a.get("cost_usd") or 0 for a in answers)
    print(f"answer cost ${cost:.2f} (grader cost not included)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
