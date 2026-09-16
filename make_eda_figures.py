# EDA figures for the Gen Z Homeownership project
# Regenerates every figure in docs/images/ from the cleaned tables in data_clean/
# Run: python3 make_eda_figures.py

import os
import math

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

out_dir = "docs/images"
os.makedirs(out_dir, exist_ok=True)

# Categorical colours, validated for colour-vision deficiency
palette = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
blues = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#256abf", "#184f95", "#0d366b"]
surface = "#fcfcfb"

# Load cleaned datasets locally
national = pd.read_csv("data_clean/national_annual.csv")
ownership = pd.read_csv("data_clean/ownership_by_age_annual.csv")
panel = pd.read_csv("data_clean/metro_year_panel.csv")

# Latest year of the metro panel, used by several figures
latest = panel[panel["year"] == 2025].dropna(subset=["price_to_income_25_34"]).copy()


def save(fig, n, title):
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=17)),
        paper_bgcolor=surface,
        plot_bgcolor=surface,
        font=dict(family="Helvetica, Arial, sans-serif", size=13, color="#0b0b0b"),
        margin=dict(l=70, r=40, t=70, b=60),
        width=1100,
        height=560,
    )
    # Static export needs a local Chrome for kaleido. Where that is unavailable the
    # figure is written as HTML instead and exported to PNG separately.
    try:
        fig.write_image(f"{out_dir}/eda-{n:02d}-large.png", scale=2)
        fig.write_image(f"{out_dir}/eda-{n:02d}.png", scale=0.62)
    except Exception:
        os.makedirs("_figures_html", exist_ok=True)
        fig.write_html(f"_figures_html/eda-{n:02d}.html", include_plotlyjs="directory")
    print(f"  eda-{n:02d}  {title}")


# Figure 1. Homeownership rate by age of householder
age_trend = ownership[ownership["age_bracket"].isin(["<25", "25-29", "30-34"])]

fig1 = px.line(
    age_trend,
    x="year",
    y="ownership_rate_pct",
    color="age_bracket",
    category_orders={"age_bracket": ["30-34", "25-29", "<25"]},
    color_discrete_sequence=palette,
    labels={"year": "", "ownership_rate_pct": "Homeownership rate (%)", "age_bracket": "Age"},
    title="Homeownership rate by age of householder, 1982 to 2025",
)
fig1.update_traces(line=dict(width=2.5))
save(fig1, 1, "Homeownership rate by age of householder, 1982 to 2025")


# Figure 2. Least affordable metropolitan areas
top_n = 12

least_affordable = (
    latest.nlargest(top_n, "price_to_income_25_34")
    .sort_values("price_to_income_25_34")
    .reset_index(drop=True)
)

fig2 = px.bar(
    least_affordable,
    x="price_to_income_25_34",
    y="region_name",
    orientation="h",
    text="price_to_income_25_34",
    color_discrete_sequence=[palette[0]],
    labels={"price_to_income_25_34": "Home price as a multiple of annual earnings", "region_name": ""},
    title=f"The {top_n} least affordable metropolitan areas, 2025",
)
fig2.update_traces(texttemplate="%{text:.1f}", textposition="outside", cliponaxis=False)
save(fig2, 2, f"The {top_n} least affordable metropolitan areas, 2025")


# Figure 3. Correlation between national measures
measures = [
    "ownership_rate_25_29_pct", "ownership_rate_30_34_pct",
    "annual_earnings_25_34", "annual_earnings_25_34_real2025",
    "national_zhvi", "mortgage_rate_30yr_pct",
    "price_to_income_25_34", "payment_to_income_pct_25_34",
    "housing_starts_thousands",
]
measures = [c for c in measures if c in national.columns]

corr = national[measures].corr().round(2)
short = [c.replace("_pct", "").replace("_25_34", "").replace("_", " ").strip() for c in measures]
corr.index, corr.columns = short, short

fig3 = px.imshow(
    corr,
    text_auto=True,
    zmin=-1,
    zmax=1,
    color_continuous_scale="RdBu_r",
    title="Correlation between national measures, 2000 to 2025",
)
fig3.update_xaxes(tickangle=40)
save(fig3, 3, "Correlation between national measures, 2000 to 2025")


# Figure 4. Where the metropolitan areas are
state_counts = latest["state_name"].value_counts()
top_states = state_counts.head(8)

share = pd.DataFrame({
    "state": list(top_states.index) + ["Other states"],
    "metros": list(top_states.values) + [int(state_counts[8:].sum())],
})

fig4 = px.pie(
    share,
    names="state",
    values="metros",
    hole=0.42,
    color_discrete_sequence=blues[::-1],
    title=f"Where the {len(latest)} metropolitan areas are, by state",
)
fig4.update_traces(textinfo="label+value", textposition="outside",
                   marker=dict(line=dict(color=surface, width=2)))
save(fig4, 4, "Where the metropolitan areas are, by state")


# Figure 5. Affordability quartile membership by year
quartiles = (
    panel.dropna(subset=["affordability_quartile"])
    .groupby(["year", "affordability_quartile"])
    .size()
    .reset_index(name="metros")
)

fig5 = px.bar(
    quartiles,
    x="year",
    y="metros",
    color="affordability_quartile",
    category_orders={"affordability_quartile":
                     ["Q1_most_affordable", "Q2", "Q3", "Q4_least_affordable"]},
    color_discrete_sequence=palette,
    labels={"year": "", "metros": "Number of metropolitan areas", "affordability_quartile": "Quartile"},
    title="Affordability quartile membership by year",
)
fig5.update_traces(marker_line=dict(color=surface, width=1.5))
save(fig5, 5, "Affordability quartile membership by year")


# Figure 6. Starting price against subsequent growth
wide = (
    panel[panel["year"].isin([2000, 2025])]
    .pivot_table(index="region_name", columns="year", values="zhvi")
    .dropna()
    .reset_index()
)
wide["growth_pct"] = (wide[2025] / wide[2000] - 1) * 100

slope, intercept = np.polyfit(wide[2000], wide["growth_pct"], 1)
line_x = np.linspace(wide[2000].min(), wide[2000].max(), 100)
pearson = wide[2000].corr(wide["growth_pct"])
# Spearman is Pearson on the ranks, computed directly so scipy is not needed
spearman = wide[2000].rank().corr(wide["growth_pct"].rank())

fig6 = px.scatter(
    wide,
    x=2000,
    y="growth_pct",
    hover_name="region_name",
    opacity=0.5,
    color_discrete_sequence=[palette[0]],
    labels={"2000": "Typical home value in 2000 (USD)", "growth_pct": "Growth to 2025 (%)"},
    title="Did expensive markets in 2000 grow faster since?",
)
fig6.add_trace(go.Scatter(
    x=line_x,
    y=slope * line_x + intercept,
    mode="lines",
    line=dict(color=palette[1], width=2.5, dash="dash"),
    name="OLS trend",
))
fig6.add_annotation(
    x=0.98, y=0.96, xref="paper", yref="paper", showarrow=False, align="right",
    text=f"Pearson r = {pearson:.3f}<br>Spearman r = {spearman:.3f}<br>n = {len(wide)} metros",
    bgcolor=surface, bordercolor="#e1e0d9", borderwidth=1, font=dict(size=12),
)
save(fig6, 6, "Did expensive markets in 2000 grow faster since?")


# Figure 7. Spread of metropolitan affordability
selected_years = [2000, 2005, 2010, 2015, 2020, 2025]
spread = panel[panel["year"].isin(selected_years)].dropna(subset=["price_to_income_25_34"])

fig7 = px.box(
    spread,
    x="year",
    y="price_to_income_25_34",
    points=False,
    color_discrete_sequence=[palette[0]],
    labels={"year": "", "price_to_income_25_34": "Price as a multiple of annual earnings"},
    title="Spread of metropolitan affordability, selected years",
)
fig7.update_xaxes(type="category")
save(fig7, 7, "Spread of metropolitan affordability, selected years")


# Figure 8. Metropolitan areas per state
state_summary = (
    latest.groupby("state_name")
    .agg(metros=("region_name", "count"), median_value=("zhvi", "median"))
    .reset_index()
)
state_summary = state_summary[state_summary["metros"] >= 4]

fig8 = px.treemap(
    state_summary,
    path=["state_name"],
    values="metros",
    color="median_value",
    color_continuous_scale=blues,
    labels={"median_value": "Median home value (USD)"},
    title="Metropolitan areas per state, shaded by median home value, 2025",
)
fig8.update_traces(marker=dict(line=dict(color=surface, width=2)),
                   root_color=surface,
                   texttemplate="%{label}<br>%{value}")
save(fig8, 8, "Metropolitan areas per state, shaded by median home value, 2025")


# Figure 9. Affordability within the states with the most metros
busiest = latest["state_name"].value_counts().head(12).index
by_state = latest[latest["state_name"].isin(busiest)]
order = by_state.groupby("state_name")["price_to_income_25_34"].median().sort_values().index.tolist()

fig9 = px.violin(
    by_state,
    x="state_name",
    y="price_to_income_25_34",
    box=True,
    category_orders={"state_name": order},
    color_discrete_sequence=[palette[0]],
    labels={"state_name": "", "price_to_income_25_34": "Price as a multiple of annual earnings"},
    title="Affordability within the 12 states with the most metros, 2025",
)
save(fig9, 9, "Affordability within the 12 states with the most metros, 2025")


# Figure 10. Normal Q-Q plot
# scipy is not a dependency here, so the inverse normal CDF is Acklam's approximation
def norm_ppf(p):
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    if p < 0.02425:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > 1 - 0.02425:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

observed = np.sort(latest["price_to_income_25_34"].values)
n_obs = len(observed)
theoretical = np.array([norm_ppf((i + 0.5) / n_obs) for i in range(n_obs)])

q1, q3 = np.percentile(observed, [25, 75])
qq_slope = (q3 - q1) / (norm_ppf(0.75) - norm_ppf(0.25))
qq_intercept = q1 - qq_slope * norm_ppf(0.25)
skewness = ((observed - observed.mean()) ** 3).mean() / observed.std() ** 3

fig10 = px.scatter(
    x=theoretical,
    y=observed,
    opacity=0.5,
    color_discrete_sequence=[palette[0]],
    labels={"x": "Theoretical normal quantiles", "y": "Observed price-to-income"},
    title="Is metropolitan affordability normally distributed?",
)
fig10.add_trace(go.Scatter(
    x=theoretical,
    y=qq_slope * theoretical + qq_intercept,
    mode="lines",
    line=dict(color=palette[1], width=2.5, dash="dash"),
    name="Normal reference",
))
fig10.add_annotation(
    x=0.03, y=0.96, xref="paper", yref="paper", showarrow=False, align="left",
    text=f"skewness = {skewness:.2f}<br>n = {n_obs} metros",
    bgcolor=surface, bordercolor="#e1e0d9", borderwidth=1, font=dict(size=12),
)
save(fig10, 10, "Is metropolitan affordability normally distributed?")


# Summary statistics for the Data Prep tab
numeric = national.select_dtypes(include=[np.number]).drop(columns=["year"], errors="ignore")

summary = pd.DataFrame({
    "mean": numeric.mean(),
    "median": numeric.median(),
    "variance": numeric.var(),
    "std_dev": numeric.std(),
    "skewness": numeric.skew(),
    "count": numeric.count(),
}).round(3)
summary.index.name = "column"
summary.to_csv("data_clean/summary_statistics.csv")
print(f"  summary_statistics.csv  {len(summary)} columns")
