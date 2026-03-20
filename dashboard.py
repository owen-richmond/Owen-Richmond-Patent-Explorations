"""
NewSpace Patent Analytics Dashboard
Perkins Coie — Interview Demo

Run:  streamlit run dashboard.py
"""

import os
import warnings
from collections import defaultdict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewSpace Patent Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
}
.stApp { background-color: #f7f8fa; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e3e6ea;
}

/* Main title */
h1 {
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    color: #0d1117 !important;
    letter-spacing: -0.4px !important;
    margin-bottom: 0 !important;
}

/* Section headers generated via st.subheader */
h3 { color: #0d1117 !important; font-weight: 600 !important; font-size: 1.05rem !important; }

/* Narrative blockquote */
blockquote {
    border-left: 3px solid #005288;
    padding: 0.65rem 1.1rem;
    background: #f0f4f8;
    border-radius: 0 4px 4px 0;
    margin: 0.6rem 0 1.1rem;
}
blockquote p { color: #1a2b42; font-size: 0.92rem; line-height: 1.65; margin: 0; }

/* KPI cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e3e6ea;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
[data-testid="metric-container"] label {
    color: #6b7280 !important;
    font-size: 0.73rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: #0d1117 !important;
}

/* Section label pill */
.sec-pill {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    color: #005288;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    border: 1px solid #c5d8ea;
    background: #eef4fb;
    border-radius: 4px;
    padding: 2px 8px;
    margin-bottom: 8px;
}
.sec-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0d1117;
    margin: 0 0 6px 0;
    padding: 0;
    line-height: 1.3;
}
.sec-sub {
    font-size: 0.84rem;
    color: #6b7280;
    line-height: 1.6;
    margin: 0 0 1.1rem 0;
    padding: 0;
}
/* Prevent Streamlit's default p-tag margin from fighting custom elements */
[data-testid="stMarkdownContainer"] .sec-title,
[data-testid="stMarkdownContainer"] .sec-sub {
    margin-bottom: 6px !important;
}

/* Horizontal rule */
hr { border: none; border-top: 1px solid #e3e6ea; margin: 1.6rem 0; }

/* Expander */
details {
    border: 1px solid #e3e6ea !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* Dataframe */
.stDataFrame { border: 1px solid #e3e6ea; border-radius: 6px; }

/* Footer */
.footer {
    font-size: 0.73rem;
    color: #9ca3af;
    text-align: center;
    padding: 1.2rem 0 0.4rem;
    border-top: 1px solid #e3e6ea;
    margin-top: 1rem;
}

/* IPR node highlight */
.ipr-note {
    font-size: 0.8rem;
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 5px;
    padding: 0.5rem 0.85rem;
    margin-top: 0.4rem;
    color: #5a4000;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────────────────────────────────────
COMPANY_COLORS = {
    "SpaceX":                       "#005288",
    "Blue Origin":                  "#2d3748",
    "Rocket Lab":                   "#c0392b",
    "Virgin Galactic":              "#0077aa",
    "Maxar Technologies":           "#6b7280",
    "Planet Labs":                  "#16a34a",
    "Relativity Space":             "#7c3aed",
    "Astra Space":                  "#d97706",
    "Sierra Nevada / Sierra Space": "#0891b2",
}

FILING_TYPE_COLORS = {
    "Priority Application":  "#005288",
    "PCT Application":       "#2e7d32",
    "Continuation":          "#6a1b9a",
    "Continuation-in-Part":  "#ad1457",
    "Divisional":            "#e65100",
    "EP National Phase":     "#0077aa",
    "JP National Phase":     "#b71c1c",
    "CN National Phase":     "#c62828",
    "CA National Phase":     "#1565c0",
    "AU National Phase":     "#00695c",
    "IPR Challenge":         "#b71c1c",
}

STATUS_SYMBOLS = {
    "granted":        "circle",
    "pending":        "diamond",
    "denied":         "x",
    "expired/lapsed": "triangle-down",
    "contested":      "star",
}

TIER_Y = {
    "Priority Application":  5,
    "Continuation":          4,
    "Continuation-in-Part":  4,
    "Divisional":            3,
    "PCT Application":       2,
    "EP National Phase":     1,
    "JP National Phase":     1,
    "CN National Phase":     1,
    "CA National Phase":     1,
    "AU National Phase":     1,
    "IPR Challenge":         0,
}

TIER_LABELS = {
    5: "Priority",
    4: "Continuations / CIPs",
    3: "Divisionals",
    2: "PCT",
    1: "National Phase",
    0: "PTAB / IPR",
}

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Inter, Helvetica Neue, Arial, sans-serif",
    font_color="#1a2b42",
    title_font_size=13,
    title_font_color="#0d1117",
    hoverlabel=dict(bgcolor="#ffffff", font_size=12, bordercolor="#e3e6ea"),
    margin=dict(l=8, r=8, t=38, b=8),
)
LEGEND_CLEAN = dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font_size=11)
LEGEND_H = dict(bgcolor="rgba(0,0,0,0)", orientation="h",
                yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=10)

AXIS = dict(gridcolor="#f0f0f0", linecolor="#e3e6ea", tickcolor="#e3e6ea")


def chart_height(n: int, base: int = 280, per_row: int = 16, cap: int = 560) -> int:
    """Scale chart height with data volume, within a sensible range."""
    return min(base + n * per_row, cap)


def _layout(fig: go.Figure, **kwargs) -> None:
    """Apply CHART_BASE defaults merged with chart-specific overrides."""
    fig.update_layout(**{**CHART_BASE, **kwargs})  # type: ignore[call-arg]


def sec(pill: str, title: str, sub: str):
    st.markdown(
        f'<div style="margin-top:0.5rem;">'
        f'<span class="sec-pill">{pill}</span><br>'
        f'<div class="sec-title">{title}</div>'
        f'<div class="sec-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def gp_url(pub_number: str) -> str:
    """Google Patents URL for a publication number."""
    clean = pub_number.replace(" ", "").replace("/", "")
    return f"https://patents.google.com/patent/{clean}/en"


# ─────────────────────────────────────────────────────────────────────────────
#  Data loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> tuple[pd.DataFrame, bool]:
    real = "data/all_patents.csv"
    if os.path.exists(real):
        return pd.read_csv(real), False
    from seed_data import get_sample_data
    return get_sample_data(), True


df_raw, is_sample = load_data()

# ─────────────────────────────────────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    if is_sample:
        st.caption("Illustrative data — run `python fetch_patents.py` to load live records")
    else:
        st.success(f"Live: **{len(df_raw):,}** patents loaded")

    st.markdown("---")
    all_co = sorted(df_raw["company"].unique())
    sel_co = st.multiselect("Companies", all_co, default=all_co)

    ymin = int(df_raw["filing_year"].dropna().min())
    ymax = int(df_raw["filing_year"].dropna().max())
    yr = st.slider("Filing year range", ymin, ymax, (ymin, ymax))

    all_cat = sorted(df_raw["tech_category"].dropna().unique())
    sel_cat = st.multiselect("Technology categories", all_cat, default=all_cat)

    st.markdown("---")
    st.caption("Data: USPTO Open Data Portal")

# ─────────────────────────────────────────────────────────────────────────────
#  Filtered dataframe
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["company"].isin(sel_co)
    & (df_raw["filing_year"] >= yr[0])
    & (df_raw["filing_year"] <= yr[1])
    & df_raw["tech_category"].isin(sel_cat)
].copy()

# ─────────────────────────────────────────────────────────────────────────────
#  Header
# ─────────────────────────────────────────────────────────────────────────────
st.title("NewSpace Patent Analytics")
st.markdown("""
<blockquote><p>
I built this to examine how NewSpace companies structure their IP portfolios, using data from the USPTO API. The pattern that
emerges is counterintuitive: SpaceX's granted patent activity concentrates almost entirely in
satellite communications and RF systems, while launch vehicle technology is protected as trade
secrets. Portfolio strategy, prosecution decisions, and FTO analysis in this space require the
kind of technical depth and sectoral fluency that drew me to Perkins Coie.
</p></blockquote>
""", unsafe_allow_html=True)

if is_sample:
    st.info(
        "Showing illustrative sample data across nine NewSpace companies. "
        "Run `python3 fetch_patents.py` to populate with live records from the USPTO.",
        icon="ℹ️",
    )

# KPIs
granted = df[df["status"] == "granted"]
sx_post19 = df[(df["company"] == "SpaceX") & (df["filing_year"] >= 2019)]["lens_id"].nunique()

_yr_min = int(df["pub_year"].dropna().min()) if not df["pub_year"].dropna().empty else 0
_yr_max = int(df["pub_year"].dropna().max()) if not df["pub_year"].dropna().empty else 0
_top_cat = df["tech_category"].value_counts().idxmax() if not df.empty else "N/A"

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Patents", f"{len(df):,}")
k2.metric("Companies Tracked", len(df["company"].unique()))
k3.metric("Technology Areas", df["tech_category"].nunique())
k4.metric("SpaceX Post-2019", sx_post19, delta="Starlink era")
k5.metric("Grant Years", f"{_yr_min}-{_yr_max}", delta=_top_cat)

_sx_recent = df[(df["company"] == "SpaceX") & (df["filing_year"] >= 2023)]["lens_id"].nunique()

st.markdown(
    f'<div style="background:#fff8e1;border-left:3px solid #f59e0b;border-radius:0 4px 4px 0;'
    f'padding:0.6rem 1rem;margin:0.8rem 0 1rem;font-size:0.88rem;color:#1a2b42;line-height:1.6;">'
    f'SpaceX filed only {_sx_recent} patents since 2023, a sharp decline from prior years. '
    f'This reflects a deliberate shift toward trade secret protection for core technology, '
    f'including Raptor engine design, Starship manufacturing processes, and materials science. '
    f'For clients operating adjacent to SpaceX technology, that opacity creates sustained demand '
    f'for FTO analysis and clearance opinions, precisely because portfolio boundaries are '
    f'difficult to map from the public record alone. It is also an opportunity for third parties '
    f'to entrench themselves against competitors, even where SpaceX holds prior use rights.'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 1 — Patent Family Prosecution History  (moved to top)
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 1",
    "Patent Family Prosecution History",
    "A patent family encompasses every filing derived from a common priority: domestic "
    "continuations, divisionals, PCT applications, and national phase entries across key "
    "jurisdictions. I selected these families to illustrate the scope of prosecution "
    "management that firms like Perkins Coie coordinate on behalf of clients in this sector. "
    "Hover any node for filing details, or follow the table links to the source record.",
)

from seed_data import get_all_families
all_families = get_all_families()

sel_family_label = st.selectbox(
    "Select patent family",
    options=list(all_families.keys()),
    label_visibility="collapsed",
)
family_data = all_families[sel_family_label]
_label_str = sel_family_label or ""
is_ipr_family = any(kw in _label_str for kw in ("IPR", "VTOL", "Challenge"))

if is_ipr_family:
    st.markdown(
        '<p class="ipr-note">SpaceX filed IPR2015-01765 at the PTAB challenging Blue Origin\'s '
        'US8678321B2 reusable vertical landing claims. The PTAB denied institution in April 2016, '
        'finding SpaceX had not demonstrated a reasonable likelihood of prevailing on any '
        'challenged claim. The proceeding illustrates how inter partes review functions as a '
        'competitive tool in capital-intensive industries where rival firms hold overlapping '
        'technical positions.</p>',
        unsafe_allow_html=True,
    )

# ── Build positions ───────────────────────────────────────────────────────────
pos_counter = defaultdict(int)
node_pos = {}
for rec in family_data:
    tier = TIER_Y.get(rec["filing_type"], 0)
    key = (rec["filing_year"], tier)
    offset = pos_counter[key] * 1.0   # wider spacing to prevent label collisions
    pos_counter[key] += 1
    node_pos[rec["node_id"]] = (rec["filing_year"] + offset, tier)

all_x = [v[0] for v in node_pos.values()]
x_min, x_max = min(all_x) - 0.5, max(all_x) + 1.5

# ── Edges ─────────────────────────────────────────────────────────────────────
edge_x, edge_y, edge_annots = [], [], []
for rec in family_data:
    if not rec["parent_id"] or rec["parent_id"] not in node_pos:
        continue
    px_, py_ = node_pos[rec["parent_id"]]
    cx, cy = node_pos[rec["node_id"]]
    # Elbow: go to child X at parent Y, then drop to child Y
    edge_x += [px_, cx, cx, None]
    edge_y += [py_, py_, cy, None]
    if rec.get("relationship"):
        mid_x = (px_ + cx) / 2
        mid_y = py_ + 0.12
        edge_annots.append(dict(
            x=mid_x, y=mid_y, text=rec["relationship"],
            xanchor="center", yanchor="bottom",
            font=dict(size=8, color="#6b7280"),
            showarrow=False,
            bgcolor="rgba(247,248,250,0.88)",
        ))

# ── Node traces (one per filing type for legend) ──────────────────────────────
traces = [go.Scatter(
    x=edge_x, y=edge_y, mode="lines",
    line=dict(color="#c0cdd8", width=1.5, dash="solid"),
    hoverinfo="none", showlegend=False, name="",
)]

type_groups: dict[str, list] = defaultdict(list)
for rec in family_data:
    type_groups[rec["filing_type"]].append(rec)

for ftype, recs in type_groups.items():
    xs = [node_pos[r["node_id"]][0] for r in recs]
    ys = [node_pos[r["node_id"]][1] for r in recs]
    sz = [26 if r["filing_type"] == "Priority Application" else
          20 if r["filing_type"] == "IPR Challenge" else 17 for r in recs]
    col = FILING_TYPE_COLORS.get(ftype, "#888888")
    syms = [STATUS_SYMBOLS.get(r["status"], "circle") for r in recs]

    hover_texts = []
    for r in recs:
        grant_line = f"Grant date: {r['grant_date']}" if r.get("grant_date") else "Status: pending / active"
        hover_texts.append(
            f"<b>{r['pub_number']}</b><br>"
            f"{r['title'][:80]}{'...' if len(r['title']) > 80 else ''}<br><br>"
            f"Type: {r['filing_type']}<br>"
            f"Jurisdiction: {r['jurisdiction']}<br>"
            f"Filed: {r['filing_date']}<br>"
            f"{grant_line}<br>"
            f"Claims: {r['claims_count']}<br>"
            f"CPC: {r['cpc_codes'].split('|')[0] if r['cpc_codes'] else 'N/A'}<br><br>"
            f"{r['abstract'][:180]}..."
        )

    traces.append(go.Scatter(
        x=xs, y=ys,
        mode="markers",
        marker=dict(symbol=syms, color=col, size=sz, line=dict(color="#ffffff", width=2)),
        customdata=hover_texts,
        hovertemplate="%{customdata}<extra></extra>",
        name=ftype,
        legendgroup=ftype,
    ))

# ── Node label annotations (alternating above/below to prevent overlap) ───────
label_annots = []
for i, rec in enumerate(family_data):
    x, y = node_pos[rec["node_id"]]
    short = (rec["pub_number"]
             .replace("B2", "").replace("B1", "").replace("A1", "").replace("A2", "")
             .strip())
    if short.startswith("US"):
        short = short[2:]          # drop "US" prefix — saves ~30% label width
    if "IPR" in rec["pub_number"]:
        short = "IPR\n01765"
    # Size-aware yshift: priority nodes are bigger so need more clearance
    is_priority = rec["filing_type"] == "Priority Application"
    shift_px = 30 if is_priority else 14
    above = (i % 2 == 0)
    label_annots.append(dict(
        x=x, y=y,
        text=short,
        yshift=shift_px if above else -shift_px,
        xanchor="center",
        yanchor="bottom" if above else "top",
        font=dict(size=7.5, color="#2c3e50"),
        showarrow=False,
        bgcolor="rgba(247,248,250,0.75)",
    ))

# ── Tier band annotations ─────────────────────────────────────────────────────
tier_annots = [
    dict(x=x_min + 0.1, y=t, text=f"<b>{lbl}</b>",
         xanchor="left", yanchor="middle",
         font=dict(size=9, color="#9ca3af"),
         showarrow=False)
    for t, lbl in TIER_LABELS.items()
    if any(TIER_Y.get(r["filing_type"], -1) == t for r in family_data)
]

fig_fam = go.Figure(data=traces)

# Background bands only for tiers present in this family
active_tiers = {TIER_Y.get(r["filing_type"], 0) for r in family_data}
for tier in active_tiers:
    fig_fam.add_shape(
        type="rect", layer="below",
        x0=x_min, x1=x_max,
        y0=tier - 0.48, y1=tier + 0.48,
        fillcolor="#f7f8fa" if tier % 2 == 1 else "#eef2f7",
        line_width=0,
    )

_fam_title = "Prosecution History: " + (
    _label_str.split("|")[1].strip() if "|" in _label_str else _label_str
)
_layout(fig_fam,
    plot_bgcolor="#ffffff",
    height=560,
    xaxis=dict(title="Filing Year", tickmode="linear", dtick=1,
               range=[x_min, x_max], **AXIS),
    yaxis=dict(showticklabels=False, range=[-0.6, 5.7],
               gridcolor="#f0f4f8", zeroline=False),
    legend=dict(title="Filing Type", bgcolor="rgba(255,255,255,0.92)",
                bordercolor="#e3e6ea", borderwidth=1, font_size=10),
    annotations=tier_annots + edge_annots + label_annots,
    margin=dict(l=90, r=16, t=44, b=36),
    hovermode="closest",
    title=dict(text=_fam_title, font_size=13, x=0),
)

st.plotly_chart(fig_fam, width="stretch")

# ── Summary KPIs + table with source links ────────────────────────────────────
fam_df = pd.DataFrame(family_data)
non_ipr = fam_df[fam_df["filing_type"] != "IPR Challenge"]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Family Members", len(non_ipr))
m2.metric("Jurisdictions", non_ipr["jurisdiction"].nunique())
m3.metric("Granted", len(non_ipr[non_ipr["status"] == "granted"]))
m4.metric("Total Claims", int(non_ipr["claims_count"].sum()))

# Build display table with a Google Patents link column
fam_display = fam_df[[
    "pub_number", "jurisdiction", "filing_type", "relationship",
    "filing_date", "status", "claims_count", "title",
]].copy()
fam_display["source"] = fam_display["pub_number"].apply(
    lambda p: gp_url(p) if p and "/" not in p and "IPR" not in p else ""
)
fam_display = fam_display.sort_values("filing_date").rename(columns={
    "pub_number":   "Publication No.",
    "jurisdiction": "Jur.",
    "filing_type":  "Filing Type",
    "relationship": "Relationship",
    "filing_date":  "Filed",
    "status":       "Status",
    "claims_count": "Claims",
    "title":        "Title",
    "source":       "Google Patents",
})

st.dataframe(
    fam_display,
    width="stretch",
    hide_index=True,
    column_config={
        "Google Patents": st.column_config.LinkColumn(
            "Google Patents", display_text="View"
        ),
        "Title": st.column_config.TextColumn("Title", width="large"),
        "Claims": st.column_config.NumberColumn("Claims", width="small"),
        "Jur.": st.column_config.TextColumn("Jur.", width="small"),
    },
)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 2 — Filing Timeline
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 2",
    "Filing Timeline",
    "SpaceX's filing activity was negligible before 2016. The volume that followed correlates "
    "directly with Starlink development, and CPC classification confirms it is concentrated in "
    "communications technology rather than launch systems. The divergence between public identity "
    "and actual portfolio composition is the defining IP strategy question in NewSpace.",
)

tl = df.groupby(["filing_year", "company"])["lens_id"].count().reset_index(name="count")

fig_tl = px.bar(
    tl, x="filing_year", y="count", color="company",
    color_discrete_map=COMPANY_COLORS, barmode="group",
    labels={"filing_year": "Filing Year", "count": "Patents Filed", "company": ""},
    title="Annual Patent Filings by Company",
)
_tl_h = chart_height(tl["filing_year"].nunique(), base=320, per_row=4, cap=460)
_layout(fig_tl, height=_tl_h,
        xaxis=dict(tickmode="linear", dtick=1, tickangle=-45, automargin=True, **AXIS),
        yaxis=dict(**AXIS), legend=LEGEND_H,
        margin=dict(l=8, r=8, t=64, b=44))
st.plotly_chart(fig_tl, width="stretch")

ca1, ca2 = st.columns(2)
with ca1:
    sx = df[df["company"] == "SpaceX"]
    sx_tl = sx.groupby(["filing_year", "tech_category"])["lens_id"].count().reset_index(name="n")
    fig_sx = px.area(
        sx_tl, x="filing_year", y="n", color="tech_category",
        title="SpaceX: Technology Area Over Time",
        labels={"filing_year": "Year", "n": "Filings", "tech_category": ""},
    )
    _layout(fig_sx, height=310,
            legend=dict(bgcolor="rgba(255,255,255,0.88)", bordercolor="#e3e6ea",
                        borderwidth=1, font_size=8, x=0.01, y=0.99,
                        xanchor="left", yanchor="top"),
            xaxis=dict(tickangle=-45, automargin=True, **AXIS),
            yaxis=dict(**AXIS),
            margin=dict(l=8, r=8, t=46, b=44))
    st.plotly_chart(fig_sx, width="stretch")

with ca2:
    cum = (df.groupby(["filing_year", "company"])["lens_id"]
           .count().reset_index(name="n").sort_values("filing_year"))
    cum["cumulative"] = cum.groupby("company")["n"].cumsum()
    fig_cum = px.line(
        cum, x="filing_year", y="cumulative", color="company",
        color_discrete_map=COMPANY_COLORS,
        title="Cumulative Portfolio Growth",
        labels={"filing_year": "Year", "cumulative": "Total Patents", "company": ""},
    )
    _layout(fig_cum, height=310,
            legend=dict(bgcolor="rgba(255,255,255,0.88)", bordercolor="#e3e6ea",
                        borderwidth=1, font_size=8, x=0.01, y=0.99,
                        xanchor="left", yanchor="top"),
            xaxis=dict(tickangle=-45, **AXIS), yaxis=dict(**AXIS),
            margin=dict(l=8, r=8, t=46, b=44))
    st.plotly_chart(fig_cum, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 3 — Technology Breakdown
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 3",
    "Technology Breakdown",
    "Computing, software, and satellite communications account for the majority of granted "
    "patents across this sector. Propulsion represents a small fraction despite being the most "
    "visible aspect of SpaceX's operations, consistent with a deliberate trade-secret posture "
    "for launch vehicle technology. That choice concentrates prosecution and enforcement activity "
    "on the communications and software portfolio.",
)

cb1, cb2 = st.columns([1.1, 0.9])
with cb1:
    tech_comp = df.groupby(["company", "tech_category"])["lens_id"].count().reset_index(name="n")
    fig_tm = px.treemap(
        tech_comp, path=["company", "tech_category"], values="n",
        color="company", color_discrete_map=COMPANY_COLORS,
        title="Portfolio Composition by Company and Technology",
    )
    fig_tm.update_traces(
        textinfo="label+value",
        hovertemplate="<b>%{label}</b><br>%{value} patents<extra></extra>",
        textfont=dict(size=13),
        marker=dict(line=dict(width=0.8, color="#333333")),
    )
    fig_tm.update_layout(uniformtext=dict(minsize=8, mode="hide"))
    _layout(fig_tm, height=460, margin=dict(l=4, r=4, t=52, b=4))
    st.plotly_chart(fig_tm, width="stretch")

with cb2:
    sx_tech = (df[df["company"] == "SpaceX"]
               .groupby("tech_category")["lens_id"].count()
               .sort_values().reset_index(name="n"))
    # Truncate long category names for axis legibility
    sx_tech["cat_short"] = sx_tech["tech_category"].str.replace(" / ", "/")
    fig_sb = px.bar(
        sx_tech, x="n", y="cat_short", orientation="h",
        title="SpaceX: Technology Distribution",
        labels={"n": "Patents", "cat_short": ""},
        color="n", color_continuous_scale="Blues",
    )
    _sb_h = chart_height(len(sx_tech), base=320, per_row=28, cap=560)
    _layout(fig_sb, height=_sb_h, showlegend=False, coloraxis_showscale=False,
            xaxis=dict(**AXIS), yaxis=dict(**AXIS),
            margin=dict(l=160, r=8, t=52, b=8))
    st.plotly_chart(fig_sb, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 4 — Competitor Landscape
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 4",
    "Competitor Landscape",
    "Each company reflects a distinct IP posture. SpaceX concentrates in communications "
    "infrastructure, Blue Origin in propulsion systems, and Maxar reflects the deeper patent "
    "culture of the established Earth observation sector. Rocket Lab, Relativity, and Sierra "
    "Space represent the more dynamic prosecution and FTO opportunity as their portfolios "
    "mature and their technology positions become commercially contested.",
)

cc1, cc2 = st.columns(2)

with cc1:
    vol = df.groupby("company")["lens_id"].count().reset_index(name="n")
    fig_vol = px.bar(
        vol.sort_values("n"), x="n", y="company", orientation="h",
        color="company", color_discrete_map=COMPANY_COLORS,
        title="Patent Volume by Company",
        labels={"n": "Total Patents", "company": ""},
    )
    _vol_h = chart_height(len(vol), base=220, per_row=32, cap=480)
    _layout(fig_vol, showlegend=False, height=_vol_h,
            xaxis=dict(**AXIS), yaxis=dict(**AXIS),
            margin=dict(l=120, r=8, t=52, b=8))
    st.plotly_chart(fig_vol, width="stretch")

with cc2:
    mix = df.groupby(["company", "tech_category"])["lens_id"].count().reset_index(name="n")
    tot = mix.groupby("company")["n"].sum().reset_index(name="total")
    mix = mix.merge(tot, on="company")
    mix["pct"] = 100 * mix["n"] / mix["total"]
    mix["cat_short"] = mix["tech_category"].str.replace(" / ", "/")
    # Shorten long company names for axis legibility
    _co_short = {
        "Sierra Nevada / Sierra Space": "Sierra Space",
        "Maxar Technologies": "Maxar",
        "Virgin Galactic": "Virgin Gal.",
        "Relativity Space": "Relativity",
    }
    mix["co_short"] = mix["company"].replace(_co_short)
    fig_mix = px.bar(
        mix, x="co_short", y="pct", color="cat_short",
        title="Technology Mix (% of Portfolio)",
        labels={"pct": "Share (%)", "co_short": "", "cat_short": "Category"},
    )
    _layout(fig_mix, barmode="stack", height=300, legend=LEGEND_CLEAN,
            xaxis=dict(tickangle=-35, automargin=True, **AXIS),
            yaxis=dict(range=[0, 100], **AXIS),
            margin=dict(l=8, r=8, t=52, b=52))
    st.plotly_chart(fig_mix, width="stretch")

# Jurisdiction + radar in a 2-col row
cd1, cd2 = st.columns([1, 1.3])

with cd1:
    from collections import Counter
    _cpc_counts: Counter = Counter()
    for _row_codes in df["cpc_codes"].dropna():
        for _c in str(_row_codes).split("|"):
            _c = _c.strip()
            if _c:
                _cpc_counts[_c[:8]] += 1
    _top_cpc = pd.DataFrame(_cpc_counts.most_common(14), columns=["cpc", "count"])
    fig_cpc = px.bar(
        _top_cpc, x="count", y="cpc", orientation="h",
        title="Top CPC Subclasses Across Portfolio",
        labels={"count": "Patents", "cpc": ""},
        color="count", color_continuous_scale="Blues",
    )
    _layout(fig_cpc, height=340, showlegend=False, coloraxis_showscale=False,
            xaxis=dict(**AXIS), yaxis=dict(autorange="reversed", **AXIS),
            margin=dict(l=110, r=8, t=52, b=8))
    st.plotly_chart(fig_cpc, width="stretch")

with cd2:
    radar_cats = [
        "Satellite/Wireless Comms", "Antenna Design", "Signal Processing",
        "Spacecraft/Launch Systems", "Rocket Propulsion", "Aeronautics/Structures",
    ]
    radar_map = {
        "Satellite / Wireless Comms": "Satellite/Wireless Comms",
        "Antenna Design": "Antenna Design",
        "Signal Processing": "Signal Processing",
        "Spacecraft / Launch Systems": "Spacecraft/Launch Systems",
        "Rocket Propulsion": "Rocket Propulsion",
        "Aeronautics / Structures": "Aeronautics/Structures",
    }
    fig_rad = go.Figure()
    for co in sel_co:
        cd = df[df["company"] == co]
        total = max(len(cd), 1)
        vals = []
        for orig_cat, _short in radar_map.items():
            vals.append(100 * len(cd[cd["tech_category"] == orig_cat]) / total)
        vals.append(vals[0])
        fig_rad.add_trace(go.Scatterpolar(
            r=vals, theta=radar_cats + [radar_cats[0]],
            fill="toself", name=co,
            line_color=COMPANY_COLORS.get(co, "#888"),
            fillcolor=COMPANY_COLORS.get(co, "#888"),
            opacity=0.42,
        ))
    fig_rad.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter, Helvetica Neue, Arial, sans-serif",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 80], tickfont_size=9,
                            gridcolor="#e3e6ea", linecolor="#e3e6ea"),
            angularaxis=dict(tickfont_size=10, gridcolor="#e3e6ea",
                             linecolor="#e3e6ea"),
        ),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
        title="Technology Focus Radar",
        title_font_size=13,
        height=340,
        margin=dict(l=50, r=50, t=44, b=20),
    )
    st.plotly_chart(fig_rad, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  Full dataset
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("Full Dataset", expanded=False):
    show_cols = ["company", "pub_number", "title", "filing_year",
                 "status", "tech_category", "jurisdiction", "assignee"]
    if "cited_by_count" in df.columns:
        show_cols.append("cited_by_count")
    disp = df[show_cols].sort_values(["company", "filing_year"],
                                     ascending=[True, False]).copy()
    disp["source"] = disp["pub_number"].apply(
        lambda p: gp_url(str(p)) if pd.notna(p) and "/" not in str(p) else ""
    )
    st.dataframe(
        disp,
        width="stretch",
        hide_index=True,
        column_config={
            "source": st.column_config.LinkColumn("Google Patents", display_text="View"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "cited_by_count": st.column_config.NumberColumn("Citations", width="small"),
        },
    )
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False),
        file_name="newspace_patents.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="footer">'
    'Data: USPTO API &nbsp;|&nbsp; '
    'Perkins Coie NewSpace Practice &nbsp;|&nbsp; '
    '</p>',
    unsafe_allow_html=True,
)
