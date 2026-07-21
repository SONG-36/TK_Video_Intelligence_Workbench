#!/usr/bin/env python3
"""Lightweight documentation checks for the design repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]

FORMAL_DOCS = [
    "00_MASTER_DESIGN.md",
    "01_CAPABILITY_ROADMAP.md",
    "02_DELIVERY_RELEASES.md",
    "03_RELEASE_1_SCOPE_AND_BOUNDARIES.md",
    "04_RELEASE_1_BUSINESS_PROCESS.md",
    "05_RELEASE_1_VERTICAL_SLICES.md",
    "architecture/01_PLATFORM_ARCHITECTURE.md",
    "architecture/02_ARCHITECTURE_DECISIONS.md",
]

REQUIRED_FRONTMATTER = {
    "document_type",
    "project",
    "baseline_version",
    "status",
    "implementation_allowed",
    "authority",
    "last_updated",
    "change_policy",
}

ALLOWED_STATUS = {
    "DRAFT_FOR_DISCUSSION",
    "DRAFT_FOR_REVIEW",
    "BASELINE_CANDIDATE",
    "BASELINE_APPROVED",
    "SUPERSEDED",
    "ARCHIVED",
}


failures: list[str] = []
warnings: list[str] = []
passes: list[str] = []


def report_pass(message: str) -> None:
    passes.append(message)
    print(f"PASS: {message}")


def report_fail(message: str) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def report_warning(message: str) -> None:
    warnings.append(message)
    print(f"WARNING: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return {}


def check_formal_docs_exist() -> None:
    missing = [doc for doc in FORMAL_DOCS if not (ROOT / doc).is_file()]
    if missing:
        report_fail(f"formal design documents missing: {', '.join(missing)}")
    else:
        report_pass("all formal design documents exist")


def check_h1(path: Path, text: str) -> None:
    h1_lines = re.findall(r"^#\s+.+$", text, flags=re.MULTILINE)
    rel = path.relative_to(ROOT)
    if len(h1_lines) == 1:
        report_pass(f"{rel} has exactly one H1")
    else:
        report_fail(f"{rel} has {len(h1_lines)} H1 headings")


def check_fences(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    in_fence = False
    fence_lang = ""
    fence_start = 0
    mermaid_unclosed = False

    for line_no, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*```\s*([^`]*)$", line)
        if not match:
            continue
        if not in_fence:
            in_fence = True
            fence_lang = match.group(1).strip().lower()
            fence_start = line_no
        else:
            in_fence = False
            fence_lang = ""
            fence_start = 0

    if in_fence:
        report_fail(f"{rel} has unclosed code fence starting at line {fence_start}")
        if fence_lang.startswith("mermaid"):
            mermaid_unclosed = True
    else:
        report_pass(f"{rel} code fences are closed")

    if mermaid_unclosed:
        report_fail(f"{rel} has an unclosed Mermaid fence")
    else:
        report_pass(f"{rel} Mermaid fences are structurally closed")


def check_frontmatter(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    frontmatter = parse_frontmatter(text)
    if not frontmatter:
        report_fail(f"{rel} has no parseable frontmatter")
        return

    missing = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
    if missing:
        report_fail(f"{rel} missing frontmatter fields: {', '.join(missing)}")
    else:
        report_pass(f"{rel} has required frontmatter fields")

    status = frontmatter.get("status", "")
    if status in ALLOWED_STATUS:
        report_pass(f"{rel} status is allowed: {status}")
    else:
        report_fail(f"{rel} status is not allowed: {status or '<missing>'}")

    implementation_allowed = frontmatter.get("implementation_allowed", "")
    if implementation_allowed.lower() == "false":
        report_pass(f"{rel} implementation_allowed is false")
    else:
        report_fail(f"{rel} implementation_allowed is not false")


def strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_links(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    checked = 0
    body = strip_code_fences(text)
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", body):
        raw_target = match.group(1).strip()
        if not raw_target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_target):
            continue
        target = raw_target.split("#", 1)[0]
        if not target:
            continue
        target = unquote(target)
        target_path = (path.parent / target).resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            report_fail(f"{rel} links outside repository: {raw_target}")
            continue
        checked += 1
        if not target_path.exists():
            report_fail(f"{rel} has broken relative link: {raw_target}")

    if checked:
        report_pass(f"{rel} relative links checked: {checked}")
    else:
        report_warning(f"{rel} has no relative Markdown links to check")


def all_markdown_files_for_links() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        rel_parts = path.relative_to(ROOT).parts
        if rel_parts[0] in {".git", "archive", "working"}:
            continue
        paths.append(path)
    return sorted(paths)


def check_master_candidates() -> None:
    candidates = [
        path
        for path in ROOT.glob("00_MASTER_DESIGN*.md")
        if "archive" not in path.parts and "working" not in path.parts
    ]
    if candidates == [ROOT / "00_MASTER_DESIGN.md"]:
        report_pass("root has only one formal 00_MASTER_DESIGN candidate")
    else:
        names = ", ".join(str(path.relative_to(ROOT)) for path in candidates)
        report_fail(f"root has multiple or unexpected Master Design candidates: {names}")


def main() -> int:
    print("Documentation checks")
    print("====================")

    check_formal_docs_exist()

    for doc in FORMAL_DOCS:
        path = ROOT / doc
        if not path.exists():
            continue
        text = read_text(path)
        check_h1(path, text)
        check_fences(path, text)
        check_frontmatter(path, text)

    for path in all_markdown_files_for_links():
        check_links(path, read_text(path))

    check_master_candidates()

    print("====================")
    print(f"PASS: {len(passes)}")
    print(f"WARNING: {len(warnings)}")
    print(f"FAIL: {len(failures)}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
