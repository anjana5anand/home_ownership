# Scaffold generator. Emits the static pages; edit the HTML directly afterwards.
# Re-run only to change the nav or shared chrome across every page at once.

SITE_TITLE = "Housing Out of Reach"
SITE_SUB   = "Homeownership, earnings and borrowing costs for Americans in their twenties, 2000&ndash;2025<br><br>Anjana Anand &middot; CSCI 5612-872: Machine Learning for DTSC &middot; Fall 2026"
REPO_URL   = "https://github.com/anjana5anand/home_ownership"

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
    <div class="hero-banner">
      <img src="images/intro-hero.jpg" alt="A large Mediterranean-style house behind a paved forecourt">
    </div>

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
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/fred_api_fetch.py">fred_api_fetch.py</a></p>
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
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/data_raw/histtab12.xlsx">histtab12.xlsx</a> <span>: raw HVS workbook</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/data_raw/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv">Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv</a> <span>: raw Zillow CSV</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/tree/main/data_raw/fred">data_raw/fred/</a> <span>: raw FRED API responses, 8 JSON files</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/fred_api_fetch.py">fred_api_fetch.py</a> <span>: API collection script</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/build_datasets.py">build_datasets.py</a> <span>: cleaning pipeline</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/make_eda_figures.py">make_eda_figures.py</a> <span>: figure generation</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/tree/main/data_clean">data_clean/</a> <span>: cleaned tables</span></li>
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
      <div class="codehead">make_eda_figures.py<span>all ten figures, 326 lines</span>
        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/make_eda_figures.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>
        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>
      </div>
      <div class="code-body">
        <pre><code># EDA figures for the Gen Z Homeownership project
# Regenerates every figure in docs/images/ from the cleaned tables in data_clean/
# Run: python3 make_eda_figures.py

import plotly.express as px
import plotly.graph_objects as go

out_dir = &quot;docs/images&quot;
os.makedirs(out_dir, exist_ok=True)
&#8942;

# Figure 1. Homeownership rate by age of householder
fig1 = px.line(wide, x=&quot;year&quot;,
               y=[&quot;ownership_rate_lt25_pct&quot;, &quot;ownership_rate_25_29_pct&quot;,
                  &quot;ownership_rate_30_34_pct&quot;],
               labels={{&quot;value&quot;: &quot;ownership rate (%)&quot;, &quot;year&quot;: &quot;&quot;}})
fig1.update_traces(line=dict(width=2.4))
save(fig1, &quot;eda-01&quot;)
&#8942;  # nine more figures follow the same pattern: build with Plotly Express,
        # annotate with the real statistic, save to html and screenshot to png</code></pre>
        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>
      </div>
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
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="github-link" href="{repo}" target="_blank" rel="noopener" aria-label="View source on GitHub">
    <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
  </a>
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
           subtitle=subtitle, body=body, repo=REPO_URL)


figslots = '      <figure>\n        <a href="images/eda-01-large.png"><img src="images/eda-01.png" alt="Homeownership rate by age of householder, 1982 to 2025"></a>\n        <figcaption><b>Figure 11.</b> Homeownership rate by age of householder, 1982 to 2025. All three brackets peak in the mid 2000s and fall sharply through 2016. The 25 to 29 and 30 to 34 brackets remain well below their pre-2008 levels more than fifteen years later, while the under 25 bracket sits slightly above where it began.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-02-large.png"><img src="images/eda-02.png" alt="The twelve least affordable metropolitan areas, 2025"></a>\n        <figcaption><b>Figure 12.</b> The twelve least affordable metropolitan areas, 2025. San Jose tops the list at 27.1 times annual earnings, with Vineyard Haven and Jackson above 23. In these markets a typical home costs more than two decades of a young worker\'s entire gross pay.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-03-large.png"><img src="images/eda-03.png" alt="Correlation between national measures, 2000 to 2025"></a>\n        <figcaption><b>Figure 13.</b> Correlation between national measures, 2000 to 2025. The mortgage rate correlates with the payment burden at 0.78, more strongly than price-to-income does at 0.71. This is the numeric form of the argument that price alone does not determine affordability.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-04-large.png"><img src="images/eda-04.png" alt="Where the 894 metropolitan areas are, by state"></a>\n        <figcaption><b>Figure 14.</b> Where the 894 metropolitan areas are, by state. Texas contributes 67 metropolitan areas and Ohio 44, with the eight largest states accounting for 36 percent of the total. Coverage is uneven, so any unweighted national average leans toward these states.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-05-large.png"><img src="images/eda-05.png" alt="Affordability quartile membership by year"></a>\n        <figcaption><b>Figure 15.</b> Affordability quartile membership by year. Quartiles are recomputed within each year, so the four bands are equal by construction and the visible change is coverage. Zillow reported 444 metropolitan areas in 2000 and 894 in 2025, which matters when comparing distributions across years.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-06-large.png"><img src="images/eda-06.png" alt="Did expensive markets in 2000 grow faster since?"></a>\n        <figcaption><b>Figure 16.</b> Did expensive markets in 2000 grow faster since?. Across the 444 metros reported in both years the relationship is weakly positive, Pearson r = 0.30, with growth ranging from 38 to 505 percent. Starting price explains only a small part of what happened next, so expensive markets did not simply run away from cheap ones.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-07-large.png"><img src="images/eda-07.png" alt="Spread of metropolitan affordability, selected years"></a>\n        <figcaption><b>Figure 17.</b> Spread of metropolitan affordability, selected years. The median metro moved from 3.67 times earnings in 2000 to 4.25 in 2025, while the interquartile range widened from 2.98-4.75 to 3.21-5.93. The typical market worsened modestly; the spread between markets worsened considerably more.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-08-large.png"><img src="images/eda-08.png" alt="Metropolitan areas per state, shaded by median home value, 2025"></a>\n        <figcaption><b>Figure 18.</b> Metropolitan areas per state, shaded by median home value, 2025. Area shows how many metropolitan areas each state contains and shade shows the median home value among them. Hawaii and Massachusetts are small in count but darkest in value, while Texas and Ohio are large in count and light.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-09-large.png"><img src="images/eda-09.png" alt="Affordability within the twelve states with the most metros, 2025"></a>\n        <figcaption><b>Figure 19.</b> Affordability within the twelve states with the most metros, 2025. Median price-to-income runs from 2.72 in Illinois to 8.12 in California, and the width of each shape shows that states differ internally as much as they differ from one another. A state-level average would hide most of this.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-10-large.png"><img src="images/eda-10.png" alt="Is metropolitan affordability normally distributed?"></a>\n        <figcaption><b>Figure 20.</b> Is metropolitan affordability normally distributed?. The points bend away from the fitted line in the upper tail and the distribution carries a skewness of 2.76. Affordability is strongly right-skewed, which argues for a log transform or rank-based methods in the modelling sections rather than assuming normality.</figcaption>\n      </figure>'

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
