"""Validate the self-contained Markdown Skill and its example; Python stdlib only."""

import json
from pathlib import Path
import re
import sys


NAME = "local-evidence-navigation"
EXPECTED = {
    "SKILL.md",
    "references/navigation-policy.md",
    "references/evidence-contract.md",
    "references/evidence-reading.md",
    "references/source-adapters.md",
    "references/harness-workflow.md",
    "references/conformance.md",
    "references/implementation-map.md",
    "assets/NAVIGATION-PROFILE.template.md",
    "assets/EVIDENCE-LEDGER.template.md",
    "assets/GAP-DECISION.template.md",
    "assets/ANSWER.template.md",
    "assets/NAVIGATION-EXAMPLE.md",
}


def reject_nonfinite(value):
    raise ValueError(f"Nonfinite JSON value: {value}")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def validate(root):
    root = Path(root).resolve()
    entries = list(root.rglob("*"))
    if any(p.is_symlink() for p in entries):
        raise ValueError("Skill payload must contain actual files, not symlinks")
    files = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    if files != EXPECTED:
        raise ValueError(f"Payload mismatch: missing={EXPECTED - files}, extra={files - EXPECTED}")
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    fields = {}
    for line in match[1].splitlines():
        key, value = line.split(":", 1)
        if key in fields:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        fields[key] = value.strip()
    if set(fields) != {"name", "description"}:
        raise ValueError("Expected name and description scalar frontmatter only")
    if fields["name"] != NAME or root.name != NAME:
        raise ValueError("Skill name and folder must agree")
    if not 1 <= len(fields["description"]) <= 1024:
        raise ValueError("Invalid description length")
    links = 0
    json_templates = 0
    for relative in sorted(files):
        path = root / relative
        body = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[^/\s]+/|[A-Z]:\\Users\\", body):
            raise ValueError(f"Machine-specific path in {relative}")
        if "[TODO:" in body:
            raise ValueError(f"Unfinished scaffold in {relative}")
        fence = None
        for line in body.splitlines():
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
        if fence:
            raise ValueError(f"Unclosed code fence in {relative}")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError(f"Broken or escaping link: {relative} -> {target}")
            links += 1
        for payload in re.findall(r"^```json\n(.*?)\n```", body, re.M | re.S):
            data = json.loads(payload, parse_constant=reject_nonfinite, object_pairs_hook=unique_keys)
            if not isinstance(data, dict):
                raise ValueError(f"Expected JSON object template in {relative}")
            json_templates += 1
    if json_templates != 4:
        raise ValueError("Expected four JSON blocks for ledger, evidence, gap and answer")
    example = (root / "assets/NAVIGATION-EXAMPLE.md").read_text(encoding="utf-8")
    source = re.search(r"^```text\n(.*?)\n```", example, re.M | re.S)
    if not source:
        raise ValueError("Missing example source excerpt")
    lines = source[1].splitlines()
    quotes = re.findall(r"第\s*(\d+)\s*行“([^”]+)”", example)
    if len(quotes) < 4:
        raise ValueError("Example must include located quotations")
    for number, quote in quotes:
        index = int(number) - 1
        if index < 0 or index >= len(lines) or lines[index] != quote:
            raise ValueError(f"Example quotation mismatch at line {number}: {quote}")
    print(f"PASS: {len(files)} Markdown files, {links} local links, {json_templates} JSON blocks, {len(quotes)} exact example quotations")


if __name__ == "__main__":
    skill_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "skills" / NAME
    try:
        validate(skill_root)
    except (ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
