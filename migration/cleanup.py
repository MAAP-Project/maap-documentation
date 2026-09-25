"""Step 6: remove the Sphinx build files that no longer apply."""
from __future__ import annotations

from common import REPO


def run(ctx) -> None:
    targets = [
        ctx.src / "conf.py",
        REPO / "docs" / "Makefile",
        REPO / "docs" / "make.bat",
        REPO / "requirements.txt",
    ]
    for t in targets:
        if t.exists():
            t.unlink()
            ctx.report.add(str(t.relative_to(REPO)), "", "REMOVED", str(t.relative_to(REPO)))
    print(f"[cleanup] removed {ctx.report.count('REMOVED')} Sphinx files")
