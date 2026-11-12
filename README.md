# Affordable housing financing review

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)

Breaks down the published financing for two Housing Trust Group developments in Miami-Dade County, [Rainbow Village](https://www.htgf.com/news/rainbow-village-breaks-ground-miami-fl) (310 homes) and [Artisan Pointe Phase I](https://www.htgf.com/news/housing-trust-group-am-affordable-housing-secure-financing-for-phase-i-of-new-affordable-community-in-naranja-florida) (115 homes), by financing stage, and re-checks every figure against its source page.

## The problem

A financing announcement for an affordable housing deal lists tax-credit equity, construction loans, permanent loans, public loans and grants side by side. Adding them up overstates the capital behind the project, because a construction loan is normally repaid by the permanent loan rather than stacked on top of it. Rainbow Village's release names $109.2m of construction facilities and a $60.4m permanent loan against a $185.0m reported cost; a naive total would count both.

This project keeps the stages apart and reports only what the sources disclose.

## What it does

- **`deals.json`** holds each development's financing items (label, amount, stage) and its source URL. Every figure comes from the two press releases linked above.
- **`analyze.py`** validates the data, totals financing by stage, computes reported cost per home where a cost was published, and writes a Markdown memo.
- **`--verify-live`** fetches each source page and confirms that the project name, unit count and every financing amount still appear on it. It exits with code 2 if any figure is missing.
- **`HTG_Financing_Review.xlsx`** presents the same items in Excel. Its Summary tab uses `SUMIF` formulas for financing by stage and cost per home.

## Run

Requires Python 3.11 or newer. No packages to install.

```bash
python analyze.py                                          # print the memo
python analyze.py --verify-live --output FINANCING_REVIEW.md   # check sources, then write it
```

## Sample output

Excerpt from `python analyze.py` (full memo: [`FINANCING_REVIEW.md`](FINANCING_REVIEW.md)):

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

With `--verify-live`, each source is checked figure by figure first:

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

## Scope

This is a review of public disclosures, not an underwriting model.

- The press releases do not include closing sources-and-uses schedules, so there is no final capital stack here.
- Values a source does not publish stay blank. Artisan Pointe's total development cost is one example.
- Loan seniority is not recorded, because the sources do not state it.
- Operating income, debt service, interest rates and returns are out of scope.

To cover another deal, add an entry to `deals.json` with its source URL. The memo's header currently names Housing Trust Group and would need updating for other developers.

## License

[MIT](LICENSE)
