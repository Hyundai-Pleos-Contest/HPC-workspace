"""Validate shared policies and local Markdown links without third-party packages."""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = ("HPC-workspace", "HPC-fe", "HPC-be", "HPC-ai")
TEMPLATES = ROOT / "templates" / "common"


def check_repository(repo: Path) -> list[str]:
    errors: list[str] = []
    for template in sorted(TEMPLATES.rglob("*")):
        if not template.is_file():
            continue
        target = repo / template.relative_to(TEMPLATES)
        if not target.is_file():
            errors.append(f"Missing shared file: {target}")
        elif target.read_text(encoding="utf-8") != template.read_text(encoding="utf-8"):
            errors.append(f"Shared policy differs: {target}")
    for name in ("README.md", "AGENTS.md"):
        if not (repo / name).is_file():
            errors.append(f"Missing entry point: {repo / name}")
    return errors


def check_links() -> list[str]:
    errors: list[str] = []
    for folder in (ROOT, ROOT / "docs"):
        paths = folder.glob("*.md") if folder == ROOT else folder.rglob("*.md")
        for source in paths:
            for target in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                local = target.split("#", 1)[0]
                if local and not (source.parent / local).exists():
                    errors.append(f"Broken link in {source.name}: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--siblings", action="store_true", help="also check sibling repositories")
    args = parser.parse_args()
    repositories = [ROOT.parent / name for name in REPOSITORIES] if args.siblings else [ROOT]
    errors = check_links()
    for repository in repositories:
        errors.extend(check_repository(repository))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Shared policy and document checks passed ({len(repositories)} repositories).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
