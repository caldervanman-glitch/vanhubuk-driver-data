#!/usr/bin/env python3
"""List conservative branch-pruning candidates; never delete anything.

A branch is a candidate only when the registry says CONTAINED and it is neither
the head nor base of an open PR. SUPERSEDED and all protected/evidence statuses
remain blocked because unique history can still be useful even when it is not
current implementation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default="branch-dispositions.json")
    ap.add_argument("--open-prs", required=True)
    args = ap.parse_args()

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    dispositions = registry.get("dispositions", {})
    open_prs = json.loads(Path(args.open_prs).read_text(encoding="utf-8"))

    protected_by_pr: dict[str, list[str]] = {}
    for pr in open_prs:
        number = int(pr.get("number", 0))
        for role, key in (("head", "headRefName"), ("base", "baseRefName")):
            branch = pr.get(key)
            if isinstance(branch, str) and branch:
                protected_by_pr.setdefault(branch, []).append(f"{role} of PR #{number}")

    branches = sorted({
        line.strip() for line in git(
            "for-each-ref", "--format=%(refname:strip=3)", "refs/remotes/origin"
        ).splitlines()
        if line.strip() and line.strip() not in {"HEAD", "main"}
    })

    candidates: list[str] = []
    for branch in branches:
        record = dispositions.get(branch)
        if not isinstance(record, dict) or record.get("status") != "CONTAINED":
            continue
        if record.get("protect_reason"):
            continue
        if branch in protected_by_pr:
            continue
        candidates.append(branch)

    print("CONSERVATIVE PRUNE CANDIDATES")
    print("Criteria: registry=CONTAINED and no open-PR head/base dependency.")
    print("This command never deletes branches. Re-run branch reconciliation immediately before any manual prune.\n")
    if not candidates:
        print("(none)")
    else:
        for branch in candidates:
            print(f"- {branch}")

    blocked_contained = sorted(
        branch for branch in branches
        if isinstance(dispositions.get(branch), dict)
        and dispositions[branch].get("status") == "CONTAINED"
        and branch in protected_by_pr
    )
    if blocked_contained:
        print("\nCONTAINED BUT BLOCKED BY OPEN PR")
        for branch in blocked_contained:
            print(f"- {branch}: {', '.join(sorted(protected_by_pr[branch]))}")

    print(f"\nCandidate count: {len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
