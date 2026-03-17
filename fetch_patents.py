"""
NewSpace Patent Fetcher — Lens.org API
======================================
Fetches patent data for SpaceX, Blue Origin, Rocket Lab, and Virgin Galactic
using the Lens.org Scholarly API (free tier, requires token).

HOW TO GET YOUR FREE TOKEN (takes ~2 minutes):
  1. Go to https://www.lens.org/lens/user/subscriptions#patents
  2. Sign up (free, no credit card)
  3. Go to Account → Lens API
  4. Click "Request Access" for the Patents API
  5. You'll receive a token immediately (or within minutes)
  6. Run:  python fetch_patents.py --token YOUR_TOKEN_HERE
     Or:   set LENS_TOKEN=YOUR_TOKEN_HERE in your shell, then python fetch_patents.py

Output:  data/all_patents.csv  (used by the Streamlit dashboard)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import pandas as pd
import requests

# ── Config ───────────────────────────────────────────────────────────────────

LENS_API_URL = "https://api.lens.org/patent/search"
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Company names → Lens.org assignee search terms
COMPANIES = {
    "SpaceX": [
        "Space Exploration Technologies Corp",
        "SpaceX Technologies",
    ],
    "Blue Origin": [
        "Blue Origin, LLC",
        "Blue Origin LLC",
        "Blue Origin",
    ],
    "Rocket Lab": [
        "Rocket Lab USA, Inc.",
        "Rocket Lab USA",
        "Rocket Lab",
    ],
    "Virgin Galactic": [
        "Virgin Galactic, LLC",
        "Virgin Galactic LLC",
        "Virgin Galactic",
        "The Spaceship Company",
    ],
}

# CPC code prefix → human-readable technology category
CPC_CATEGORIES = [
    ("H04B", "Satellite / Wireless Comms"),
    ("H04W", "Satellite / Wireless Comms"),
    ("H04L", "Satellite / Wireless Comms"),
    ("H04N", "Satellite / Wireless Comms"),
    ("H04", "Satellite / Wireless Comms"),
    ("H01Q", "Antenna Design"),
    ("H01P", "RF / Waveguides"),
    ("H03", "Signal Processing"),
    ("G01S", "Remote Sensing / GPS"),
    ("B64G", "Spacecraft / Launch Systems"),
    ("F02K", "Rocket Propulsion"),
    ("F03H", "Propulsion (Other)"),
    ("B64C", "Aeronautics / Structures"),
    ("G06", "Computing / Software"),
    ("H02", "Power / Electrical Systems"),
    ("F16", "Mechanical Engineering"),
    ("B23", "Manufacturing"),
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


# ── Lens.org API helpers ──────────────────────────────────────────────────────

def build_lens_query(assignee_names: list[str]) -> dict:
    """Build Lens.org query: OR across assignee name variants."""
    terms = [
        {"match_phrase": {"assignee.name": name}}
        for name in assignee_names
    ]
    base_query = {"bool": {"should": terms, "minimum_should_match": 1}}
    return base_query


def fetch_company_patents(company: str, assignee_names: list[str], token: str) -> pd.DataFrame:
    """Page through Lens.org API to fetch all patents for one company."""
    print(f"\n{'='*60}")
    print(f"Fetching: {company}")
    print(f"  Aliases: {assignee_names}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    include_fields = [
        "lens_id",
        "title",
        "publication_type",
        "date_published",
        "filing_date",
        "priority_date",
        "publication_number",
        "application_number",
        "assignee",
        "inventor",
        "abstract",
        "claims",
        "classifications.cpc",
        "legal_status",
        "jurisdiction",
        "families.family_id",
        "families.members",
        "references_cited",
    ]

    all_results = []
    from_offset = 0
    page_size = 100  # Lens.org max per page
    total = None

    while True:
        payload = {
            "query": build_lens_query(assignee_names),
            "include": include_fields,
            "size": page_size,
            "from": from_offset,
            "sort": [{"date_published": "desc"}],
        }

        try:
            resp = requests.post(
                LENS_API_URL,
                headers=headers,
                json=payload,
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")
            break

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 10))
            print(f"  Rate limited — waiting {wait}s...")
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            print(f"  Error {resp.status_code}: {resp.text[:300]}")
            if resp.status_code == 401:
                print("  ► Your token is invalid or expired. Get a new one at lens.org")
            break

        data = resp.json()
        hits = data.get("data", [])
        if total is None:
            total = data.get("total", 0)
            print(f"  Total found: {total}")

        if not hits:
            break

        all_results.extend(hits)
        fetched = len(all_results)
        print(f"  Fetched {fetched}/{total} patents")

        if fetched >= total:
            break

        from_offset += page_size
        time.sleep(0.5)

    print(f"  Done — {len(all_results)} patents for {company}")
    return parse_lens_results(all_results, company)


def parse_lens_results(raw: list, company: str) -> pd.DataFrame:
    """Flatten Lens.org patent records into a tidy DataFrame."""
    rows = []
    for p in raw:
        # Title
        title_raw = p.get("title", [])
        title = title_raw[0].get("text", "") if isinstance(title_raw, list) and title_raw else str(title_raw)

        # Abstract
        abs_raw = p.get("abstract", [])
        abstract = abs_raw[0].get("text", "")[:400] if isinstance(abs_raw, list) and abs_raw else ""

        # Assignee (first / primary)
        assignees = p.get("assignee") or []
        primary_assignee = assignees[0].get("name", "") if assignees else ""

        # Inventors (count)
        inventors = p.get("inventor") or []
        inventor_count = len(inventors)

        # CPC codes
        cpcs_raw = p.get("classifications", {}).get("cpc", []) or []
        cpc_codes = [c.get("symbol", "") for c in cpcs_raw if c.get("symbol")]
        tech_category = classify_cpc(cpc_codes)

        # Dates
        filing_date = p.get("filing_date") or p.get("priority_date") or ""
        pub_date = p.get("date_published") or ""
        filing_year = None
        pub_year = None
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

        # Jurisdiction (from publication_number prefix e.g. US, EP, WO)
        pub_num = p.get("publication_number") or p.get("application_number") or ""
        jurisdiction = pub_num[:2] if pub_num and len(pub_num) >= 2 else "XX"
        if not jurisdiction.isalpha():
            jurisdiction = "XX"

        # Family size
        families = p.get("families") or []
        family_id = families[0].get("family_id", "") if families else ""
        family_size = len(families[0].get("members", [])) if families else 1

        # Legal status
        legal = p.get("legal_status") or {}
        status = "granted" if legal.get("granted") else "pending"
        if legal.get("expired") or legal.get("lapsed"):
            status = "expired/lapsed"

        rows.append({
            "company": company,
            "lens_id": p.get("lens_id", ""),
            "pub_number": pub_num,
            "title": title,
            "abstract": abstract,
            "pub_type": p.get("publication_type", ""),
            "status": status,
            "assignee": primary_assignee,
            "jurisdiction": jurisdiction,
            "filing_date": filing_date,
            "filing_year": filing_year,
            "pub_date": pub_date,
            "pub_year": pub_year,
            "cpc_codes": "|".join(cpc_codes[:8]),
            "tech_category": tech_category,
            "inventor_count": inventor_count,
            "family_id": family_id,
            "family_size": family_size,
        })

    return pd.DataFrame(rows)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch NewSpace patent data from Lens.org",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("LENS_TOKEN", ""),
        help="Lens.org API Bearer token (or set LENS_TOKEN env var)",
    )
    parser.add_argument(
        "--companies",
        nargs="+",
        choices=list(COMPANIES.keys()),
        default=list(COMPANIES.keys()),
        help="Which companies to fetch (default: all)",
    )
    args = parser.parse_args()

    if not args.token:
        print("ERROR: No Lens.org API token provided.")
        print()
        print("Get a free token in ~2 minutes:")
        print("  1. Go to  https://www.lens.org/lens/user/subscriptions#patents")
        print("  2. Sign up (free, no credit card)")
        print("  3. Go to Account → Lens API → Request Access")
        print("  4. Run:  python fetch_patents.py --token YOUR_TOKEN")
        print("     Or:   export LENS_TOKEN=YOUR_TOKEN && python fetch_patents.py")
        sys.exit(1)

    print("NewSpace Patent Fetcher")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fetching data for: {', '.join(args.companies)}")

    all_dfs = []
    for company in args.companies:
        aliases = COMPANIES[company]
        df = fetch_company_patents(company, aliases, args.token)
        if not df.empty:
            path = os.path.join(OUTPUT_DIR, f"{company.replace(' ', '_').lower()}_patents.csv")
            df.to_csv(path, index=False)
            print(f"  Saved → {path}")
            all_dfs.append(df)

    if not all_dfs:
        print("\nNo data fetched. Check your token and connection.")
        sys.exit(1)

    combined = pd.concat(all_dfs, ignore_index=True)
    out_path = os.path.join(OUTPUT_DIR, "all_patents.csv")
    combined.to_csv(out_path, index=False)

    print(f"\n{'='*60}")
    print(f"Combined: {len(combined)} patents → {out_path}")
    print("\nBy company:")
    print(combined.groupby("company")["lens_id"].count().to_string())
    print("\nBy tech category:")
    print(
        combined.groupby("tech_category")["lens_id"]
        .count()
        .sort_values(ascending=False)
        .to_string()
    )
    print(f"\nDone: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nNext step:  streamlit run dashboard.py")


if __name__ == "__main__":
    main()
