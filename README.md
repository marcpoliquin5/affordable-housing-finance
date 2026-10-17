# Affordable housing financing review

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

This project analyzes published financing for two real Housing Trust Group developments in Miami-Dade County: [Rainbow Village](https://www.htgf.com/news/rainbow-village-breaks-ground-miami-fl) and [Artisan Pointe Phase I](https://www.htgf.com/news/housing-trust-group-am-affordable-housing-secure-financing-for-phase-i-of-new-affordable-community-in-naranja-florida). Every figure in `deals.json` comes from those press releases. The Python code separates construction financing, permanent financing, equity, public loans, grants, and reimbursements. It does not infer loan seniority when the source does not state it.

## Run

Requires Python 3.11 or newer. No packages are required.

```bash
python analyze.py --verify-live --output FINANCING_REVIEW.md
```

The command checks that the source pages still publish the key figures, then writes a memo. Run `python analyze.py` to print it.

`HTG_Financing_Review.xlsx` presents the same sourced items in Excel. Its Summary tab uses formulas to calculate disclosed financing by stage and the reported cost per home; a blank cost remains blank where it was not disclosed. The Python analysis and live verification run independently of Excel.

## Important finance boundary

Construction loans and permanent loans are often sequential, and the releases do not publish the complete closing sources-and-uses schedules. Adding every announced amount would overstate available capital. This project reports financing by stage and leaves undisclosed totals blank. It does not invent operating income, debt service, interest rates, or investment returns.

## Sample output

Running `python analyze.py` prints the memo below (excerpt; the full output is in [`FINANCING_REVIEW.md`](FINANCING_REVIEW.md)):

```text
## Rainbow Village

Homes: 310
Reported development cost: $185.0m
Reported cost per home: $596,774
Published monthly rent range: $793–$2,634

| Financing item | Stage | Amount ($m) |
|---|---|---:|
| LIHTC equity | equity | 70.0 |
| SAIL financing | program financing | 15.0 |
| KeyBank construction financing | construction debt | 52.0 |
| JPMorgan Chase construction financing | construction debt | 57.2 |
| KeyBank permanent financing | permanent debt | 60.4 |
...
Construction facilities disclosed: $109.2m. Permanent facilities disclosed: $60.4m.
```

With `--verify-live`, the script first fetches each source page and reports, per figure, whether it is still published:

```text
{
  "source": "https://www.htgf.com/news/rainbow-village-breaks-ground-miami-fl",
  "checks": {
    "name": true,
    "units": true,
    "LIHTC equity": true,
    ...
  },
  "all_found": true
}
```

## Use cases

- **Disclosure review.** Reconcile announced financing for affordable housing deals against the public record, item by item, with every figure traceable to its source.
- **Capital-stack literacy.** Show how Low-Income Housing Tax Credit (LIHTC) equity, construction debt, permanent debt, public loans, grants, and reimbursements play different roles at different stages of a development.
- **Analyst training.** A compact worked example of a core real-estate finance discipline: classify each source correctly, and never sum amounts that represent sequential financing stages.
- **Template for other deals.** The `deals.json` data model and the live-verification logic are not tied to one developer. Covering other published deals means adding entries with their source URLs (and updating the memo's source line, which currently names Housing Trust Group).

## Why it matters

Press releases about affordable housing often list many financing sources side by side. Adding them together can overstate the capital available, because a construction loan is usually repaid by a permanent loan rather than stacked on top of it. Keeping financing stages separate, and leaving undisclosed values blank instead of estimating them, is the difference between a defensible analysis and a misleading one.

## Repository contents

| File | Purpose |
|---|---|
| `deals.json` | Sourced financing items for each development |
| `analyze.py` | Classification, memo generation, and live source verification |
| `FINANCING_REVIEW.md` | Generated memo |
| `HTG_Financing_Review.xlsx` | The same sourced items in Excel, with formula-driven summary |

## License

[MIT](LICENSE)
