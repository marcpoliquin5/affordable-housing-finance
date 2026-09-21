# Affordable housing financing review

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

## Job fit

The [Housing Trust Group Finance Coordinator opening](https://htg.hrmdirect.com/employment/job-openings.php?search=true) involves project accounting, debt, equity, due diligence, and budgeting. This project demonstrates source reconciliation and financing classification using the employer's own public disclosures. It is also relevant to real-estate credit and reporting roles in the Monday job shortlist.
