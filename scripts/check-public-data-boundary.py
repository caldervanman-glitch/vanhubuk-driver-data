#!/usr/bin/env python3
"""Fail closed if private operational fields drift into the public driver-data repo.

This repository currently contains public-directory data. That does not make it an
acceptable store for raw signup/account/billing/identity material. This check is
intentionally structural: it inspects tracked data-file names and CSV headers, not
customer/driver values, so CI does not echo personal data into logs.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_HEADER_EXACT = {
    "email",
    "email_address",
    "private_email",
    "home_address",
    "date_of_birth",
    "dob",
    "supabase_user_id",
    "auth_user_id",
    "activation_token",
    "magic_link",
    "password",
    "password_hash",
    "stripe_customer_id",
    "stripe_subscription_id",
    "bank_account",
    "bank_account_number",
    "account_number",
    "sort_code",
    "policy_number",
    "insurance_policy_number",
    "insurance_document",
    "insurance_document_url",
    "driving_licence",
    "driving_licence_number",
    "passport_number",
    "identity_document",
}

FORBIDDEN_HEADER_PARTS = (
    "activation_token",
    "access_token",
    "refresh_token",
    "magic_link",
    "password",
    "secret",
    "stripe_customer",
    "stripe_subscription",
    "bank_account",
    "sort_code",
    "policy_number",
    "insurance_document",
    "licence_number",
    "license_number",
    "passport",
    "identity_document",
)

FORBIDDEN_DATA_FILENAME_PARTS = (
    "signup",
    "submission",
    "private",
    "credential",
    "secret",
    "token",
    "billing",
    "stripe",
    "bank",
    "insurance-document",
    "insurance_document",
)


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], check=True, text=True, stdout=subprocess.PIPE
    ).stdout.splitlines()
    return [Path(name) for name in out if name.strip()]


def main() -> int:
    errors: list[str] = []
    files = tracked_files()

    for path in files:
        low_name = normalise(path.as_posix())
        if path.suffix.lower() in {".csv", ".json", ".jsonl"} and any(
            normalise(part) in low_name for part in FORBIDDEN_DATA_FILENAME_PARTS
        ):
            errors.append(
                f"{path}: filename suggests private operational data in a public-data repository"
            )

        if path.suffix.lower() != ".csv":
            continue

        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f"{path}: cannot safely parse CSV header ({type(exc).__name__})")
            continue

        for raw in header:
            field = normalise(raw)
            if not field:
                continue
            if field in FORBIDDEN_HEADER_EXACT or any(part in field for part in FORBIDDEN_HEADER_PARTS):
                errors.append(
                    f"{path}: forbidden private/operational column {raw!r}; keep it in the private backend instead"
                )

    if errors:
        print("Public-data boundary FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Public-data boundary PASS: inspected {sum(p.suffix.lower() == '.csv' for p in files)} CSV headers "
        "without reading or logging row values."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
