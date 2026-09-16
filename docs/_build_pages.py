# Scaffold generator. Emits the static pages; edit the HTML directly afterwards.
# Re-run only to change the nav or shared chrome across every page at once.

SITE_TITLE = "Housing Out of Reach"
SITE_SUB   = "Homeownership, earnings and borrowing costs for Americans in their twenties, 2000&ndash;2025<br><br>Anjana Anand &middot; PLACEHOLDER course &middot; PLACEHOLDER term"

PAGES = [
    ("index.html",           "Introduction",    "Why homeownership slipped out of reach for a generation", None),
    ("dataprep-eda.html",    "Data Prep & EDA", "Three sources, what was wrong with them, and what they show", "Analysis"),
    ("clustering.html",      "Clustering",      "PLACEHOLDER subtitle", "Models"),
    ("pca.html",             "PCA",             "PLACEHOLDER subtitle", None),
    ("naive-bayes.html",     "Naive Bayes",     "PLACEHOLDER subtitle", None),
    ("decision-trees.html",  "Decision Trees",  "PLACEHOLDER subtitle", None),
    ("svm.html",             "SVMs",            "PLACEHOLDER subtitle", None),
    ("regression.html",      "Regression",      "PLACEHOLDER subtitle", None),
    ("neural-networks.html", "Neural Networks", "PLACEHOLDER subtitle", None),
    ("conclusions.html",     "Conclusions",     "What the evidence says about affordability", "Findings"),
    ("about.html",           "About Me",        "PLACEHOLDER subtitle", None),
]

QUESTIONS = [
    ("How much has the likelihood of owning a home changed for Americans in their twenties and early thirties over the past two decades?",
     "Data Prep &amp; EDA · Conclusions"),
    ("Have the earnings of young workers kept pace with the price of the homes they would need to buy?",
     "Data Prep &amp; EDA · Regression"),
    ("How many years of saving does a typical young worker now need to reach a twenty percent down payment, and how does that compare with someone the same age in 2000?",
     "Data Prep &amp; EDA"),
    ("How has homeownership among householders under 25 differed from those aged 25 to 34, and what might explain the divergence?",
     "Data Prep &amp; EDA · Conclusions"),
    ("How much does a young person's chance of owning depend on which metropolitan area they live in?",
     "Data Prep &amp; EDA · Clustering"),
    ("Has the distance between the most and least affordable housing markets widened since 2000?",
     "Data Prep &amp; EDA · PCA"),
    ("Do American housing markets fall into distinct types that present different obstacles to young buyers?",
     "Clustering"),
    ("Which characteristics most separate an affordable metropolitan area from an unaffordable one?",
     "Decision Trees · PCA"),
    ("Can a metropolitan area's affordability be anticipated from its recent price behaviour alone?",
     "Naive Bayes · SVMs · Neural Networks"),
    ("Did the 2008 financial crisis and the 2020 pandemic leave lasting marks on young-adult homeownership, or did the market return to its earlier path?",
     "Data Prep &amp; EDA · Regression"),
]


COPY = {}
exec(open('_copy.py').read(), COPY)


def todo(text):
    return '<div class="todo">\n      <p>' + text + '</p>\n    </div>'


def questions_html():
    items = "\n".join(
        '      <li>{}</li>'.format(q)
        for q, _m in QUESTIONS)
    return '<ol class="questions">\n' + items + '\n    </ol>'


INTRO_BODY = """
    <figure class="hero">
      <img src="images/intro-hero.jpg" alt="A large Mediterranean-style house behind a paved forecourt">
      <figcaption><b>Figure 1.</b> PLACEHOLDER: two sentences on what this image represents and why it
      opens the project. Credit the image source here.</figcaption>
    </figure>

    <h2>Research Topic &amp; Significance</h2>
    {t_topic}

    <h2>Stakeholders</h2>
    {t_stake}

    <h2>Existing Solutions &amp; Gaps</h2>
    {t_gaps}

    <h2>Blueprint for This Project</h2>
    {t_blueprint}

    <h2>Dataset Considerations</h2>
    {t_dataset}

    <h2>Research Questions</h2>
    <p>Ten questions this project sets out to answer, and the section of this site where each is addressed.</p>
    {questions}

    <h2>Data Sources</h2>
    <div class="scroll">
      <table>
        <thead><tr><th>Source</th><th>Access</th><th>What it provides</th><th>Coverage</th></tr></thead>
        <tbody>
          <tr>
            <td><a href="https://www.census.gov/housing/hvs/data/histtabs.html">Census Housing Vacancy Survey</a><br><span style="color:var(--muted)">Table 12</span></td>
            <td>Download</td>
            <td>Households and owner households by age of householder</td>
            <td>1982&ndash;2025, national, annual</td>
          </tr>
          <tr>
            <td><a href="https://fred.stlouisfed.org/docs/api/fred/">BLS and Census via FRED</a><br><span style="color:var(--muted)">8 series</span></td>
            <td><strong>API</strong></td>
            <td>Median weekly earnings by age, 30-year mortgage rate, homeownership rate, median sales price, Case&ndash;Shiller index, CPI, housing starts</td>
            <td>2000&ndash;2026, national, weekly to quarterly</td>
          </tr>
          <tr>
            <td><a href="https://www.zillow.com/research/data/">Zillow ZHVI</a><br><span style="color:var(--muted)">metro, tier 0.33&ndash;0.67</span></td>
            <td>Download</td>
            <td>Typical home value per metropolitan area</td>
            <td>2000&ndash;2026, 894 metros, monthly</td>
          </tr>
        </tbody>
      </table>
    </div>
"""

PREP_BODY = """
    <h2>Data Collection</h2>
    {t_collect}

    <h3>API source</h3>
    <div class="callout">
      <p><strong>Source:</strong> Federal Reserve Bank of St. Louis, FRED API<br>
      <strong>Documentation:</strong> <a href="https://fred.stlouisfed.org/docs/api/fred/">fred.stlouisfed.org/docs/api/fred</a><br>
      <strong>Base endpoint:</strong> <code>https://api.stlouisfed.org/fred/series/observations</code></p>
      <p><strong>Example GET request</strong></p>
      <pre><code>https://api.stlouisfed.org/fred/series/observations
  ?series_id=MORTGAGE30US
  &amp;observation_start=2000-01-01
  &amp;file_type=json
  &amp;api_key=YOUR_KEY</code></pre>
      <p>Eight series were retrieved this way, returning 2,771 raw observations.
      <a href="#">PLACEHOLDER: link to fred_api_fetch.py</a></p>
    </div>

    <h3>Downloaded sources</h3>
    {t_downloads}

{sources}
    <h2>Assumptions</h2>
    <div class="todo">
      <p>Every modelling choice below is a decision, not a measurement. Introduce them in your own words.</p>
    </div>
    <ul class="tight">
      <li>Annual earnings are estimated as median weekly earnings &times; 52.</li>
      <li>Years-to-down-payment assumes 15% of gross income saved each year.</li>
      <li>Monthly payment figures assume a 30-year fixed loan at 80% loan-to-value.</li>
      <li>Each year's home value is the latest month Zillow reported that year, so 2026 is partial.</li>
      <li>Earnings are national, so metro affordability compares local prices against a national income.</li>
    </ul>

    <h2>Links to Raw Data &amp; Code</h2>
    <ul class="linklist">
      <li><a href="#">PLACEHOLDER</a> <span>: histtab12.xlsx, raw HVS workbook</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: Metro ZHVI, raw Zillow CSV</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: raw FRED API responses, 8 JSON files</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: fred_api_fetch.py, API collection script</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: build_datasets.py, cleaning pipeline</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: make_eda_figures.py, figure generation</span></li>
      <li><a href="#">PLACEHOLDER</a> <span>: cleaned tables, data_clean/</span></li>
    </ul>

    <h2>Summary Statistics</h2>

    <p>Descriptive statistics for the national table, 26 annual observations covering 2000 to 2025.
    Skewness is the column worth reading: the ownership and rate measures are close to symmetric, while
    price and earnings are mildly right-skewed by their upward trend rather than by outliers.</p>

    <div class="scroll">
      <table>
        <thead><tr><th>Column</th><th class="num">Mean</th><th class="num">Median</th>
        <th class="num">Variance</th><th class="num">Std dev</th><th class="num">Skewness</th>
        <th class="num">Count</th></tr></thead>
        <tbody>
          <tr><td><code>ownership_rate_lt25_pct</code></td><td class="num">23.34</td><td class="num">22.93</td><td class="num">1.66</td><td class="num">1.29</td><td class="num">0.54</td><td class="num">26</td></tr>
          <tr><td><code>ownership_rate_25_29_pct</code></td><td class="num">36.03</td><td class="num">35.24</td><td class="num">10.79</td><td class="num">3.28</td><td class="num">0.25</td><td class="num">26</td></tr>
          <tr><td><code>ownership_rate_30_34_pct</code></td><td class="num">50.70</td><td class="num">49.23</td><td class="num">15.24</td><td class="num">3.90</td><td class="num">0.37</td><td class="num">26</td></tr>
          <tr><td><code>annual_earnings_25_34</code></td><td class="num">39,340</td><td class="num">36,784</td><td class="num">75,881,392</td><td class="num">8,711.0</td><td class="num">0.98</td><td class="num">26</td></tr>
          <tr><td><code>annual_earnings_25_34_real2025</code></td><td class="num">53,963</td><td class="num">53,162</td><td class="num">6,560,728</td><td class="num">2,561.4</td><td class="num">0.83</td><td class="num">26</td></tr>
          <tr><td><code>national_zhvi</code></td><td class="num">223,512</td><td class="num">202,524</td><td class="num">5,343,570,842</td><td class="num">73,100</td><td class="num">1.01</td><td class="num">26</td></tr>
          <tr><td><code>mortgage_rate_30yr_pct</code></td><td class="num">5.21</td><td class="num">5.19</td><td class="num">1.90</td><td class="num">1.38</td><td class="num">0.12</td><td class="num">26</td></tr>
          <tr><td><code>price_to_income_25_34</code></td><td class="num">5.59</td><td class="num">5.55</td><td class="num">0.53</td><td class="num">0.73</td><td class="num">0.15</td><td class="num">26</td></tr>
          <tr><td><code>payment_to_income_pct_25_34</code></td><td class="num">29.71</td><td class="num">29.00</td><td class="num">41.01</td><td class="num">6.40</td><td class="num">0.41</td><td class="num">26</td></tr>
          <tr><td><code>housing_starts_thousands</code></td><td class="num">1,307.7</td><td class="num">1,348.8</td><td class="num">174,704</td><td class="num">418.0</td><td class="num">-0.17</td><td class="num">26</td></tr>
        </tbody>
      </table>
    </div>

    <p>The full table for all 22 numeric columns is written to
    <code>data_clean/summary_statistics.csv</code> by the pipeline.</p>

    <h2>Exploratory Data Analysis</h2>
    {t_eda}

    <div class="callout">
      <p>Ten figures. Each carries a title, axis labels and two sentences beneath: what it shows,
      then what it means. Thumbnails link through to the full-size image.</p>
    </div>

    <div class="figgrid">
{figslots}
    </div>



    <h3>Code used</h3>
    <p>Every figure above is produced by a single script that reads the cleaned tables and writes
    both a full-size image and a thumbnail. Re-running it regenerates all ten, so the figures cannot
    drift from the data behind them.</p>
    <div class="codeblock">
      <div class="codehead">make_eda_figures.py<span>all ten figures, 326 lines</span></div>
      <pre><code># EDA figures for the Gen Z Homeownership project
# Regenerates every figure in docs/images/ from the cleaned tables in data_clean/
# Run: python3 make_eda_figures.py

import os
import math

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

out_dir = &quot;docs/images&quot;
os.makedirs(out_dir, exist_ok=True)

# Categorical colours, validated for colour-vision deficiency
palette = [&quot;#2a78d6&quot;, &quot;#eb6834&quot;, &quot;#1baf7a&quot;, &quot;#eda100&quot;]
blues = [&quot;#cde2fb&quot;, &quot;#9ec5f4&quot;, &quot;#5598e7&quot;, &quot;#2a78d6&quot;, &quot;#256abf&quot;, &quot;#184f95&quot;, &quot;#0d366b&quot;]
surface = &quot;#fcfcfb&quot;

# Load cleaned datasets locally
national = pd.read_csv(&quot;data_clean/national_annual.csv&quot;)
ownership = pd.read_csv(&quot;data_clean/ownership_by_age_annual.csv&quot;)
panel = pd.read_csv(&quot;data_clean/metro_year_panel.csv&quot;)

# Latest year of the metro panel, used by several figures
latest = panel[panel[&quot;year&quot;] == 2025].dropna(subset=[&quot;price_to_income_25_34&quot;]).copy()


def save(fig, n, title):
    fig.update_layout(
        template=&quot;plotly_white&quot;,
        title=dict(text=title, font=dict(size=17)),
        paper_bgcolor=surface,
        plot_bgcolor=surface,
        font=dict(family=&quot;Helvetica, Arial, sans-serif&quot;, size=13, color=&quot;#0b0b0b&quot;),
        margin=dict(l=70, r=40, t=70, b=60),
        width=1100,
        height=560,
    )
    # Static export needs a local Chrome for kaleido. Where that is unavailable the
    # figure is written as HTML instead and exported to PNG separately.
    try:
        fig.write_image(f&quot;{{out_dir}}/eda-{{n:02d}}-large.png&quot;, scale=2)
        fig.write_image(f&quot;{{out_dir}}/eda-{{n:02d}}.png&quot;, scale=0.62)
    except Exception:
        os.makedirs(&quot;_figures_html&quot;, exist_ok=True)
        fig.write_html(f&quot;_figures_html/eda-{{n:02d}}.html&quot;, include_plotlyjs=&quot;directory&quot;)
    print(f&quot;  eda-{{n:02d}}  {{title}}&quot;)


# Figure 1. Homeownership rate by age of householder
age_trend = ownership[ownership[&quot;age_bracket&quot;].isin([&quot;&lt;25&quot;, &quot;25-29&quot;, &quot;30-34&quot;])]

fig1 = px.line(
    age_trend,
    x=&quot;year&quot;,
    y=&quot;ownership_rate_pct&quot;,
    color=&quot;age_bracket&quot;,
    category_orders={{&quot;age_bracket&quot;: [&quot;30-34&quot;, &quot;25-29&quot;, &quot;&lt;25&quot;]}},
    color_discrete_sequence=palette,
    labels={{&quot;year&quot;: &quot;&quot;, &quot;ownership_rate_pct&quot;: &quot;Homeownership rate (%)&quot;, &quot;age_bracket&quot;: &quot;Age&quot;}},
    title=&quot;Homeownership rate by age of householder, 1982 to 2025&quot;,
)
fig1.update_traces(line=dict(width=2.5))
save(fig1, 1, &quot;Homeownership rate by age of householder, 1982 to 2025&quot;)


# Figure 2. Least affordable metropolitan areas
top_n = 12

least_affordable = (
    latest.nlargest(top_n, &quot;price_to_income_25_34&quot;)
    .sort_values(&quot;price_to_income_25_34&quot;)
    .reset_index(drop=True)
)

fig2 = px.bar(
    least_affordable,
    x=&quot;price_to_income_25_34&quot;,
    y=&quot;region_name&quot;,
    orientation=&quot;h&quot;,
    text=&quot;price_to_income_25_34&quot;,
    color_discrete_sequence=[palette[0]],
    labels={{&quot;price_to_income_25_34&quot;: &quot;Home price as a multiple of annual earnings&quot;, &quot;region_name&quot;: &quot;&quot;}},
    title=f&quot;The {{top_n}} least affordable metropolitan areas, 2025&quot;,
)
fig2.update_traces(texttemplate=&quot;%{{text:.1f}}&quot;, textposition=&quot;outside&quot;, cliponaxis=False)
save(fig2, 2, f&quot;The {{top_n}} least affordable metropolitan areas, 2025&quot;)


# Figure 3. Correlation between national measures
measures = [
    &quot;ownership_rate_25_29_pct&quot;, &quot;ownership_rate_30_34_pct&quot;,
    &quot;annual_earnings_25_34&quot;, &quot;annual_earnings_25_34_real2025&quot;,
    &quot;national_zhvi&quot;, &quot;mortgage_rate_30yr_pct&quot;,
    &quot;price_to_income_25_34&quot;, &quot;payment_to_income_pct_25_34&quot;,
    &quot;housing_starts_thousands&quot;,
]
measures = [c for c in measures if c in national.columns]

corr = national[measures].corr().round(2)
short = [c.replace(&quot;_pct&quot;, &quot;&quot;).replace(&quot;_25_34&quot;, &quot;&quot;).replace(&quot;_&quot;, &quot; &quot;).strip() for c in measures]
corr.index, corr.columns = short, short

fig3 = px.imshow(
    corr,
    text_auto=True,
    zmin=-1,
    zmax=1,
    color_continuous_scale=&quot;RdBu_r&quot;,
    title=&quot;Correlation between national measures, 2000 to 2025&quot;,
)
fig3.update_xaxes(tickangle=40)
save(fig3, 3, &quot;Correlation between national measures, 2000 to 2025&quot;)


# Figure 4. Where the metropolitan areas are
state_counts = latest[&quot;state_name&quot;].value_counts()
top_states = state_counts.head(8)

share = pd.DataFrame({{
    &quot;state&quot;: list(top_states.index) + [&quot;Other states&quot;],
    &quot;metros&quot;: list(top_states.values) + [int(state_counts[8:].sum())],
}})

fig4 = px.pie(
    share,
    names=&quot;state&quot;,
    values=&quot;metros&quot;,
    hole=0.42,
    color_discrete_sequence=blues[::-1],
    title=f&quot;Where the {{len(latest)}} metropolitan areas are, by state&quot;,
)
fig4.update_traces(textinfo=&quot;label+value&quot;, textposition=&quot;outside&quot;,
                   marker=dict(line=dict(color=surface, width=2)))
save(fig4, 4, &quot;Where the metropolitan areas are, by state&quot;)


# Figure 5. Affordability quartile membership by year
quartiles = (
    panel.dropna(subset=[&quot;affordability_quartile&quot;])
    .groupby([&quot;year&quot;, &quot;affordability_quartile&quot;])
    .size()
    .reset_index(name=&quot;metros&quot;)
)

fig5 = px.bar(
    quartiles,
    x=&quot;year&quot;,
    y=&quot;metros&quot;,
    color=&quot;affordability_quartile&quot;,
    category_orders={{&quot;affordability_quartile&quot;:
                     [&quot;Q1_most_affordable&quot;, &quot;Q2&quot;, &quot;Q3&quot;, &quot;Q4_least_affordable&quot;]}},
    color_discrete_sequence=palette,
    labels={{&quot;year&quot;: &quot;&quot;, &quot;metros&quot;: &quot;Number of metropolitan areas&quot;, &quot;affordability_quartile&quot;: &quot;Quartile&quot;}},
    title=&quot;Affordability quartile membership by year&quot;,
)
fig5.update_traces(marker_line=dict(color=surface, width=1.5))
save(fig5, 5, &quot;Affordability quartile membership by year&quot;)


# Figure 6. Starting price against subsequent growth
wide = (
    panel[panel[&quot;year&quot;].isin([2000, 2025])]
    .pivot_table(index=&quot;region_name&quot;, columns=&quot;year&quot;, values=&quot;zhvi&quot;)
    .dropna()
    .reset_index()
)
wide[&quot;growth_pct&quot;] = (wide[2025] / wide[2000] - 1) * 100

slope, intercept = np.polyfit(wide[2000], wide[&quot;growth_pct&quot;], 1)
line_x = np.linspace(wide[2000].min(), wide[2000].max(), 100)
pearson = wide[2000].corr(wide[&quot;growth_pct&quot;])
# Spearman is Pearson on the ranks, computed directly so scipy is not needed
spearman = wide[2000].rank().corr(wide[&quot;growth_pct&quot;].rank())

fig6 = px.scatter(
    wide,
    x=2000,
    y=&quot;growth_pct&quot;,
    hover_name=&quot;region_name&quot;,
    opacity=0.5,
    color_discrete_sequence=[palette[0]],
    labels={{&quot;2000&quot;: &quot;Typical home value in 2000 (USD)&quot;, &quot;growth_pct&quot;: &quot;Growth to 2025 (%)&quot;}},
    title=&quot;Did expensive markets in 2000 grow faster since?&quot;,
)
fig6.add_trace(go.Scatter(
    x=line_x,
    y=slope * line_x + intercept,
    mode=&quot;lines&quot;,
    line=dict(color=palette[1], width=2.5, dash=&quot;dash&quot;),
    name=&quot;OLS trend&quot;,
))
fig6.add_annotation(
    x=0.98, y=0.96, xref=&quot;paper&quot;, yref=&quot;paper&quot;, showarrow=False, align=&quot;right&quot;,
    text=f&quot;Pearson r = {{pearson:.3f}}&lt;br&gt;Spearman r = {{spearman:.3f}}&lt;br&gt;n = {{len(wide)}} metros&quot;,
    bgcolor=surface, bordercolor=&quot;#e1e0d9&quot;, borderwidth=1, font=dict(size=12),
)
save(fig6, 6, &quot;Did expensive markets in 2000 grow faster since?&quot;)


# Figure 7. Spread of metropolitan affordability
selected_years = [2000, 2005, 2010, 2015, 2020, 2025]
spread = panel[panel[&quot;year&quot;].isin(selected_years)].dropna(subset=[&quot;price_to_income_25_34&quot;])

fig7 = px.box(
    spread,
    x=&quot;year&quot;,
    y=&quot;price_to_income_25_34&quot;,
    points=False,
    color_discrete_sequence=[palette[0]],
    labels={{&quot;year&quot;: &quot;&quot;, &quot;price_to_income_25_34&quot;: &quot;Price as a multiple of annual earnings&quot;}},
    title=&quot;Spread of metropolitan affordability, selected years&quot;,
)
fig7.update_xaxes(type=&quot;category&quot;)
save(fig7, 7, &quot;Spread of metropolitan affordability, selected years&quot;)


# Figure 8. Metropolitan areas per state
state_summary = (
    latest.groupby(&quot;state_name&quot;)
    .agg(metros=(&quot;region_name&quot;, &quot;count&quot;), median_value=(&quot;zhvi&quot;, &quot;median&quot;))
    .reset_index()
)
state_summary = state_summary[state_summary[&quot;metros&quot;] &gt;= 4]

fig8 = px.treemap(
    state_summary,
    path=[&quot;state_name&quot;],
    values=&quot;metros&quot;,
    color=&quot;median_value&quot;,
    color_continuous_scale=blues,
    labels={{&quot;median_value&quot;: &quot;Median home value (USD)&quot;}},
    title=&quot;Metropolitan areas per state, shaded by median home value, 2025&quot;,
)
fig8.update_traces(marker=dict(line=dict(color=surface, width=2)),
                   root_color=surface,
                   texttemplate=&quot;%{{label}}&lt;br&gt;%{{value}}&quot;)
save(fig8, 8, &quot;Metropolitan areas per state, shaded by median home value, 2025&quot;)


# Figure 9. Affordability within the states with the most metros
busiest = latest[&quot;state_name&quot;].value_counts().head(12).index
by_state = latest[latest[&quot;state_name&quot;].isin(busiest)]
order = by_state.groupby(&quot;state_name&quot;)[&quot;price_to_income_25_34&quot;].median().sort_values().index.tolist()

fig9 = px.violin(
    by_state,
    x=&quot;state_name&quot;,
    y=&quot;price_to_income_25_34&quot;,
    box=True,
    category_orders={{&quot;state_name&quot;: order}},
    color_discrete_sequence=[palette[0]],
    labels={{&quot;state_name&quot;: &quot;&quot;, &quot;price_to_income_25_34&quot;: &quot;Price as a multiple of annual earnings&quot;}},
    title=&quot;Affordability within the 12 states with the most metros, 2025&quot;,
)
save(fig9, 9, &quot;Affordability within the 12 states with the most metros, 2025&quot;)


# Figure 10. Normal Q-Q plot
# scipy is not a dependency here, so the inverse normal CDF is Acklam&#x27;s approximation
def norm_ppf(p):
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    if p &lt; 0.02425:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p &gt; 1 - 0.02425:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

observed = np.sort(latest[&quot;price_to_income_25_34&quot;].values)
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
    labels={{&quot;x&quot;: &quot;Theoretical normal quantiles&quot;, &quot;y&quot;: &quot;Observed price-to-income&quot;}},
    title=&quot;Is metropolitan affordability normally distributed?&quot;,
)
fig10.add_trace(go.Scatter(
    x=theoretical,
    y=qq_slope * theoretical + qq_intercept,
    mode=&quot;lines&quot;,
    line=dict(color=palette[1], width=2.5, dash=&quot;dash&quot;),
    name=&quot;Normal reference&quot;,
))
fig10.add_annotation(
    x=0.03, y=0.96, xref=&quot;paper&quot;, yref=&quot;paper&quot;, showarrow=False, align=&quot;left&quot;,
    text=f&quot;skewness = {{skewness:.2f}}&lt;br&gt;n = {{n_obs}} metros&quot;,
    bgcolor=surface, bordercolor=&quot;#e1e0d9&quot;, borderwidth=1, font=dict(size=12),
)
save(fig10, 10, &quot;Is metropolitan affordability normally distributed?&quot;)


# Summary statistics for the Data Prep tab
numeric = national.select_dtypes(include=[np.number]).drop(columns=[&quot;year&quot;], errors=&quot;ignore&quot;)

summary = pd.DataFrame({{
    &quot;mean&quot;: numeric.mean(),
    &quot;median&quot;: numeric.median(),
    &quot;variance&quot;: numeric.var(),
    &quot;std_dev&quot;: numeric.std(),
    &quot;skewness&quot;: numeric.skew(),
    &quot;count&quot;: numeric.count(),
}}).round(3)
summary.index.name = &quot;column&quot;
summary.to_csv(&quot;data_clean/summary_statistics.csv&quot;)
print(f&quot;  summary_statistics.csv  {{len(summary)}} columns&quot;)</code></pre>
    </div>

    <h2>Inspection &amp; Reflection</h2>
    <div class="todo">
      <p>Missingness, duplicates, coverage gaps, and any bias the cleaning introduced. Be explicit about
      what a reader should not over-interpret.</p>
    </div>
"""

MODEL_BODY = """
    <div class="meta">
      <dl>
        <dt>Category</dt><dd>PLACEHOLDER: regression / classification / clustering / dimensionality reduction</dd>
        <dt>Target</dt><dd>PLACEHOLDER: the column being predicted, or &ldquo;unsupervised&rdquo;</dd>
        <dt>Data used</dt><dd>PLACEHOLDER: which cleaned table, and how many rows</dd>
      </dl>
    </div>

    <h2>Why This Model Was Chosen</h2>
    {t_why}
    <ul class="tight">
      <li>PLACEHOLDER: reason one</li>
      <li>PLACEHOLDER: reason two</li>
      <li>PLACEHOLDER: reason three</li>
    </ul>

    <h2>Core Assumptions</h2>
    {t_assume}
    <ul class="tight">
      <li>PLACEHOLDER: assumption one</li>
      <li>PLACEHOLDER: assumption two</li>
      <li>PLACEHOLDER: assumption three</li>
    </ul>

    <h2>Data Preparation</h2>
    {t_prep}

    <figure>
      <img src="images/PLACEHOLDER-{slug}-before.png" alt="Data before preparation">
      <figcaption><b>Before.</b> PLACEHOLDER: the data before preparation for this method.</figcaption>
    </figure>
    <figure>
      <img src="images/PLACEHOLDER-{slug}-after.png" alt="Data after preparation">
      <figcaption><b>After.</b> PLACEHOLDER: the data as fed to the model.</figcaption>
    </figure>

    <h2>Parameters Explored</h2>
    <div class="scroll">
      <table>
        <thead><tr><th>Run</th><th>Parameters</th><th>Note</th></tr></thead>
        <tbody>
          <tr><td>1</td><td><code>PLACEHOLDER</code></td><td>PLACEHOLDER</td></tr>
          <tr><td>2</td><td><code>PLACEHOLDER</code></td><td>PLACEHOLDER</td></tr>
          <tr><td>3</td><td><code>PLACEHOLDER</code></td><td>PLACEHOLDER</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Results</h2>
    <figure>
      <img src="images/PLACEHOLDER-{slug}-result.png" alt="Model results">
      <figcaption><b>Figure.</b> PLACEHOLDER: what this figure shows, then what it means.</figcaption>
    </figure>
    <div class="scroll">
      <table>
        <thead><tr><th>Metric</th><th class="num">Value</th><th>Direction</th><th>What it means here</th></tr></thead>
        <tbody>
          <tr><td>PLACEHOLDER</td><td class="num">n/a</td><td>Higher is better</td><td>PLACEHOLDER</td></tr>
          <tr><td>PLACEHOLDER</td><td class="num">n/a</td><td>Lower is better</td><td>PLACEHOLDER</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Code</h2>
    <ul class="linklist">
      <li><a href="#">PLACEHOLDER</a> <span>: notebook or script for this section</span></li>
    </ul>

    <h2>Conclusions</h2>
    {t_concl}
"""

CONCL_BODY = """
    <h2>Model Conclusions</h2>
    {t_models}

    <div class="scroll">
      <table>
        <thead><tr><th>Model</th><th>Best result</th><th>Headline finding</th></tr></thead>
        <tbody>
          <tr><td>Clustering</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>PCA</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>Naive Bayes</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>Decision Trees</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>SVMs</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>Regression</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
          <tr><td>Neural Networks</td><td>PLACEHOLDER</td><td>PLACEHOLDER</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Visualization Findings</h2>
    {t_viz}

    <h2>Answers to the Research Questions</h2>
    <div class="todo">
      <p>Take the ten questions from the Introduction in order. Answer each in a few sentences, pointing
      at the section and figure that supports it.</p>
    </div>

    <h2>Overall Conclusions</h2>
    {t_overall}

    <h2>Limitations</h2>
    <div class="todo">
      <p>Specific and honest: what the data cannot show, where coverage is thin, and which assumptions
      would change the conclusion if they were wrong.</p>
    </div>

    <h2>Future Work</h2>
    {t_future}
"""

ABOUT_BODY = """
    <div class="member">
      <img src="images/PLACEHOLDER-portrait.jpg" alt="">
      <div>
        <h4>Anjana Anand</h4>
        <p class="role">PLACEHOLDER role</p>
        <p>PLACEHOLDER: this is the one page where first person is allowed. Write about yourself here:
        background, what drew you to this topic, what you took from the project.</p>
        <p><a href="#">LinkedIn</a> &middot; <a href="#">GitHub</a></p>
      </div>
    </div>
"""


def nav(current):
    out = []
    for href, label, _sub, group in PAGES:
        if group:
            out.append('        <p class="group">{}</p>'.format(group))
        cls = ' class="active"' if href == current else ''
        out.append('        <a href="{}"{}>{}</a>'.format(href, cls, label))
    return "\n".join(out)


def page(href, label, subtitle, body):
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{label} &middot; {site}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=Public+Sans:wght@400;500;650&display=swap">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <div class="shell">

    <aside class="sidebar">
      <p class="site-title">{site}</p>
      <p class="site-sub">{sub}</p>
      <p class="nav-label">Contents</p>
      <nav>
{navlinks}
      </nav>
    </aside>

    <main class="content">
      <h1>{label}</h1>
      <p class="subtitle">{subtitle}</p>
      <hr class="rule-under">
{body}
    </main>

  </div>

  <script src="assets/ui.js" defer></script>
</body>
</html>
""".format(label=label, site=SITE_TITLE, sub=SITE_SUB, navlinks=nav(href),
           subtitle=subtitle, body=body)


figslots = '      <figure>\n        <a href="images/eda-01-large.png"><img src="images/eda-01.png" alt="Homeownership rate by age of householder, 1982 to 2025"></a>\n        <figcaption><b>Figure 11.</b> Homeownership rate by age of householder, 1982 to 2025. All three brackets peak in the mid 2000s and fall sharply through 2016. The 25 to 29 and 30 to 34 brackets remain well below their pre-2008 levels more than fifteen years later, while the under 25 bracket sits slightly above where it began.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-02-large.png"><img src="images/eda-02.png" alt="The twelve least affordable metropolitan areas, 2025"></a>\n        <figcaption><b>Figure 12.</b> The twelve least affordable metropolitan areas, 2025. San Jose tops the list at 27.1 times annual earnings, with Vineyard Haven and Jackson above 23. In these markets a typical home costs more than two decades of a young worker\'s entire gross pay.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-03-large.png"><img src="images/eda-03.png" alt="Correlation between national measures, 2000 to 2025"></a>\n        <figcaption><b>Figure 13.</b> Correlation between national measures, 2000 to 2025. The mortgage rate correlates with the payment burden at 0.78, more strongly than price-to-income does at 0.71. This is the numeric form of the argument that price alone does not determine affordability.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-04-large.png"><img src="images/eda-04.png" alt="Where the 894 metropolitan areas are, by state"></a>\n        <figcaption><b>Figure 14.</b> Where the 894 metropolitan areas are, by state. Texas contributes 67 metropolitan areas and Ohio 44, with the eight largest states accounting for 36 percent of the total. Coverage is uneven, so any unweighted national average leans toward these states.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-05-large.png"><img src="images/eda-05.png" alt="Affordability quartile membership by year"></a>\n        <figcaption><b>Figure 15.</b> Affordability quartile membership by year. Quartiles are recomputed within each year, so the four bands are equal by construction and the visible change is coverage. Zillow reported 444 metropolitan areas in 2000 and 894 in 2025, which matters when comparing distributions across years.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-06-large.png"><img src="images/eda-06.png" alt="Did expensive markets in 2000 grow faster since?"></a>\n        <figcaption><b>Figure 16.</b> Did expensive markets in 2000 grow faster since?. Across the 444 metros reported in both years the relationship is weakly positive, Pearson r = 0.30, with growth ranging from 38 to 505 percent. Starting price explains only a small part of what happened next, so expensive markets did not simply run away from cheap ones.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-07-large.png"><img src="images/eda-07.png" alt="Spread of metropolitan affordability, selected years"></a>\n        <figcaption><b>Figure 17.</b> Spread of metropolitan affordability, selected years. The median metro moved from 3.67 times earnings in 2000 to 4.25 in 2025, while the interquartile range widened from 2.98-4.75 to 3.21-5.93. The typical market worsened modestly; the spread between markets worsened considerably more.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-08-large.png"><img src="images/eda-08.png" alt="Metropolitan areas per state, shaded by median home value, 2025"></a>\n        <figcaption><b>Figure 18.</b> Metropolitan areas per state, shaded by median home value, 2025. Area shows how many metropolitan areas each state contains and shade shows the median home value among them. Hawaii and Massachusetts are small in count but darkest in value, while Texas and Ohio are large in count and light.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-09-large.png"><img src="images/eda-09.png" alt="Affordability within the twelve states with the most metros, 2025"></a>\n        <figcaption><b>Figure 19.</b> Affordability within the twelve states with the most metros, 2025. Median price-to-income runs from 2.70 in Mississippi to 15.68 in Hawaii, and the width of each shape shows that states differ internally as much as they differ from one another. A state-level average would hide most of this.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-10-large.png"><img src="images/eda-10.png" alt="Is metropolitan affordability normally distributed?"></a>\n        <figcaption><b>Figure 20.</b> Is metropolitan affordability normally distributed?. The points bend away from the fitted line in the upper tail and the distribution carries a skewness of 2.76. Affordability is strongly right-skewed, which argues for a log transform or rank-based methods in the modelling sections rather than assuming normality.</figcaption>\n      </figure>'

def build_all():
    for href, label, subtitle, _group in PAGES:
        slug = href.replace(".html", "")
        if href == "index.html":
            body = INTRO_BODY.format(
                questions=questions_html(),
                t_topic=COPY['INTRO_TOPIC'],
                t_stake=COPY['INTRO_STAKE'],
                t_gaps=COPY['INTRO_GAPS'],
                t_blueprint=COPY['INTRO_BLUEPRINT'],
                t_dataset=COPY['INTRO_DATASET'],
            )
        elif href == "dataprep-eda.html":
            body = PREP_BODY.format(
                figslots=figslots,
            sources=COPY['PREP_SOURCES'],
                t_collect=COPY['PREP_COLLECT'],
                t_downloads=COPY['PREP_DOWNLOADS'],
                                    t_eda=COPY['PREP_EDA'],
            )
        elif href == "conclusions.html":
            body = CONCL_BODY.format(
                t_models=todo("A paragraph per model family: what it found, and whether it is believable."),
                t_viz=todo("What the figures show that the metrics do not."),
                t_overall=todo("Three or four paragraphs pulling the project together, for a reader who is not a data scientist."),
                t_future=todo("What could be done with more time or better data."),
            )
        elif href == "about.html":
            body = ABOUT_BODY
        else:
            body = MODEL_BODY.format(
                slug=slug,
                t_why=todo("Why this method suits this question, in your own words."),
                t_assume=todo("What this model assumes about the data, and whether the data actually meets those assumptions."),
                t_prep=todo("What this method requires that the others do not, and what was done to meet it."),
                t_concl=todo("What the results mean for the homeownership question. Not a restatement of the metrics."),
            )
        with open(href, "w") as f:
            f.write(page(href, label, subtitle, body))
        print("wrote", href)


if __name__ == "__main__":
    build_all()
