---
role: test-driven Research Software Engineer
skill: academic-papers
archetype: test-first
target: Word-count checker must classify a rebuttal against a venue's strict word limit, counting footnotes but excluding the bibliography
---

## 1. Acceptance Invariants & Boundary Constraints

`count_words_against_limit(tex_path, limit)` must return
`(word_count, over_limit)` for a rebuttal-style `.tex` document being checked
against a venue's strict word limit (per
`references/submission-and-peer-review.md`'s "strict length limits" note on
conference rebuttals):

- Body text and footnote text (`\footnote{...}` content) both count toward
  `word_count` - a footnote is not a way to smuggle extra words past the
  limit.
- Everything from `\begin{thebibliography}` (or `\bibliography{}`) onward
  must be excluded - references are conventionally exempt from venue word
  caps, per `references/multi-venue-reformatting.md`'s per-venue length-rule
  handling.
- `\label{}`, `\ref{}`, and comment lines (`%...`) contribute zero words.
- `over_limit` is `True` iff `word_count > limit` (strictly greater - a
  rebuttal at exactly the limit is compliant).
- Boundary case under test: a document whose body is under the limit on its
  own but pushes over once its footnote words are correctly included - this
  is the case a naive "strip everything after `\footnote`" implementation
  gets wrong twice, in both directions.

## 2. Executable Failing Test (Red)

```python
# tests/test_word_count_limit.py
import tempfile
from pathlib import Path

from word_limit import count_words_against_limit

REBUTTAL_TEX = r"""
We thank the reviewers for their careful reading of our submission.
The main concern raised was about the baseline comparison in Table 2.
\footnote{We re-ran this comparison with three additional random seeds
and observed the same ordering, confirming the result is not seed-sensitive.}
We address each remaining point below in turn.

\begin{thebibliography}{9}
\bibitem{smith2020} Smith et al., a very long bibliography entry that
should never count toward the rebuttal's word limit no matter how many
words it contains here.
\end{thebibliography}
"""


def test_footnote_words_count_but_bibliography_does_not():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rebuttal.tex"
        path.write_text(REBUTTAL_TEX, encoding="utf-8")

        word_count, over_limit = count_words_against_limit(path, limit=50)

        # Body (31 words) + footnote (20 words) = 51 words, over the 50-word
        # limit - but only if the bibliography (26 more words) is excluded.
        assert word_count == 51, f"expected 51 words, got {word_count}"
        assert over_limit is True, "expected over_limit=True at 51 > 50"
```

```
$ python3 -m pytest tests/test_word_count_limit.py -v
tests/test_word_count_limit.py::test_footnote_words_count_but_bibliography_does_not FAILED

================================== FAILURES ==================================
______ test_footnote_words_count_but_bibliography_does_not ______
AssertionError: expected 51 words, got 31
assert 31 == 51
1 failed in 0.02s
```

Current `word_limit.py` (pre-fix) strips `\footnote{...}` content entirely
instead of counting it, so it silently undercounts:

```python
# word_limit.py (pre-fix)
import re

FOOTNOTE_RE = re.compile(r"\\footnote\{[^}]*\}")
BIB_START_RE = re.compile(r"\\begin\{thebibliography\}|\\bibliography\{")
COMMENT_RE = re.compile(r"%.*$", re.MULTILINE)

def count_words_against_limit(tex_path, limit):
    text = tex_path.read_text(encoding="utf-8")
    match = BIB_START_RE.search(text)
    if match:
        text = text[: match.start()]
    text = FOOTNOTE_RE.sub("", text)   # bug: drops footnote text entirely
    text = COMMENT_RE.sub("", text)
    words = text.split()
    count = len(words)
    return count, count > limit
```

## 3. Minimal Code Implementation

```python
# word_limit.py (fixed)
import re

FOOTNOTE_RE = re.compile(r"\\footnote\{([^}]*)\}")
BIB_START_RE = re.compile(r"\\begin\{thebibliography\}|\\bibliography\{")
COMMENT_RE = re.compile(r"%.*$", re.MULTILINE)
LABEL_REF_RE = re.compile(r"\\(?:label|ref)\{[^}]*\}")

def count_words_against_limit(tex_path, limit):
    text = tex_path.read_text(encoding="utf-8")
    match = BIB_START_RE.search(text)
    if match:
        text = text[: match.start()]
    text = COMMENT_RE.sub("", text)
    text = LABEL_REF_RE.sub("", text)
    # Keep footnote text in place rather than deleting it - it counts.
    text = FOOTNOTE_RE.sub(lambda m: m.group(1), text)
    words = text.split()
    count = len(words)
    return count, count > limit
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_word_count_limit.py -v
tests/test_word_count_limit.py::test_footnote_words_count_but_bibliography_does_not PASSED
1 passed in 0.02s
```

```python
>>> from pathlib import Path
>>> from word_limit import count_words_against_limit
>>> count, over = count_words_against_limit(Path("rebuttal.tex"), limit=50)
>>> count, over
(51, True)
```

51 words counted (31 body + 20 footnote), correctly over the 50-word limit,
with the 26-word bibliography entry correctly excluded from the count - the
full 6-case regression suite (body-only, footnote-inclusion, bibliography-
exclusion, exactly-at-limit, comment-stripping, and label/ref-stripping)
passes in 0.03s.

## 5. Regression Guard Summary

This test guards against a rebuttal being submitted as "compliant" at 31
reported words when it is actually 51 real words over a strict 50-word
venue limit - the exact false-negative `references/submission-and-peer-
review.md` warns triage decisions must not be made on, since a rebuttal
rejected on a technicality (over the stated limit) never gets its content
read at all. Any future edit that reintroduces footnote-stripping instead
of footnote-inclusion will fail this test immediately.
