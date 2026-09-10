# VanHub UK live data

This repository is the canonical current-data source for the **public driver and town directory representation** shown on VanHub UK. **Current CSV blobs on `main` are authoritative for that public directory representation.** Do not select an older branch because its name or Git ahead count looks newer.

**Repository boundary:** authenticated driver accounts, activation, entitlements, billing and marketplace transaction state belong in `caldervanman-glitch/vanhub-marketplace`; VanChat conversational semantics/evaluation belong in `caldervanman-glitch/vanchat`. A signup may legitimately affect both the private Marketplace account state and this public directory representation, but do not make either one silently overwrite the other's authority.

Before reusing or deleting a historical branch, read [`BRANCH_RECONCILIATION.md`](BRANCH_RECONCILIATION.md) and [`branch-dispositions.json`](branch-dispositions.json). The automated branch audit prevents closed/unclassified work, including stale open-PR work, from disappearing outside the current control plane.

## Current data files

- Drivers.csv: the current drivers live on VanHub UK.
- Towns.csv: the current ordinary UK town collection.
- London Towns.csv: the current London town collection.

## Public-data boundary

This repository is currently public. Keep it limited to fields intentionally suitable for the public VanHub directory/town data. Do **not** add raw signup/submission exports, private email/home-address data, authentication or magic-link identifiers, billing/bank identifiers, identity documents, insurance documents/policy numbers, passwords, secrets or tokens.

`scripts/check-public-data-boundary.py` and its GitHub Actions workflow enforce the structural part of this boundary without reading or echoing CSV row values into CI logs. A future schema change that needs a currently prohibited field must be an explicit reviewed policy change, not an incidental import convenience.

## Signup update workflow

1. Start from current `main` and read Drivers.csv before processing new signup messages.
2. Use the complete VanHub signup emails as new evidence.
3. Cross-reference each signup against Drivers.csv to classify it as new, an update, a duplicate, unrelated or needing review.
4. Cross-reference each driver location against Towns.csv or London Towns.csv.
5. Add a missing town to the correct town CSV when the location is clear and the town data can be sourced safely.
6. Validate the driver and town CSVs together before updating this repository.

The inbox is the source of new signup evidence. These CSV files determine which drivers and towns are already live in the public directory; they do not define private account, entitlement or billing truth.
