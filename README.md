# NewSpace Patent Analytics Dashboard

Patent intelligence dashboard comparing SpaceX, Blue Origin, Rocket Lab, and Virgin Galactic.
Built for Perkins Coie NewSpace practice demo.

---

## Quick Start (demo mode — no token needed)

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

Opens at **http://localhost:8501** with illustrative sample data immediately.

---

## Step 1 — Get Your Free Lens.org API Token (~2 minutes)

1. Go to **https://www.lens.org** → click **Sign Up** (free, no credit card)
2. After signing in, go to **Account → Subscriptions → Lens API**
3. Click **Request Access** under "Patent API"
4. Your token appears immediately on the same page — copy it

---

## Step 2 — Fetch Real Patent Data

```bash
# Option A: pass token directly
python fetch_patents.py --token YOUR_TOKEN_HERE

# Option B: set as environment variable
export LENS_TOKEN=YOUR_TOKEN_HERE
python fetch_patents.py

# Fetch only specific companies
python fetch_patents.py --token YOUR_TOKEN --companies SpaceX "Blue Origin"
```

This writes `data/all_patents.csv`. Typical run time: 1–2 minutes for all four companies.

---

## Step 3 — Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard auto-detects `data/all_patents.csv` and switches from demo to live data.

---

## What the Dashboard Shows

| Panel | Description |
|-------|-------------|
| **A — Filing Timeline** | Annual filings by company, SpaceX tech area breakdown, cumulative growth |
| **B — Technology Breakdown** | Treemap + bar chart by CPC category — SpaceX's Starlink dominance is obvious |
| **C — Competitor Landscape** | Volume comparison, normalised tech mix, jurisdiction breakdown, radar chart |
| **D — Patent Family Tree** | Interactive network graph of continuations, divisionals, PCT filings |

---

## Files

```
.
├── fetch_patents.py    # Lens.org API fetcher (run this first)
├── dashboard.py        # Streamlit dashboard
├── seed_data.py        # Sample data for demo mode
├── requirements.txt    # Python dependencies
└── data/
    └── all_patents.csv # Written by fetch_patents.py
```

---

## Stack

- **Data**: [Lens.org Patent API](https://www.lens.org/lens/user/subscriptions#patents) (free)
- **Dashboard**: Streamlit
- **Charts**: Plotly
- **Network graph**: NetworkX + PyVis
- **Processing**: Pandas
