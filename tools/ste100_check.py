#!/usr/bin/env python3
"""Mechanical checks for ASD-STE100 style documentation.

This tool checks the mechanical part of ASD-STE100 Part 1 (sentence length,
verb forms, sentence structure) with heuristics. It does not check the
controlled dictionary (Part 2), which is licensed. Use a project glossary for
the domain nouns and keep the terminology consistent by hand.

Codes used in the output are local identifiers, not ASD-STE100 rule numbers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROCEDURAL = "procedural"
DESCRIPTIVE = "descriptive"
LIMITS = {PROCEDURAL: 20, DESCRIPTIVE: 25}

CONTRACTIONS = re.compile(
    r"\b(?:don't|doesn't|didn't|can't|couldn't|won't|wouldn't|isn't|aren't|"
    r"wasn't|weren't|hasn't|haven't|hadn't|it's|that's|there's|let's|"
    r"we're|they're|you're|i'm|we've|they've|you've)\b",
    re.I,
)
LATIN = re.compile(r"\b(?:e\.g|i\.e|etc|via|vs|cf|approx)\.?\b", re.I)
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+(?:ed|en))\b", re.I
)
PERFECT = re.compile(r"\b(?:has|have|had)\s+(?:\w+ly\s+)?(\w+(?:ed|en))\b", re.I)
ING = re.compile(r"\b([A-Za-z]{4,}ing)\b")
MODALS = re.compile(r"\b(should|may|might|could|ought)\b", re.I)
VAGUE = re.compile(
    r"\b(?:several|various|some|many|few|appropriate|suitable|adequate|"
    r"proper|relevant|reasonable|etc)\b",
    re.I,
)
PHRASAL = re.compile(
    r"\b(?:carry out|set up|start up|take over|put in|make sure|"
    r"find out|look into|go on|turn on|turn off|switch off|check out)\b",
    re.I,
)
NOMINAL = re.compile(
    r"\b\w{4,}(?:tion|ment|ance|ence|ization|isation)\b", re.I
)
ABBREV = re.compile(r"\b(?:[A-Z]{2,6})s?\b")

# -ing words that are approved nouns or fixed terms in our documents.
ING_ALLOWED = {
    "shipping", "receiving", "transporting", "processing", "sampling",
    "packaging", "labelling", "labeling", "logging", "reporting",
    "monitoring", "building", "reading", "heading", "warning", "meaning",
    "string", "ring", "thing", "during", "something", "anything", "nothing",
    "everything", "ceiling", "spring", "bring", "brings", "according",
    "including", "excluding", "following", "settings", "mapping",
    "encoding", "decoding", "testing", "naming", "listing", "sorting",
}
# Words ending in -ed that are not participles.
ED_ALLOWED = {
    "red", "bed", "need", "speed", "feed", "seed", "indeed", "hundred",
    "thousand", "shed", "sued", "shred", "embed", "kindred", "sacred",
}
# Phrases where the passive is standard and acceptable.
PASSIVE_ALLOWED = (
    "is called", "are called", "is named", "are named", "is defined",
    "are defined", "is required", "are required", "is allowed",
    "are allowed", "is stored", "are stored",
)

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE = re.compile(r"^\s*\|")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
FRONTMATTER = re.compile(r"^---\s*$")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")


@dataclass
class Issue:
    path: str
    line: int
    code: str
    severity: str
    message: str
    text: str = ""


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)
    files: int = 0
    sentences: int = 0
    words: int = 0

    def add(self, *args, **kwargs):
        self.issues.append(Issue(*args, **kwargs))

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warn"]


def strip_markup(line: str) -> str:
    line = INLINE_CODE.sub(" ", line)
    line = LINK.sub(r"\1", line)
    line = URL.sub(" ", line)
    line = re.sub(r"[*_~>]{1,3}", "", line)
    return line


def read_blocks(path: Path):
    """Yield (line_number, text, in_list) for prose lines only."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    in_fence = False
    in_front = False
    for idx, raw in enumerate(lines, start=1):
        if FRONTMATTER.match(raw):
            if idx == 1:
                in_front = True
                continue
            if in_front:
                in_front = False
                continue
        if in_front:
            continue
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if TABLE.match(raw) or HEADING.match(raw):
            continue
        stripped = strip_markup(raw).strip()
        if not stripped:
            continue
        yield idx, stripped, bool(LIST_ITEM.match(raw))


def split_sentences(text: str):
    """Split on sentence ends. Keep abbreviations such as D1, v0.1, e.g. intact."""
    protected = re.sub(r"\b([A-Z]\d+|\d+\.\d+|[A-Z]{2,})\b", lambda m: m.group(0).replace(".", "\u0000"), text)
    parts = re.split(r"(?<=[.!?])\s+", protected)
    return [p.replace("\u0000", ".").strip() for p in parts if p.strip()]


def count_words(sentence: str) -> int:
    # Hyphenated compounds and identifiers count as one word.
    return len([w for w in re.split(r"\s+", sentence.strip()) if w])


def check_sentence(rep: Report, path: str, lineno: int, sentence: str, mode: str):
    words = count_words(sentence)
    rep.sentences += 1
    rep.words += words
    limit = LIMITS[mode]
    if words > limit:
        rep.add(path, lineno, "STE-S01", "error",
                f"sentence has {words} words, limit {limit} for {mode} text", sentence)

    if sentence.count("<") == 0 and re.search(r"\b(?:first|then|next|finally)\b,", sentence, re.I):
        pass

    if sentence.count(";") > 0:
        rep.add(path, lineno, "STE-P02", "warn", "semicolon splits two sentences", sentence)

    m = PASSIVE.search(sentence)
    if m and not any(p in sentence.lower() for p in PASSIVE_ALLOWED):
        rep.add(path, lineno, "STE-V01", "warn", f"possible passive voice: '{m.group(1)}'", sentence)

    m = PERFECT.search(sentence)
    if m and m.group(1).lower() not in ED_ALLOWED:
        rep.add(path, lineno, "STE-V02", "error", f"perfect tense: '{m.group(0)}'", sentence)

    for w in ING.findall(sentence):
        if w.lower() not in ING_ALLOWED:
            rep.add(path, lineno, "STE-V03", "warn", f"-ing form: '{w}'", sentence)
            break

    for m in MODALS.finditer(sentence):
        rep.add(path, lineno, "STE-V04", "warn",
                f"modal '{m.group(0)}': use 'must', 'can' or 'will'", sentence)
        break

    if CONTRACTIONS.search(sentence):
        rep.add(path, lineno, "STE-W01", "error", "contraction", sentence)

    for m in LATIN.finditer(sentence):
        rep.add(path, lineno, "STE-W02", "error", f"Latin abbreviation '{m.group(0)}'", sentence)
        break

    for m in VAGUE.finditer(sentence):
        rep.add(path, lineno, "STE-W03", "warn", f"vague word '{m.group(0)}'", sentence)
        break

    m = PHRASAL.search(sentence)
    if m:
        rep.add(path, lineno, "STE-W04", "warn", f"phrasal verb '{m.group(0)}'", sentence)

    # Noun cluster: four or more nouns in sequence.
    tokens = re.findall(r"[A-Za-z][A-Za-z-]+", sentence)
    run = 0
    for tok in tokens:
        if tok.lower() not in {
            "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with",
            "by", "at", "is", "are", "was", "were", "be", "this", "that", "these",
            "those", "it", "its", "from", "as", "if", "when", "must", "can",
            "will", "not", "no", "you", "we", "they", "he", "she", "all", "each",
            "one", "two", "three", "more", "than", "then", "also", "only", "but",
            "which", "who", "what", "how", "why", "where", "there", "their",
        }:
            run += 1
            if run >= 4:
                rep.add(path, lineno, "STE-N01", "warn",
                        "noun cluster of four or more words", sentence)
                break
        else:
            run = 0


def check_file(rep: Report, path: Path, mode: str):
    rep.files += 1
    para_lines: list[tuple[int, str]] = []

    def flush_para():
        if len(para_lines) > 6:
            rep.add(str(path), para_lines[6][0], "STE-P01", "warn",
                    f"paragraph has {len(para_lines)} sentences, limit 6",
                    para_lines[0][1])
        para_lines.clear()

    for lineno, text, is_list in read_blocks(path):
        if is_list:
            flush_para()
            sentences = split_sentences(text)
            for s in sentences:
                check_sentence(rep, str(path), lineno, s, PROCEDURAL)
            continue
        sentences = split_sentences(text)
        for s in sentences:
            check_sentence(rep, str(path), lineno, s, mode)
            para_lines.append((lineno, s))
    flush_para()


def guess_mode(path: Path) -> str:
    name = path.name.lower()
    if any(k in str(path).lower() for k in ("contributing", "readme", "install", "setup", "guide", "tutorial")):
        return PROCEDURAL
    return DESCRIPTIVE


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check markdown files against ASD-STE100 writing rules (mechanical part).")
    ap.add_argument("paths", nargs="+", help="files or directories")
    ap.add_argument("--mode", choices=[PROCEDURAL, DESCRIPTIVE, "auto"], default="auto")
    ap.add_argument("--max-words", type=int, default=0, help="override the sentence word limit")
    ap.add_argument("--json", action="store_true", help="machine readable output")
    ap.add_argument("--strict", action="store_true", help="warnings also fail the run")
    args = ap.parse_args(argv)

    if args.max_words:
        LIMITS[PROCEDURAL] = args.max_words
        LIMITS[DESCRIPTIVE] = args.max_words

    files: list[Path] = []
    for raw in args.paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(q for q in p.rglob("*.md") if ".git" not in q.parts))
        elif p.is_file():
            files.append(p)
        else:
            print(f"not found: {p}", file=sys.stderr)
            return 2
    if not files:
        print("no markdown files found", file=sys.stderr)
        return 2

    rep = Report()
    for f in files:
        mode = guess_mode(f) if args.mode == "auto" else args.mode
        check_file(rep, f, mode)

    if args.json:
        print(json.dumps({
            "files": rep.files,
            "sentences": rep.sentences,
            "words": rep.words,
            "errors": len(rep.errors),
            "warnings": len(rep.warnings),
            "issues": [i.__dict__ for i in rep.issues],
        }, ensure_ascii=False, indent=2))
    else:
        for i in sorted(rep.issues, key=lambda x: (x.path, x.line, x.code)):
            label = "ERROR" if i.severity == "error" else "warn "
            print(f"{i.path}:{i.line}: {label} [{i.code}] {i.message}")
            if i.text:
                snippet = i.text if len(i.text) <= 110 else i.text[:107] + "..."
                print(f"    {snippet}")
        print()
        print(f"{rep.files} files, {rep.sentences} sentences, {rep.words} words")
        print(f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")

    failed = bool(rep.errors) or (args.strict and rep.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
