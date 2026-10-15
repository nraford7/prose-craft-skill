#!/usr/bin/env python3
"""The Mechanical Sweep from SKILL.md, as a script. It finds; it does not fix.
Usage: sweep.py <file.md> [...]   Exit 0 = clean, 1 = at least one hit.
Keep the lists in step with the Filter section of SKILL.md."""
import re, sys
from collections import Counter

BANNED_WORDS = [
    "delve", "utilize", "leverage", "robust", "streamline", "harness",
    "certainly", "tapestry", "landscape", "paradigm", "synergy", "ecosystem",
    "multifaceted", "nuanced", "pivotal", "transformative", "quietly",
    "deeply", "fundamentally", "remarkably", "arguably", "strikingly",
    "underscore", "resonate", "illuminate", "plethora", "myriad",
    "earn", "earns", "earned", "earning",
]
BANNED_PHRASES = [
    "pave the way", "when it comes to", "serves as", "stands as",
    "it's worth noting", "worth noting", "it bears mentioning", "importantly",
    "interestingly", "notably", "hard-earned", "here's the kicker",
    "here's the thing", "let's break this down", "unpack", "dive in",
    "imagine a world where", "the truth is simple", "think of it as",
    "in conclusion", "to sum up", "in this post", "in this article",
    "we'll cover", "as discussed", "in short,", "ultimately,",
    "move the needle", "circle back", "double down", "low-hanging fruit",
    "game changer", "game-changer", "best practices", "mission-critical",
    "lean into", "deep dive", "rent-free", "hits different", "chef's kiss",
    "let that sink in", "the quiet part out loud", "you can't unsee",
    "whether you're", "excited to announce", "thrilled to share",
    "proud to present", "as we all know", "in today's",
]
TEMPLATES = [
    (r"\bnot (just |only )?\w+[^.]{0,40}[,;—-]+ (it's|it is|but)\b", "negative parallelism"),
    (r"\bisn't just\b", "negative parallelism"),
    (r"\bnot because\b", "negative parallelism (causal)"),
    (r"\bthe question isn't\b", "cross-sentence reframe"),
    (r"\b(simple|elegant|powerful|lightweight|intuitive|flexible) (yet|but|and) \w+", "paired adjectives"),
    (r"\b\w+ing (its|their|the) (role|importance|significance)\b", "-ing significance tail"),
    (r"[“”‘’]", "smart quotes"),
    (r"\s→\s", "arrow"),
]
STOP = set("""about above after again against because before being below between
could does doing during every further having other should their there these
those through under until where which while would itself really""".split())

def sweep(path):
    text = re.sub(r"```.*?```", "", open(path).read(), flags=re.S)
    low = text.lower()
    hits = []
    for w in BANNED_WORDS:
        for m in re.finditer(rf"\b{w}\b", low):
            hits.append(("ban", w))
    for p in BANNED_PHRASES:
        n = len(re.findall(rf"(?<![\w']){re.escape(p)}", low))
        if n:
            hits.append(("ban", f"{p} x{n}"))
    for rx, label in TEMPLATES:
        for m in re.finditer(rx, text, re.I):
            hits.append(("template", f"{label}: '{m.group()[:50]}'"))
    dashes = text.count("—")
    if dashes > 3:
        hits.append(("em-dash", f"{dashes} (cap 3; a house style may lower it)"))
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    firsts = [re.sub(r"\W", "", s.split()[0].lower()) if s.split() else "" for s in sents]
    for i in range(len(firsts) - 2):
        if firsts[i] and firsts[i] == firsts[i+1] == firsts[i+2]:
            hits.append(("openers", f"3 in a row start with '{firsts[i]}'"))
    for para in text.split("\n\n"):
        c = Counter(w for w in re.findall(r"[a-z']{5,}", para.lower()) if w not in STOP)
        for w, n in c.items():
            if n >= 3:
                hits.append(("saturation", f"'{w}' x{n} in one paragraph"))
    words = re.findall(r"[a-z']+", low)
    c = Counter(w for w in words if len(w) >= 5 and w not in STOP)
    limit = 8 * max(1, len(words) / 2000)
    for w, n in c.items():
        if n > limit:
            hits.append(("saturation", f"'{w}' x{n} in {len(words)} words"))
    if text.count("!") > 3:
        hits.append(("exclamation", f"{text.count('!')} in piece"))
    if re.search(r"(?:#[A-Z]\w+\s+)+#[A-Z]\w+", text):
        hits.append(("hashtags", "hashtag block"))
    return hits

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    dirty = False
    for p in sys.argv[1:]:
        hits = sweep(p)
        dirty |= bool(hits)
        print(f"[{'HITS' if hits else 'CLEAN'}] {p}: {len(hits)}")
        for kind, msg in hits:
            print(f"  {kind}: {msg}")
    sys.exit(1 if dirty else 0)
