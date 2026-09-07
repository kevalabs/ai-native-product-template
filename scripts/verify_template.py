"""Check template scripts and required entry points without build artifacts."""

import ast
from pathlib import Path


root = Path(__file__).resolve().parents[1]
for directory in ("scripts", "tests"):
    for path in sorted((root / directory).glob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
for relative in (
    "Makefile", ".githooks/pre-commit", ".github/workflows/verify.yml",
    "scripts/check_sdlc.py", "scripts/check_github.py", "tests/test_sdlc.py", "tests/test_github.py",
):
    path = root / relative
    if not path.is_file() or not path.read_text().strip():
        raise SystemExit(f"Missing template entry point: {relative}")
print("Template scripts and entry points verified.")
