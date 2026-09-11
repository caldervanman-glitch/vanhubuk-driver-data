# VanHub UK live directory data

This repository is the canonical current-data source for the **driver and town directory representation** shown on VanHub UK. **Current CSV blobs on `main` are authoritative for that directory representation.** Do not select an older branch because its name or Git ahead count looks newer.

**Repository boundary:** authenticated driver accounts, activation, entitlements, billing and marketplace transaction state belong in `caldervanman-glitch/vanhub-marketplace`; VanChat conversational semantics/evaluation belong in `caldervanman-glitch/vanchat`. A signup may legitimately affect both the private Marketplace account state and this directory representation, but do not make either one silently overwrite the other's authority.

Before reusing or deleting a historical branch, read [`BRANCH_RECONCILIATION.md`](BRANCH_RECONCILIATION.md) and [`branch-dispositions.json`](branch-dispositions.json). The automated branch audit prevents closed/unclassified work, including stale open-PR work, from disappearing outside the current control plane.

## Current data files

- `Drivers.csv`: the current drivers represented on VanHub UK.
- `Towns.csv`: the current ordinary UK town collection.
- `London Towns.csv`: the current London town collection.

## Repository visibility and data boundary

This repository should be **private**. The directory workflow does not require anonymous GitHub access, raw GitHub URLs or GitHub Pages. A dependency audit on 2026-09-10 found no runtime/code reference to this repository from the inspected VanHub application/support repositories and no GitHub Pages surface here.

The CSVs intentionally contain directory-facing fields, but Git history is a broader and more permanent exposure boundary than the live profile page. Keep the repository limited to data that belongs in the directory representation and do **not** add raw signup/submission exports, private email/home-address data, authentication or magic-link identifiers, billing/bank identifiers, identity documents, insurance documents/policy numbers, passwords, secrets or tokens.

`scripts/check-public-data-boundary.py` and its GitHub Actions workflow enforce the structural part of this boundary without reading or echoing CSV row values into CI logs. The guard remains useful even when the repository is private: private Git is still not the correct store for account secrets, billing data or identity documents.

Do not introduce anonymous `raw.githubusercontent.com` reads as a future application dependency. Application/runtime consumers should use the owning Marketplace/Framer data path rather than relying on repository visibility.

## Signup update workflow

1. Start from current `main` and read `Drivers.csv` before processing new signup messages.
2. Use the complete VanHub signup emails as new evidence.
3. Cross-reference each signup against `Drivers.csv` to classify it as new, an update, a duplicate, unrelated or needing review.
4. Cross-reference each driver location against `Towns.csv` or `London Towns.csv`.
5. Add a missing town to the correct town CSV when the location is clear and the town data can be sourced safely.
6. Validate the driver and town CSVs together before updating this repository.

The inbox is the source of new signup evidence. These CSV files determine which drivers and towns are already represented in the directory; they do not define private account, entitlement or billing truth.
