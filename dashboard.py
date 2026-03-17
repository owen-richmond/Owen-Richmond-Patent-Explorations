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
    margin-bottom: 4px;
}
.sec-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0d1117;
    margin: 0 0 3px;
}
.sec-sub {
    font-size: 0.84rem;
    color: #6b7280;
    line-height: 1.55;
    margin-bottom: 0.9rem;
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
    "SpaceX":          "#005288",
    "Blue Origin":     "#2d3748",
    "Rocket Lab":      "#c0392b",
    "Virgin Galactic": "#0077aa",
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

AXIS = dict(gridcolor="#f0f0f0", linecolor="#e3e6ea", tickcolor="#e3e6ea", tickfont_size=11)


def sec(pill: str, title: str, sub: str):
    st.markdown(
        f'<span class="sec-pill">{pill}</span>'
        f'<p class="sec-title">{title}</p>'
        f'<p class="sec-sub">{sub}</p>',
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
        st.warning(
            "Running on illustrative sample data.  \n"
            "To load complete live records:  \n"
            "1. Register free at [lens.org](https://www.lens.org)  \n"
            "2. Go to Account → Lens API → Request Access  \n"
            "3. Run `python fetch_patents.py --token YOUR_TOKEN`"
        )
    else:
        st.success(f"Live data: **{len(df_raw):,}** patents")

    st.markdown("---")
    all_co = sorted(df_raw["company"].unique())
    sel_co = st.multiselect("Companies", all_co, default=all_co)

    ymin = int(df_raw["filing_year"].dropna().min())
    ymax = int(df_raw["filing_year"].dropna().max())
    yr = st.slider("Filing year range", ymin, ymax, (ymin, ymax))

    all_cat = sorted(df_raw["tech_category"].dropna().unique())
    sel_cat = st.multiselect("Technology categories", all_cat, default=all_cat)

    st.markdown("---")
    st.caption("Data: Lens.org Patent API")

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
The NewSpace industry represents a growing IP opportunity. Companies like SpaceX are building
patent portfolios focused heavily on <strong>satellite communications and RF technology</strong>
rather than core rocketry, which they protect as trade secrets. This creates a layered IP landscape
where prosecution strategy, freedom-to-operate analysis, and portfolio management require deep
expertise in wireless systems, semiconductors, and signal processing — areas central to
<strong>Perkins Coie's patent practice</strong>.
</p></blockquote>
""", unsafe_allow_html=True)

# KPIs
granted = df[df["status"] == "granted"]
sx_post19 = df[(df["company"] == "SpaceX") & (df["filing_year"] >= 2019)]["lens_id"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Patents", f"{len(df):,}")
k2.metric("Companies Tracked", len(df["company"].unique()))
k3.metric("Technology Areas", df["tech_category"].nunique())
k4.metric("SpaceX Post-2019", sx_post19, delta="Starlink era")
k5.metric("Granted", f"{len(granted):,}", delta=f"{100*len(granted)/max(len(df),1):.0f}% grant rate")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 1 — Patent Family Prosecution History  (moved to top)
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 1",
    "Patent Family Prosecution History",
    "A patent family captures every filing tied to a single invention: the priority application, "
    "US continuations and divisionals, an international PCT filing, and national-phase entries in "
    "each target jurisdiction. Mapping and managing these relationships is a core service at firms "
    "like Perkins Coie. Select a family below to explore the full prosecution history, then hover "
    "any node for filing details and click the source links in the table to open the original record.",
)

from seed_data import get_all_families
all_families = get_all_families()

sel_family_label = st.selectbox(
    "Select patent family",
    options=list(all_families.keys()),
    label_visibility="collapsed",
)
family_data = all_families[sel_family_label]
is_bo_vtol = "VTOL" in sel_family_label

if is_bo_vtol:
    st.markdown(
        '<p class="ipr-note"><strong>Competitive dynamics:</strong> SpaceX filed '
        'IPR2015-01765 at the PTAB challenging Blue Origin\'s US8678321B2 reusable landing '
        'claims. The PTAB denied institution in April 2016. This case illustrates how patent '
        'prosecution intersects with competitive strategy in the NewSpace industry.</p>',
        unsafe_allow_html=True,
    )

# ── Build positions ───────────────────────────────────────────────────────────
pos_counter = defaultdict(int)
node_pos = {}
for rec in family_data:
    tier = TIER_Y.get(rec["filing_type"], 0)
    key = (rec["filing_year"], tier)
    offset = pos_counter[key] * 0.5
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

    labels = []
    for r in recs:
        # Short label: strip kind codes, keep just the number
        short = (r["pub_number"]
                 .replace("B2", "").replace("B1", "").replace("A1", "").replace("A2", "")
                 .strip())
        if "IPR" in short:
            short = "IPR\n2015-01765"
        labels.append(short)

    traces.append(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(symbol=syms, color=col, size=sz, line=dict(color="#ffffff", width=2)),
        text=labels,
        textposition="top center",
        textfont=dict(size=8.5, color="#2c3e50"),
        customdata=hover_texts,
        hovertemplate="%{customdata}<extra></extra>",
        name=ftype,
        legendgroup=ftype,
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

fam_layout = {
    **CHART_BASE,
    "plot_bgcolor": "#ffffff",
    "height": 560,
    "xaxis": dict(title="Filing Year", tickmode="linear", dtick=1,
                  range=[x_min, x_max], **AXIS),
    "yaxis": dict(showticklabels=False, range=[-0.6, 5.7],
                  gridcolor="#f0f4f8", zeroline=False),
    "legend": dict(title="Filing Type", bgcolor="rgba(255,255,255,0.92)",
                   bordercolor="#e3e6ea", borderwidth=1, font_size=10),
    "annotations": tier_annots + edge_annots,
    "margin": dict(l=90, r=16, t=44, b=36),
    "hovermode": "closest",
    "title": dict(
        text=(
            "Prosecution History: SpaceX Starlink Phased-Array Antenna Family"
            if not is_bo_vtol else
            "Prosecution History: Blue Origin VTOL Landing Family (with SpaceX IPR)"
        ),
        font_size=13, x=0,
    ),
}
fig_fam.update_layout(**fam_layout)

st.plotly_chart(fig_fam, use_container_width=True)

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
    use_container_width=True,
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
    "Annual patent filings reveal a near-dormant SpaceX portfolio through 2015, followed by "
    "sustained growth driven almost entirely by Starlink communications technology rather than "
    "launch vehicle innovation.",
)

tl = df.groupby(["filing_year", "company"])["lens_id"].count().reset_index(name="count")

fig_tl = px.bar(
    tl, x="filing_year", y="count", color="company",
    color_discrete_map=COMPANY_COLORS, barmode="group",
    labels={"filing_year": "Filing Year", "count": "Patents Filed", "company": ""},
    title="Annual Patent Filings by Company",
)
fig_tl.update_layout(**CHART_BASE, height=360,
                     xaxis=dict(tickmode="linear", dtick=1, tickangle=-45, **AXIS),
                     legend=LEGEND_H)
fig_tl.update_yaxes(**AXIS)
st.plotly_chart(fig_tl, use_container_width=True)

ca1, ca2 = st.columns(2)
with ca1:
    sx = df[df["company"] == "SpaceX"]
    sx_tl = sx.groupby(["filing_year", "tech_category"])["lens_id"].count().reset_index(name="n")
    fig_sx = px.area(
        sx_tl, x="filing_year", y="n", color="tech_category",
        title="SpaceX: Technology Area Over Time",
        labels={"filing_year": "Year", "n": "Filings", "tech_category": ""},
    )
    fig_sx.update_layout(**CHART_BASE, height=310, legend=LEGEND_H)
    fig_sx.update_xaxes(tickangle=-45, **AXIS)
    fig_sx.update_yaxes(**AXIS)
    st.plotly_chart(fig_sx, use_container_width=True)

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
    fig_cum.update_layout(**CHART_BASE, height=310, legend=LEGEND_H)
    fig_cum.update_xaxes(tickangle=-45, **AXIS)
    fig_cum.update_yaxes(**AXIS)
    st.plotly_chart(fig_cum, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 3 — Technology Breakdown
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 3",
    "Technology Breakdown",
    "CPC classification analysis shows SpaceX's portfolio concentrated in antenna design, "
    "satellite communications, and signal processing — the three pillars of the Starlink ground "
    "terminal. Propulsion and launch systems, the areas most publicly associated with SpaceX, "
    "represent a small fraction of its patent activity.",
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
    )
    fig_tm.update_layout(**CHART_BASE, height=460, margin=dict(l=4, r=4, t=38, b=4))
    st.plotly_chart(fig_tm, use_container_width=True)

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
    fig_sb.update_layout(**CHART_BASE, height=460, showlegend=False,
                         coloraxis_showscale=False,
                         margin=dict(l=160, r=8, t=38, b=8))
    fig_sb.update_xaxes(**AXIS)
    fig_sb.update_yaxes(tickfont_size=11, **{k: v for k, v in AXIS.items() if k != "tickfont_size"})
    st.plotly_chart(fig_sb, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 4 — Competitor Landscape
# ─────────────────────────────────────────────────────────────────────────────
sec(
    "Section 4",
    "Competitor Landscape",
    "The four leading commercial space companies pursue fundamentally different IP strategies. "
    "Blue Origin concentrates on propulsion and launch system patents; SpaceX concentrates on "
    "communications infrastructure. Rocket Lab and Virgin Galactic maintain smaller, focused "
    "portfolios aligned with their respective market positions.",
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
    fig_vol.update_layout(**CHART_BASE, showlegend=False, height=280,
                          margin=dict(l=100, r=8, t=38, b=8))
    fig_vol.update_xaxes(**AXIS)
    fig_vol.update_yaxes(**AXIS)
    st.plotly_chart(fig_vol, use_container_width=True)

with cc2:
    mix = df.groupby(["company", "tech_category"])["lens_id"].count().reset_index(name="n")
    tot = mix.groupby("company")["n"].sum().reset_index(name="total")
    mix = mix.merge(tot, on="company")
    mix["pct"] = 100 * mix["n"] / mix["total"]
    # Shorten category labels
    mix["cat_short"] = mix["tech_category"].str.replace(" / ", "/")
    fig_mix = px.bar(
        mix, x="company", y="pct", color="cat_short",
        title="Technology Mix (% of Portfolio)",
        labels={"pct": "Portfolio Share (%)", "company": "", "cat_short": "Category"},
    )
    fig_mix.update_layout(**CHART_BASE, barmode="stack", height=280,
                          legend=LEGEND_CLEAN)
    fig_mix.update_xaxes(**AXIS)
    fig_mix.update_yaxes(range=[0, 100], **AXIS)
    st.plotly_chart(fig_mix, use_container_width=True)

# Jurisdiction + radar in a 2-col row
cd1, cd2 = st.columns([1, 1.3])

with cd1:
    valid_jur = ["US", "WO", "EP", "CN", "JP", "KR", "AU", "CA", "GB"]
    jur = (df[df["jurisdiction"].isin(valid_jur)]
           .groupby(["company", "jurisdiction"])["lens_id"].count().reset_index(name="n"))
    fig_jur = px.bar(
        jur, x="jurisdiction", y="n", color="company", barmode="group",
        color_discrete_map=COMPANY_COLORS,
        title="Filing Jurisdiction",
        labels={"n": "Filings", "jurisdiction": "", "company": ""},
    )
    fig_jur.update_layout(**CHART_BASE, height=340, legend=LEGEND_H)
    fig_jur.update_xaxes(**AXIS)
    fig_jur.update_yaxes(**AXIS)
    st.plotly_chart(fig_jur, use_container_width=True)

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
    st.plotly_chart(fig_rad, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  Full dataset
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("Full Dataset", expanded=False):
    show_cols = ["company", "pub_number", "title", "filing_year",
                 "status", "tech_category", "jurisdiction", "assignee"]
    disp = df[show_cols].sort_values(["company", "filing_year"],
                                     ascending=[True, False]).copy()
    disp["source"] = disp["pub_number"].apply(
        lambda p: gp_url(str(p)) if pd.notna(p) and "/" not in str(p) else ""
    )
    st.dataframe(
        disp,
        use_container_width=True,
        hide_index=True,
        column_config={
            "source": st.column_config.LinkColumn("Google Patents", display_text="View"),
            "title": st.column_config.TextColumn("Title", width="large"),
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
    'Data: Lens.org Patent API &nbsp;|&nbsp; '
    'Perkins Coie NewSpace Practice &nbsp;|&nbsp; '
    'Patent data is illustrative; verify against official sources before reliance.'
    '</p>',
    unsafe_allow_html=True,
)
