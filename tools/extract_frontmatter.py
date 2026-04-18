#!/usr/bin/env python3
"""Extract the `bodenkraft:` YAML frontmatter block from a Markdown/Quarto
document and print it as JSON on stdout.

Used by .github/workflows/validate.yml to feed the frontmatter into ajv
for JSON Schema validation.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Install with: pip install pyyaml\n"
    )
    sys.exit(2)


FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n",
    re.DOTALL,
)


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: extract_frontmatter.py <file>\n")
        return 2

    path = pathlib.Path(sys.argv[1])
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        sys.stderr.write(f"no YAML frontmatter found in {path}\n")
        return 1

    data = yaml.safe_load(match.group(1))
    block = data.get("bodenkraft") if isinstance(data, dict) else None
    if block is None:
        sys.stderr.write(f"no `bodenkraft:` block in {path} frontmatter\n")
        return 1

    json.dump(block, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
