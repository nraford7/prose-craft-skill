# prose-craft regression test

Run this after any edit to `SKILL.md`, `constructions.md` or `figures.md`. It checks that the skill, applied by a fresh agent, turns machine-prose into clean prose without inventing facts. Pattern adapted from deslop-text's `/regtest` (adamdunkels/deslop-text, 2026-10-15).

Two layers:

1. **`sweep.py`** runs the Mechanical Sweep literally. Deterministic, free, catches listed words and templates. Keep its lists in step with the Filter.
2. **The agent test** below catches what a regex cannot: vague, hedged, empty prose with no listed phrase in it. The ChatGPT corpus texts are mostly this kind; `sweep.py` passes four of six originals.

## Corpus

`corpus/claude/` and `corpus/chatgpt/`: 12 machine-written drafts (blog post, newsletter, corporate memo, self-help article, product review, meeting summary). Copied from deslop-text under its MIT license (Copyright (c) 2026 Adam Dunkels). Landing pages, product pages and pitches were left out: conversion copy belongs to `copy-editing`.

Add a file by dropping a `.md` into any `corpus/<source>/` folder. Good additions target a check the corpus does not exercise yet.

## Running the agent test

Spawn one subagent per corpus file, all in one message so they run in parallel. Give each this prompt, with the path filled in:

> Read `~/.claude/skills/prose-craft/SKILL.md` (and `constructions.md` if you build sentences). Then read `<corpus file>`.
>
> 1. **Review.** List every Filter, Floor and Composition violation in the original, quoting the phrase.
> 2. **Fix.** Apply the skill's Workflow exactly, including the edit-vs-regenerate threshold. Keep every fact and claim the original makes. Keep lists as lists and headings as headings. **Do not invent facts, numbers, names or examples.** Where the original has no defensible claim, follow the skill: write the smallest truthful version and say what is missing in one line under the text.
> 3. **Verify.** Run `python3 ~/.claude/skills/prose-craft/tests/sweep.py` on your fixed text. Then re-read the skill and review the fixed text as if someone else wrote it.
> 4. **Readability.** Grammatical, coherent, original meaning kept, still reads as its genre.
> 5. Write the original violations, the fixed text, remaining violations, sweep output, readability verdict and PASS/FAIL to `~/.claude/skills/prose-craft/tests/results/<source>/<name>-result.md`. Return one line: `<source>/<name> | <violations before> | <sweep hits after> | <judgment violations after> | invented: yes/no | readable: yes/no | PASS/FAIL`.

**PASS** needs all of: zero `sweep.py` hits on the fixed text, at most two judgment-level violations left, no invented fact, readable. Any invented fact is an automatic FAIL. This is stricter than deslop-text, which lets the fixer add "plausible concrete detail".

Collect the lines into a table and end with `N of 12 passed`. List the checks behind each failure.

## What a failure means

- **The same check fails on several texts:** that Filter rule is unclear. Fix the rule in `SKILL.md`.
- **The fix introduced a new tell:** a rewrite principle needs a constraint.
- **One text fails once:** runs are not deterministic, because an LLM fixes and judges. Rerun it before changing the skill.

After any `SKILL.md` change, also run `Narrative-Engine/scripts/check-sync.sh`.

`results/` is gitignored.
