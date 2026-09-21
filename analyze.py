"""Analyze disclosed financing for real HTG affordable housing developments."""

from __future__ import annotations

import argparse
import json
import urllib.request
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).with_name("deals.json")


def load_deals() -> list[dict]:
    deals = json.loads(DATA.read_text(encoding="utf-8"), parse_float=Decimal)
    for deal in deals:
        if deal["units"] <= 0:
            raise ValueError("Unit count must be positive")
        for item in deal["funding"]:
            if item["amount_millions"] <= 0:
                raise ValueError("Funding amounts must be positive")
    return deals


def summarize(deal: dict) -> dict:
    by_stage = defaultdict(Decimal)
    for item in deal["funding"]:
        by_stage[item["stage"]] += item["amount_millions"]
    cost = deal["reported_project_cost_millions"]
    return {
        "name": deal["name"],
        "publication_date": deal["publication_date"],
        "source": deal["source"],
        "units": deal["units"],
        "reported_project_cost_millions": cost,
        "reported_cost_per_unit_usd": None if cost is None else int(cost * 1_000_000 / deal["units"]),
        "funding_by_stage_millions": dict(by_stage),
        "construction_facilities_millions": by_stage["construction_debt"],
        "permanent_facilities_millions": by_stage["permanent_debt"],
        "rent_range_monthly_usd": deal["rent_range_monthly_usd"],
        "note": "Construction and permanent facilities are different financing stages. The press release does not provide a closing sources-and-uses schedule, so listed amounts must not be added into a final capital stack."
    }


def verify_live(deals: list[dict]) -> list[dict]:
    """Check that each public source still publishes the reported headline facts."""
    results = []
    for deal in deals:
        request = urllib.request.Request(deal["source"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=25) as response:
            page = response.read(4_000_001).decode("utf-8", errors="replace")
        checks = {"name": deal["name"].split(" Phase")[0] in page,
                  "units": str(deal["units"]) in page}
        for item in deal["funding"]:
            amount = item["amount_millions"]
            written = format(amount.normalize(), "f")
            alternatives = (f"${written} million", f"${int(amount * 1_000_000):,}")
            checks[item["label"]] = any(value in page for value in alternatives)
        results.append({"source": deal["source"], "checks": checks,
                        "all_found": all(checks.values())})
    return results


def report(deals: list[dict]) -> str:
    sections = ["# Published financing review", "", "Figures below come from Housing Trust Group press releases. Amounts are USD millions unless noted. This is a disclosure review, not an underwriting model or verified closing statement.", ""]
    for deal in deals:
        summary = summarize(deal)
        sections += [f"## {deal['name']}", "", f"Source: {deal['source']} ({deal['publication_date']})", "",
                     f"Homes: {deal['units']}"]
        if summary["reported_project_cost_millions"] is not None:
            sections += [f"Reported development cost: ${summary['reported_project_cost_millions']}m",
                         f"Reported cost per home: ${summary['reported_cost_per_unit_usd']:,}"]
        else:
            sections += ["Reported development cost: not disclosed in this source"]
        sections += [f"Published monthly rent range: ${deal['rent_range_monthly_usd'][0]:,}–${deal['rent_range_monthly_usd'][1]:,}", "", "| Financing item | Stage | Amount ($m) |", "|---|---|---:|"]
        sections += [f"| {item['label']} | {item['stage'].replace('_', ' ')} | {item['amount_millions']} |" for item in deal["funding"]]
        sections += ["", f"Construction facilities disclosed: ${summary['construction_facilities_millions']}m. Permanent facilities disclosed: ${summary['permanent_facilities_millions']}m.", "", summary["note"], ""]
    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-live", action="store_true")
    parser.add_argument("--output", help="Write Markdown memo to this path")
    args = parser.parse_args()
    deals = load_deals()
    if args.verify_live:
        findings = verify_live(deals)
        print(json.dumps(findings, indent=2))
        if not all(row["all_found"] for row in findings):
            raise SystemExit(2)
    memo = report(deals)
    if args.output:
        Path(args.output).write_text(memo, encoding="utf-8")
    else:
        print(memo)


if __name__ == "__main__":
    main()
