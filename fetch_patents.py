#!/usr/bin/env python3
"""
NewSpace Patent Fetcher — USPTO Open Data Portal (ODP)
=======================================================
Fetches granted US patent data for SpaceX, Blue Origin, and seven other
NewSpace companies using the USPTO ODP Patent Applications Search API.

Usage:
    python3 fetch_patents.py                          # fetch all companies
    python3 fetch_patents.py --companies SpaceX       # single company
    python3 fetch_patents.py --dry-run                # print query JSON and exit
    python3 fetch_patents.py --token YOUR_TOKEN       # override default token

Output:
    data/all_patents.csv          (used by the Streamlit dashboard)
    data/patent_families.json     (family-level aggregations)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import pandas as pd
import requests

# ── Config ────────────────────────────────────────────────────────────────────

ODP_URL    = "https://api.uspto.gov/api/v1/patent/applications/search"
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Default API key — override via --token flag or USPTO_TOKEN env var.
_DEFAULT_TOKEN = "tkdpmwsqonraguesssfdnfgflolqqd"

# ODP rate-limit guidance: back off briefly on 429, no required delay otherwise.
_PAGE_SIZE      = 100
_SLEEP_ON_429   = 2.0
_SLEEP_BETWEEN  = 0.15   # courtesy pause between pages

# ── Company name variants ──────────────────────────────────────────────────────

COMPANIES = {
    "SpaceX": [
        "Space Exploration Technologies Corp",
        "Space Exploration Technologies Corporation",
        "SpaceX",
        "Starlink Communications",
    ],
    "Blue Origin": [
        "Blue Origin LLC",
        "Blue Origin, LLC",
        "Blue Origin Federal",
        "Blue Origin",
    ],
    "Rocket Lab": [
        "Rocket Lab USA Inc",
        "Rocket Lab USA, Inc.",
        "Rocket Lab Limited",
        "Rocket Lab",
    ],
    "Virgin Galactic": [
        "Virgin Galactic LLC",
        "Virgin Galactic, LLC",
        "The Spaceship Company",
        "Virgin Galactic Holdings",
        "Virgin Galactic",
    ],
    "Maxar Technologies": [
        "Maxar Technologies",
        "Maxar Technologies Inc",
        "Maxar Technologies Ltd",
        "DigitalGlobe",
        "DigitalGlobe Inc",
        "MDA",
        "MDA Ltd",
        "MDA Space",
    ],
    "Planet Labs": [
        "Planet Labs",
        "Planet Labs PBC",
        "Planet Labs Inc",
    ],
    "Relativity Space": [
        "Relativity Space",
        "Relativity Space Inc",
    ],
    "Astra Space": [
        "Astra Space",
        "Astra Space Inc",
    ],
    "Sierra Nevada / Sierra Space": [
        "Sierra Nevada Corporation",
        "Sierra Space",
        "Sierra Space Corporation",
    ],
}

# ── CPC code prefix -> technology category ─────────────────────────────────────

CPC_CATEGORIES = [
    ("H04B7/195", "Satellite / Wireless Comms"),
    ("H04B7",     "Satellite / Wireless Comms"),
    ("H04W84",    "Satellite / Wireless Comms"),
    ("H04W",      "Satellite / Wireless Comms"),
    ("H04L",      "Satellite / Wireless Comms"),
    ("H04N",      "Satellite / Wireless Comms"),
    ("H04",       "Satellite / Wireless Comms"),
    ("H01Q",      "Antenna Design"),
    ("H01P",      "Signal Processing"),
    ("H03",       "Signal Processing"),
    ("G01S",      "Remote Sensing / GPS"),
    ("B64G1/62",  "Spacecraft / Launch Systems"),
    ("B64G",      "Spacecraft / Launch Systems"),
    ("F02K",      "Rocket Propulsion"),
    ("F03H",      "Rocket Propulsion"),
    ("F04D",      "Rocket Propulsion"),
    ("B64C",      "Aeronautics / Structures"),
    ("G06",       "Computing / Software"),
    ("H02",       "Power / Electrical Systems"),
    ("F16",       "Mechanical Engineering"),
    ("B22F",      "Manufacturing"),
    ("B23",       "Manufacturing"),
    ("F17",       "Spacecraft / Launch Systems"),
]


def classify_cpc(cpc_codes: list[str]) -> str:
    """Map a list of CPC codes to a single human-readable category."""
    if not cpc_codes:
        return "Other"
    for code in cpc_codes:
        for prefix, label in CPC_CATEGORIES:
            if code.startswith(prefix):
                return label
    return "Other"


# ── ODP API helpers ────────────────────────────────────────────────────────────

def build_query(assignee_names: list[str]) -> str:
    """
    Build an OpenSearch Lucene query string matching any of the given
    applicant name variants against the applicantBag.applicantNameText field.
    """
    terms = " OR ".join(f'"{name}"' for name in assignee_names)
    return f"applicationMetaData.applicantBag.applicantNameText:({terms})"


def fetch_company_patents(company: str, assignee_names: list[str], token: str) -> pd.DataFrame:
    """Fetch all granted patents for one company using offset pagination."""
    print(f"\n{'='*60}")
    print(f"Fetching: {company}")
    print(f"  Aliases: {', '.join(assignee_names)}")

    headers = {
        "x-api-key": token,
        "Content-Type": "application/json",
    }

    base_payload: dict = {
        "q": build_query(assignee_names),
        "filters": [
            {
                "name": "applicationMetaData.publicationCategoryBag",
                "value": ["Granted/Issued"],
            }
        ],
        "sort": [{"field": "applicationMetaData.filingDate", "order": "Desc"}],
        "fields": ["applicationNumberText", "applicationMetaData"],
    }

    all_results: list[dict] = []
    offset  = 0
    total   = None
    retries = 0
    t_start = time.time()

    while True:
        payload = {
            **base_payload,
            "pagination": {"offset": offset, "limit": _PAGE_SIZE},
        }

        try:
            resp = requests.post(ODP_URL, headers=headers, json=payload, timeout=60)
        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")
            break

        if resp.status_code == 429:
            print(f"  Rate limited — waiting {_SLEEP_ON_429}s ...")
            time.sleep(_SLEEP_ON_429)
            continue

        if resp.status_code == 404:
            # ODP returns 404 when the page has no results (end of set)
            break

        if resp.status_code not in (200, 201):
            print(f"  Error {resp.status_code}: {resp.text[:400]}")
            retries += 1
            if retries >= 3:
                print("  Max retries reached, moving on.")
                break
            time.sleep(5 * retries)
            continue

        retries = 0
        data = resp.json()
        hits = data.get("patentFileWrapperDataBag") or []

        if total is None:
            # ODP doesn't return total_hits reliably; track via empty page
            total = data.get("count", 0)
            print(f"  First-page count: {total}")

        if not hits:
            break

        all_results.extend(hits)
        print(f"  Fetched {len(all_results):,}  (page offset {offset})")

        if len(hits) < _PAGE_SIZE:
            # Last page — fewer results than requested means we're done
            break

        offset += _PAGE_SIZE
        time.sleep(_SLEEP_BETWEEN)

    elapsed = time.time() - t_start
    print(f"  Done — {len(all_results):,} records in {elapsed:.1f}s")
    return parse_odp_results(all_results, company)


def _clean_cpc(raw: str) -> str:
    """Remove internal whitespace from ODP CPC strings like 'H04N  23/90'."""
    parts = raw.strip().split()
    return "".join(parts)


def parse_odp_results(raw: list[dict], company: str) -> pd.DataFrame:
    """Flatten USPTO ODP patent records into a tidy DataFrame."""
    rows = []
    for item in raw:
        app_num = item.get("applicationNumberText") or ""
        meta    = item.get("applicationMetaData") or {}

        title       = meta.get("inventionTitle") or ""
        filing_date = meta.get("filingDate") or meta.get("effectiveFilingDate") or ""
        grant_date  = meta.get("grantDate") or ""
        patent_num  = str(meta.get("patentNumber") or "").strip()
        status_desc = meta.get("applicationStatusDescriptionText") or ""

        # Applicant / assignee
        applicant_bag    = meta.get("applicantBag") or []
        primary_assignee = applicant_bag[0].get("applicantNameText", "") if applicant_bag else ""

        # Inventors
        inventor_bag   = meta.get("inventorBag") or []
        inventor_names = "; ".join(
            i.get("inventorNameText") or f"{i.get('firstName','')} {i.get('lastName','')}".strip()
            for i in inventor_bag[:10]
            if i.get("inventorNameText") or i.get("lastName")
        )
        inventor_count = len(inventor_bag)

        # CPC codes — strip extra whitespace from ODP format ("H04N  23/90" → "H04N23/90")
        cpc_raw   = meta.get("cpcClassificationBag") or []
        cpc_codes = [_clean_cpc(c) for c in cpc_raw if c.strip()]
        tech_cat  = classify_cpc(cpc_codes)

        # Dates
        pub_date = grant_date or filing_date
        filing_year = pub_year = None
        try:
            if filing_date:
                filing_year = int(str(filing_date)[:4])
        except (ValueError, TypeError):
            pass
        try:
            if pub_date:
                pub_year = int(str(pub_date)[:4])
        except (ValueError, TypeError):
            pass

        # Status
        status_lower = status_desc.lower()
        if "patent" in status_lower or "grant" in status_lower:
            status = "granted"
        elif "abandon" in status_lower or "expire" in status_lower or "lapse" in status_lower:
            status = "expired/lapsed"
        else:
            status = "granted"  # all results are Granted/Issued filtered

        rows.append({
            "company":        company,
            "lens_id":        app_num,
            "pub_number":     f"US{patent_num}" if patent_num else "",
            "title":          title,
            "abstract":       "",   # not available in ODP metadata search
            "pub_type":       "grant",
            "status":         status,
            "assignee":       primary_assignee,
            "jurisdiction":   "US",
            "filing_date":    filing_date,
            "filing_year":    filing_year,
            "pub_date":       pub_date,
            "pub_year":       pub_year,
            "cpc_codes":      "|".join(cpc_codes[:8]),
            "tech_category":  tech_cat,
            "inventor_count": inventor_count,
            "family_id":      "",
            "family_size":    1,
            "priority_date":  meta.get("effectiveFilingDate") or "",
            "grant_date":     grant_date,
            "expiration_date": "",
            "inventors":      inventor_names,
            "claims_count":   0,
            "cited_by_count": 0,
        })

    return pd.DataFrame(rows)


def save_family_summary(df: pd.DataFrame) -> None:
    """Write a family-level aggregation JSON for optional dashboard use."""
    if df.empty or "family_id" not in df.columns:
        return
    fam = (
        df[df["family_id"].notna() & (df["family_id"] != "")]
        .groupby("family_id")
        .agg(
            company=("company",       "first"),
            size=   ("lens_id",       "count"),
            tech=   ("tech_category", "first"),
            filed=  ("filing_date",   "min"),
        )
        .reset_index()
        .rename(columns={"filed": "earliest_filing"})
        .to_dict(orient="records")
    )
    path = os.path.join(OUTPUT_DIR, "patent_families.json")
    with open(path, "w") as f:
        json.dump(fam, f, indent=2)
    print(f"  Family summary: {len(fam)} families -> {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch NewSpace patent data from USPTO Open Data Portal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("USPTO_TOKEN", _DEFAULT_TOKEN),
        help="USPTO ODP API key (or set USPTO_TOKEN env var)",
    )
    parser.add_argument(
        "--companies",
        nargs="+",
        choices=list(COMPANIES.keys()),
        default=list(COMPANIES.keys()),
        help="Companies to fetch (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        default=OUTPUT_DIR,
        help="Directory for CSV output (default: data/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print query string for each company and exit without calling the API",
    )
    args = parser.parse_args()

    if not args.token:
        print("ERROR: No API token provided.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    if args.dry_run:
        print("DRY RUN — queries only, no API calls\n")
        for company in args.companies:
            q = build_query(COMPANIES[company])
            print(f"--- {company} ---")
            print(q)
            print()
        return

    print("NewSpace Patent Fetcher  (USPTO Open Data Portal)")
    print(f"Started:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Companies: {', '.join(args.companies)}")
    t0 = time.time()

    all_dfs = []
    for company in args.companies:
        df = fetch_company_patents(company, COMPANIES[company], args.token)
        if not df.empty:
            slug = company.replace(" ", "_").replace("/", "-").lower()
            path = os.path.join(args.output_dir, f"{slug}_patents.csv")
            df.to_csv(path, index=False)
            print(f"  Saved -> {path}")
            all_dfs.append(df)

    if not all_dfs:
        print("\nNo data fetched. Check your token and network connection.")
        sys.exit(1)

    combined = pd.concat(all_dfs, ignore_index=True)

    # Deduplicate by application number
    before   = len(combined)
    combined = combined.drop_duplicates(subset=["lens_id"], keep="first")
    after    = len(combined)
    if before != after:
        print(f"\nDeduplication: removed {before - after:,} duplicate application numbers")

    out_path = os.path.join(args.output_dir, "all_patents.csv")
    combined.to_csv(out_path, index=False)
    save_family_summary(combined)

    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"Total: {len(combined):,} patents -> {out_path}")
    print(f"Elapsed: {elapsed/60:.1f} min")
    print("\nBy company:")
    print(combined.groupby("company")["lens_id"].count().sort_values(ascending=False).to_string())
    print("\nBy technology category:")
    print(
        combined.groupby("tech_category")["lens_id"]
        .count()
        .sort_values(ascending=False)
        .to_string()
    )
    print(f"\nDone: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nNext:  streamlit run dashboard.py")


if __name__ == "__main__":
    main()
