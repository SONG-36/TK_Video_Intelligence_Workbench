#!/usr/bin/env python3
"""Documentation checks for the consolidated canonical document set."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]

FORMAL_DOCS = [
    "00_PRODUCT_SYSTEM_OVERVIEW.md",
    "01_MVP_WALKING_SKELETON.md",
    "02_DOMAIN_MODEL.md",
    "03_TECHNICAL_ARCHITECTURE.md",
    "04_EVOLUTION_BACKLOG.md",
    "05_EXISTING_SYSTEM_MAPPING.md",
    "architecture/ADR_LOG.md",
]

OLD_FORMAL_DOCS = [
    "00_MASTER_DESIGN.md",
    "01_CAPABILITY_ROADMAP.md",
    "02_DELIVERY_RELEASES.md",
    "03_RELEASE_1_SCOPE_AND_BOUNDARIES.md",
    "04_RELEASE_1_BUSINESS_PROCESS.md",
    "05_RELEASE_1_VERTICAL_SLICES.md",
    "06_RELEASE_1A_MVP_SCOPE.md",
    "07_RELEASE_1A_IMPLEMENTATION_PLAN.md",
    "08_LONG_TERM_EVOLUTION_BACKLOG.md",
    "09_EXISTING_SYSTEM_MAPPING.md",
    "10_RELEASE_1A_TECHNICAL_BASELINE.md",
    "11_RELEASE_1A_DOMAIN_MODEL_LITE.md",
    "12_PHASE_I1_PRODUCT_WORKSPACE_PLAN.md",
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

REQUIRED_ENTRYPOINT_REFS = {
    "README.md": [
        "00_PRODUCT_SYSTEM_OVERVIEW.md",
        "01_MVP_WALKING_SKELETON.md",
        "02_DOMAIN_MODEL.md",
        "03_TECHNICAL_ARCHITECTURE.md",
        "04_EVOLUTION_BACKLOG.md",
        "05_EXISTING_SYSTEM_MAPPING.md",
        "architecture/ADR_LOG.md",
    ],
    "AGENTS.md": [
        "00_PRODUCT_SYSTEM_OVERVIEW.md",
        "01_MVP_WALKING_SKELETON.md",
        "02_DOMAIN_MODEL.md",
        "03_TECHNICAL_ARCHITECTURE.md",
        "04_EVOLUTION_BACKLOG.md",
        "05_EXISTING_SYSTEM_MAPPING.md",
        "architecture/ADR_LOG.md",
    ],
    "DOCUMENT_MAP.md": [
        "00_PRODUCT_SYSTEM_OVERVIEW.md",
        "01_MVP_WALKING_SKELETON.md",
        "02_DOMAIN_MODEL.md",
        "03_TECHNICAL_ARCHITECTURE.md",
        "04_EVOLUTION_BACKLOG.md",
        "05_EXISTING_SYSTEM_MAPPING.md",
        "architecture/ADR_LOG.md",
    ],
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


def is_under(path: Path, dirname: str) -> bool:
    return dirname in path.relative_to(ROOT).parts


def markdown_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*.md"):
        rel_parts = path.relative_to(ROOT).parts
        if ".git" in rel_parts or "archive" in rel_parts:
            continue
        paths.append(path)
    return sorted(paths)


def strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_formal_set() -> None:
    missing = [doc for doc in FORMAL_DOCS if not (ROOT / doc).is_file()]
    if missing:
        report_fail(f"formal documents missing: {', '.join(missing)}")
    else:
        report_pass("all formal documents exist")

    active_numbered = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.glob("[0-9][0-9]_*.md")
        if path.is_file()
    )
    expected_root = sorted(doc for doc in FORMAL_DOCS if "/" not in doc)
    if active_numbered == expected_root:
        report_pass("root formal numbered documents are exactly 00-05")
    else:
        report_fail(
            "unexpected root formal numbered documents: "
            + ", ".join(active_numbered)
        )

    architecture_md = sorted(
        str(path.relative_to(ROOT)) for path in (ROOT / "architecture").glob("*.md")
    )
    if architecture_md == ["architecture/ADR_LOG.md"]:
        report_pass("architecture formal documents are exactly ADR_LOG")
    else:
        report_fail(
            "unexpected architecture documents: "
            + ", ".join(architecture_md)
        )


def check_old_docs_absent() -> None:
    present = [doc for doc in OLD_FORMAL_DOCS if (ROOT / doc).exists()]
    if present:
        report_fail(f"old formal documents still present: {', '.join(present)}")
    else:
        report_pass("old formal documents are absent from active tree")

    disallowed = sorted(
        str(path.relative_to(ROOT))
        for pattern in ("06_*.md", "07_*.md", "08_*.md", "09_*.md", "10_*.md", "11_*.md", "12_*.md")
        for path in ROOT.glob(pattern)
    )
    if disallowed:
        report_fail("disallowed numbered formal files found: " + ", ".join(disallowed))
    else:
        report_pass("no disallowed numbered formal files found")


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
    fence_start = 0

    for line_no, line in enumerate(text.splitlines(), 1):
        if not re.match(r"^\s*```\s*[^`]*$", line):
            continue
        if not in_fence:
            in_fence = True
            fence_start = line_no
        else:
            in_fence = False
            fence_start = 0

    if in_fence:
        report_fail(f"{rel} has unclosed code fence starting at line {fence_start}")
    else:
        report_pass(f"{rel} code fences are closed")


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

    impl = frontmatter.get("implementation_allowed", "").lower()
    if impl == "false":
        report_pass(f"{rel} implementation_allowed is false")
    else:
        report_fail(f"{rel} implementation_allowed must be false")

    if frontmatter.get("last_updated") == "2026-07-22":
        report_pass(f"{rel} last_updated is 2026-07-22")
    else:
        report_fail(f"{rel} last_updated is not 2026-07-22")


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


def check_old_references() -> None:
    old_names = [Path(doc).name for doc in OLD_FORMAL_DOCS]
    old_paths = OLD_FORMAL_DOCS
    patterns = sorted(set(old_names + old_paths))
    offenders: list[str] = []

    for path in markdown_files():
        rel = str(path.relative_to(ROOT))
        if rel == "architecture/ADR_LOG.md":
            continue
        text = read_text(path)
        for pattern in patterns:
            if pattern in text:
                offenders.append(f"{rel}: {pattern}")

    if offenders:
        report_fail("old formal document references outside ADR_LOG: " + "; ".join(offenders[:20]))
    else:
        report_pass("old formal document references appear only in ADR_LOG")


def check_active_iteration_count() -> None:
    active = sorted(ROOT.glob("working/ACTIVE_ITERATION*.md"))
    if len(active) <= 1:
        report_pass("at most one ACTIVE_ITERATION file exists")
    else:
        report_fail(
            "multiple ACTIVE_ITERATION files found: "
            + ", ".join(str(path.relative_to(ROOT)) for path in active)
        )


def check_kernel_not_current_implementation() -> None:
    banned_patterns = [
        r"Platform Kernel code exists",
        r"Platform Kernel is implemented",
        r"Kernel Framework is implemented",
        r"current MVP implements Platform Kernel",
        r"current MVP implements Kernel Framework",
    ]
    offenders: list[str] = []
    for doc in FORMAL_DOCS:
        path = ROOT / doc
        if not path.exists():
            continue
        text = read_text(path)
        for pattern in banned_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                offenders.append(f"{doc}: {pattern}")
    if offenders:
        report_fail("formal docs imply Platform Kernel is currently implemented: " + "; ".join(offenders))
    else:
        report_pass("formal docs do not describe Platform Kernel as current implementation")


def check_entrypoints() -> None:
    for rel, required_refs in REQUIRED_ENTRYPOINT_REFS.items():
        path = ROOT / rel
        if not path.exists():
            report_fail(f"{rel} missing")
            continue
        text = read_text(path)
        missing = [ref for ref in required_refs if ref not in text]
        if missing:
            report_fail(f"{rel} missing new canonical refs: {', '.join(missing)}")
        else:
            report_pass(f"{rel} points to new canonical documents")


def check_no_implementation_true() -> None:
    offenders: list[str] = []
    for path in markdown_files():
        if "implementation_allowed: true" in read_text(path):
            offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        report_fail("implementation_allowed true found in markdown: " + ", ".join(offenders))
    else:
        report_pass("no implementation_allowed true in active markdown")


def main() -> int:
    print("Documentation checks")
    print("====================")

    check_formal_set()
    check_old_docs_absent()

    for doc in FORMAL_DOCS:
        path = ROOT / doc
        if not path.exists():
            continue
        text = read_text(path)
        check_h1(path, text)
        check_fences(path, text)
        check_frontmatter(path, text)

    for path in markdown_files():
        check_links(path, read_text(path))

    check_old_references()
    check_active_iteration_count()
    check_kernel_not_current_implementation()
    check_entrypoints()
    check_no_implementation_true()

    print("====================")
    print(f"PASS: {len(passes)}")
    print(f"WARNING: {len(warnings)}")
    print(f"FAIL: {len(failures)}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
