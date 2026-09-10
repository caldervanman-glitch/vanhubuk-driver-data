#!/usr/bin/env python3
"""Fail closed when remote Git branches can hide unclassified work.

The registry supplies semantic disposition. Git ancestry supplies only mechanics.
A branch being "ahead" does NOT prove useful work is missing from main because
rebases/cherry-picks can reproduce identical content under different commits.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ALLOWED = {
    "CONTAINED",
    "SUPERSEDED",
    "ARCHIVE_EVIDENCE",
    "UNIQUE_REVIEW",
    "PII_QUARANTINE",
    "ORPHAN_ARTIFACT",
    "DUPLICATE_UNIQUE",
}
MUST_EXIST = {"ARCHIVE_EVIDENCE", "UNIQUE_REVIEW", "PII_QUARANTINE", "ORPHAN_ARTIFACT"}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def load_open_prs(path: str | None) -> list[dict]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"open-PR file does not exist: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("open-PR JSON must be a list")
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default="branch-dispositions.json")
    ap.add_argument("--main", default="origin/main")
    ap.add_argument("--open-prs")
    args = ap.parse_args()

    registry_path = Path(args.registry)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema_version") != 1:
        raise SystemExit("unsupported branch registry schema_version")
    if registry.get("canonical_branch") != "main":
        raise SystemExit("registry canonical_branch must be main")

    dispositions = registry.get("dispositions")
    if not isinstance(dispositions, dict):
        raise SystemExit("registry dispositions must be an object")

    open_prs = load_open_prs(args.open_prs)
    pr_heads: dict[str, list[int]] = {}
    pr_bases: dict[str, list[int]] = {}
    for pr in open_prs:
        number = int(pr.get("number", 0))
        head = pr.get("headRefName")
        base = pr.get("baseRefName")
        if isinstance(head, str):
            pr_heads.setdefault(head, []).append(number)
        if isinstance(base, str):
            pr_bases.setdefault(base, []).append(number)

    refs_raw = git(
        "for-each-ref",
        "--format=%(refname:strip=3)",
        "refs/remotes/origin",
    ).stdout.splitlines()
    branches = sorted({b.strip() for b in refs_raw if b.strip() and b.strip() != "HEAD"})
    if "main" not in branches:
        raise SystemExit("origin/main was not fetched")

    errors: list[str] = []
    warnings: list[str] = []
    rows: list[tuple[str, str, str, str]] = []

    for branch, record in sorted(dispositions.items()):
        if not isinstance(record, dict):
            errors.append(f"{branch}: registry entry is not an object")
            continue
        status = record.get("status")
        if status not in ALLOWED:
            errors.append(f"{branch}: invalid status {status!r}")
        canonical = record.get("canonical")
        if not isinstance(canonical, str) or not canonical:
            errors.append(f"{branch}: canonical branch/reference is required")

    for branch in branches:
        if branch == "main":
            rows.append((branch, "MAIN", "0", "canonical"))
            continue

        record = dispositions.get(branch)
        if record is None:
            if branch in pr_heads:
                nums = ",".join(f"#{n}" for n in sorted(pr_heads[branch]))
                rows.append((branch, "ACTIVE_PR", "?", f"open {nums}"))
                continue
            errors.append(
                f"{branch}: UNREGISTERED remote branch and not the head of an open PR; "
                "classify it before it can become hidden work"
            )
            rows.append((branch, "UNREGISTERED", "?", "ERROR"))
            continue

        status = record["status"]
        branch_ref = f"origin/{branch}"

        common = git("merge-base", args.main, branch_ref, check=False)
        has_common = common.returncode == 0 and bool(common.stdout.strip())
        is_ancestor = False
        unique = "orphan"
        if has_common:
            anc = git("merge-base", "--is-ancestor", branch_ref, args.main, check=False)
            is_ancestor = anc.returncode == 0
            unique = git("rev-list", "--count", f"{args.main}..{branch_ref}").stdout.strip()

        if status == "CONTAINED" and not is_ancestor:
            errors.append(
                f"{branch}: registry says CONTAINED but tip is not an ancestor of {args.main}; "
                "reconcile or reclassify it"
            )
        if status == "ORPHAN_ARTIFACT" and has_common:
            errors.append(
                f"{branch}: registry says ORPHAN_ARTIFACT but it now has a common ancestor with {args.main}; "
                "reclassify it"
            )
        if status == "DUPLICATE_UNIQUE":
            canonical = record.get("canonical")
            if canonical == branch:
                errors.append(f"{branch}: DUPLICATE_UNIQUE cannot point to itself")
            elif canonical != "main" and canonical not in branches:
                errors.append(f"{branch}: canonical duplicate target {canonical!r} does not exist remotely")

        prs = []
        if branch in pr_heads:
            prs.append("head " + ",".join(f"#{n}" for n in sorted(pr_heads[branch])))
        if branch in pr_bases:
            prs.append("base " + ",".join(f"#{n}" for n in sorted(pr_bases[branch])))
        tag = "; ".join(prs) if prs else ""
        rows.append((branch, status, unique, tag))

    remote = set(branches)
    for branch, record in sorted(dispositions.items()):
        if branch in remote:
            continue
        status = record.get("status")
        if status in MUST_EXIST:
            errors.append(
                f"{branch}: registry protects {status} material but the remote branch is missing; "
                "move/reclassify the evidence in the same change that removes the branch"
            )
        else:
            warnings.append(f"{branch}: registry entry remains but branch is absent ({status})")

    widths = [0, 0, 0, 0]
    headers = ("BRANCH", "DISPOSITION", "UNIQUE_COMMITS", "OPEN_PR_ROLE")
    for i, h in enumerate(headers):
        widths[i] = len(h)
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(value))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*("-" * w for w in widths)))
    for row in rows:
        print(fmt.format(*row))

    if warnings:
        print("\nWARNINGS")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nERRORS")
        for error in errors:
            print(f"- {error}")
        print(
            "\nBranch reconciliation FAILED. An unclassified, misclassified, "
            "or unexpectedly missing protected branch exists."
        )
        return 1

    print(
        f"\nBranch reconciliation PASS: {len(branches)} remote branches, "
        f"{len(dispositions)} registered historical branches, {len(open_prs)} open PRs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
