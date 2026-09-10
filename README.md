# VanHub UK live data

This repository is the canonical current-data source for the driver and town collections shown on VanHub UK. **Current CSV blobs on `main` are authoritative.** Do not select an older branch because its name or Git ahead count looks newer.

Before reusing or deleting a historical branch, read [`BRANCH_RECONCILIATION.md`](BRANCH_RECONCILIATION.md) and [`branch-dispositions.json`](branch-dispositions.json). The automated branch audit prevents closed/unclassified work from disappearing outside the normal PR view.

## Current data files

- Drivers.csv: the current drivers live on VanHub UK.
- Towns.csv: the current ordinary UK town collection.
- London Towns.csv: the current London town collection.

## Signup update workflow

1. Start from current `main` and read Drivers.csv before processing new signup messages.
2. Use the complete VanHub signup emails as new evidence.
3. Cross-reference each signup against Drivers.csv to classify it as new, an update, a duplicate, unrelated or needing review.
4. Cross-reference each driver location against Towns.csv or London Towns.csv.
5. Add a missing town to the correct town CSV when the location is clear and the town data can be sourced safely.
6. Validate the driver and town CSVs together before updating this repository.

The inbox is the source of new signup evidence. These CSV files determine which drivers and towns are already live.
