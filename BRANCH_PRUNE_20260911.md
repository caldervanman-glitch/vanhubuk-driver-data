# Driver-data branch prune — 2026-09-11

The prune removed only redundant branch refs while preserving historical material that may still be useful.

## Result

- Remote branches: **4 → 2**.
- Deleted: `data/import-new-drivers-20260821` after proof that its tip was already contained in `main`.
- Deleted: merged cleanup head after PR #4 landed.
- Retained: `data/add-london-towns-20260821` as `SUPERSEDED` reference history.
- No driver/town CSV row content changed.

The canonical directory datasets remain the files on `main`.
