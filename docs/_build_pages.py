# Scaffold generator. Emits the static pages; edit the HTML directly afterwards.
# Re-run only to change the nav or shared chrome across every page at once.

SITE_TITLE = "Housing Out of Reach"
SITE_SUB   = "Homeownership, earnings and borrowing costs for Americans in their twenties, 2000&ndash;2025<br><br>Anjana Anand &middot; CSCI 5612-872: Machine Learning for DTSC &middot; Fall 2026"
REPO_URL   = "https://github.com/anjana5anand/home_ownership"

PAGES = [
    ("index.html",           "Introduction",    "Why homeownership slipped out of reach for a generation", None),
    ("dataprep.html",        "Data Prep",       "Three sources, and what was wrong with each one", "Analysis"),
    ("eda.html",             "EDA",              "Summary statistics and ten figures exploring the cleaned data", None),
    ("clustering.html",      "Clustering",      "Partitional and hierarchical clustering of metro housing markets", "Models"),
    ("pca.html",             "PCA",             "Reducing eleven affordability features to a handful that matter", None),
    ("naive-bayes.html",     "Naive Bayes",     "PLACEHOLDER subtitle", None),
    ("decision-trees.html",  "Decision Trees",  "PLACEHOLDER subtitle", None),
    ("svm.html",             "SVMs",            "PLACEHOLDER subtitle", None),
    ("regression.html",      "Regression",      "PLACEHOLDER subtitle", None),
    ("neural-networks.html", "Neural Networks", "PLACEHOLDER subtitle", None),
    ("conclusions.html",     "Conclusions",     "What the evidence says about affordability", "Findings"),
    ("about.html",           "About Me",        "MS Data Science student, CU Boulder", None),
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
      <img class="hero-photo" src="images/intro-hero.jpg" alt="A large Mediterranean-style house behind a paved forecourt">
      <div class="hero-overlay">
        <h1>Housing Out of Reach</h1>
        <p class="hero-sub">Why homeownership has slipped out of reach for a generation</p>
      </div>
    </div>

    <h2>Research Topic &amp; Significance</h2>
    {t_topic}

    <h2>Stakeholders</h2>
    {t_stake}

    <h2>Existing Solutions &amp; Gaps</h2>
    {t_gaps}

    <h2>Blueprint for This Project</h2>
    {t_blueprint}

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

DATAPREP_BODY = """
    <h2>Data Collection</h2>
    {t_collect}

    <h2>Dataset Considerations</h2>
    {t_dataset}

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
"""

EDA_BODY = """
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

    <figure class="wide">
      <a href="images/eda-11-large.png"><img src="images/eda-11.png" alt="Distribution shape of the national annual measures, 2000 to 2025"></a>
      <figcaption><b>Figure 11.</b> Each panel is a histogram of the column at left, with a normal curve fitted to that column's own mean and standard deviation laid over it. The ownership and mortgage-rate panels track their curve closely, while earnings and home value pull away to the right of it, the shape a positive skewness number is describing.</figcaption>
    </figure>

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

CLUSTERING_BODY = """
    <div class="meta">
      <dl>
        <dt>Category</dt><dd>Unsupervised &middot; clustering (partitional and hierarchical)</dd>
        <dt>Target</dt><dd>None, unsupervised</dd>
        <dt>Data used</dt><dd><code>metro_2025_unsupervised_scaled.csv</code>, 894 metros &times; 11 standardized features</dd>
      </dl>
    </div>

    <h2>Overview</h2>
    {t_overview1}

    <figure>
      <img src="images/theory-partitional.png" alt="Partitional clustering concept: points assigned to the nearest centroid">
      <figcaption><b>Figure.</b> Partitional clustering (k-means). Every point joins the nearest centroid, and centroids move to the mean of their assigned points until the assignment stops changing.</figcaption>
    </figure>
    <figure>
      <img src="images/theory-hierarchical.png" alt="Hierarchical clustering concept: a dendrogram of six points">
      <figcaption><b>Figure.</b> Hierarchical clustering. The closest pair merges first, then the next closest, building a tree that can be cut at any height to produce a chosen number of clusters.</figcaption>
    </figure>

    {t_overview2}

    <h2>Data Prep</h2>
    {t_dataprep}

    <figure class="sample">
      <img src="images/data-sample-unsupervised.png" alt="Sample rows of the unlabeled numeric clustering dataset">
      <figcaption><b>Sample.</b> First rows of <code>metro_2025_unsupervised.csv</code>, the 894-metro by 11-feature table clustering runs on (4 of 11 columns shown).
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_unsupervised.csv" target="_blank" rel="noopener">Full file on GitHub &#8599;</a></figcaption>
    </figure>

    <h2>Code</h2>
    <p>Python, using scikit-learn for k-means and SciPy for hierarchical clustering. Hierarchical clustering
    uses <strong>cosine distance</strong> with average linkage; k-means uses Euclidean distance on the same
    standardized features.</p>

    <div class="codeblock">
      <div class="codehead">run_clustering.py<span>k-means sweep &amp; hierarchical, cosine distance</span>
        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/run_clustering.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>
        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>
      </div>
      <div class="code-body">
        <pre><code>k_range = list(range(2, 11))
sil_scores = [silhouette_score(X, KMeans(n_clusters=k, n_init=10,
              random_state=42).fit_predict(X)) for k in k_range]
best_k = k_range[int(np.argmax(sil_scores))]

&#8942;  # hierarchical clustering with cosine distance, the point of this script

Z = linkage(X, method=&quot;average&quot;, metric=&quot;cosine&quot;)
hclust_labels = fcluster(Z, t=hclust_suggested_k, criterion=&quot;maxclust&quot;)
ari = adjusted_rand_score(km_same_k, hclust_labels)</code></pre>
        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>
      </div>
    </div>

    <ul class="linklist">
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/prep_unsupervised_data.py" target="_blank" rel="noopener">prep_unsupervised_data.py</a> <span>: builds the standardized 894&times;11 table from the metro panel</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/run_clustering.py" target="_blank" rel="noopener">run_clustering.py</a> <span>: k-means sweep, hierarchical clustering, comparison figures</span></li>
    </ul>

    <h2>Results</h2>
    {t_results}

    <figure>
      <img src="images/cluster-silhouette-curve.png" alt="Silhouette score by k for k-means">
      <figcaption><b>Figure.</b> Average silhouette score for k-means across nine values of k, from 2 to 10. The score peaks at k = 2 and falls steadily as k grows, meaning additional clusters beyond two do not separate the data any more cleanly.</figcaption>
    </figure>

    <div class="scroll">
      <table>
        <thead><tr><th>k</th><th class="num">Silhouette score</th></tr></thead>
        <tbody>
          <tr><td><strong>2</strong></td><td class="num"><strong>0.433</strong></td></tr>
          <tr><td>3</td><td class="num">0.333</td></tr>
          <tr><td>4</td><td class="num">0.338</td></tr>
          <tr><td>5</td><td class="num">0.271</td></tr>
          <tr><td>6</td><td class="num">0.270</td></tr>
          <tr><td>7</td><td class="num">0.260</td></tr>
          <tr><td>8</td><td class="num">0.259</td></tr>
          <tr><td>9</td><td class="num">0.259</td></tr>
          <tr><td>10</td><td class="num">0.250</td></tr>
        </tbody>
      </table>
    </div>

    <figure>
      <img src="images/cluster-silhouette-plot.png" alt="Per-metro silhouette plot at k=2">
      <figcaption><b>Figure.</b> Per-metro silhouette values at the chosen k = 2. Both clusters sit mostly above the average line with few negative values, meaning few metros are ambiguously placed between the two groups.</figcaption>
    </figure>

    <figure class="wide">
      <img src="images/cluster-kmeans-k-compare.png" alt="k-means clusters compared at k=2, 3 and 6">
      <figcaption><b>Figure.</b> k-means at three different values of k (2, 3 and 6), projected onto the first two principal components. The k = 2 split shown at left is the one the silhouette method prefers; higher k values mostly subdivide the larger, more affordable group rather than finding new structure.</figcaption>
    </figure>

    <figure>
      <img src="images/cluster-dendrogram.png" alt="Hierarchical clustering dendrogram, cosine distance">
      <figcaption><b>Figure.</b> Hierarchical clustering dendrogram, average linkage, cosine distance, all 894 metros. The single tall merge near the top is the largest gap in the tree, and cutting there produces two clusters, the same number the silhouette method chose independently.</figcaption>
    </figure>

    <figure class="wide">
      <img src="images/cluster-kmeans-vs-hclust.png" alt="k-means versus hierarchical clustering at k=2">
      <figcaption><b>Figure.</b> k-means versus hierarchical clustering at the same k = 2. Adjusted Rand Index = 0.74: the two methods, using different distance metrics, largely agree on which metros belong together.</figcaption>
    </figure>

    <div class="scroll">
      <table>
        <thead><tr><th>Cluster</th><th class="num">Metros</th><th class="num">Avg. home value</th><th class="num">Avg. price/income</th><th class="num">Avg. payment % income</th></tr></thead>
        <tbody>
          <tr><td>0, expensive</td><td class="num">196</td><td class="num">$541,934</td><td class="num">9.16</td><td class="num">56.1%</td></tr>
          <tr><td>1, affordable</td><td class="num">698</td><td class="num">$229,315</td><td class="num">3.87</td><td class="num">23.7%</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Conclusions</h2>
    {t_concl}
"""

PCA_BODY = """
    <div class="meta">
      <dl>
        <dt>Category</dt><dd>Unsupervised &middot; dimensionality reduction</dd>
        <dt>Target</dt><dd>None, unsupervised</dd>
        <dt>Data used</dt><dd><code>metro_2025_unsupervised_scaled.csv</code>, 894 metros &times; 11 standardized features</dd>
      </dl>
    </div>

    <h2>Overview</h2>
    {t_overview1}

    <figure>
      <img src="images/theory-pca-direction.png" alt="PCA concept: the first principal component is the direction of maximum variance">
      <figcaption><b>Figure.</b> PCA finds new axes in order of how much variance each one captures. PC1 runs through the long axis of the cloud; PC2 is orthogonal to it and catches most of what PC1 misses.</figcaption>
    </figure>
    <figure>
      <img src="images/theory-dim-reduction.png" alt="Dimensionality reduction concept: projecting many features onto one principal component">
      <figcaption><b>Figure.</b> Dimensionality reduction. Points that originally need several axes to describe can be projected onto just the first component and still keep most of their relative spread.</figcaption>
    </figure>

    {t_overview2}

    <h2>Data Prep</h2>
    {t_dataprep}

    <figure class="sample">
      <img src="images/data-sample-unsupervised.png" alt="Sample rows of the unlabeled numeric PCA dataset">
      <figcaption><b>Sample.</b> First rows of <code>metro_2025_unsupervised.csv</code>, the same 894-metro by 11-feature table used for clustering (4 of 11 columns shown).
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_unsupervised.csv" target="_blank" rel="noopener">Full file on GitHub &#8599;</a></figcaption>
    </figure>

    <h2>Code</h2>
    <p>Python, using scikit-learn's <code>PCA</code> on the standardized features. <code>explained_variance_</code>
    and <code>components_</code> are exactly the eigenvalues and eigenvectors of the feature correlation matrix
    once the inputs are standardized.</p>

    <div class="codeblock">
      <div class="codehead">run_pca.py<span>eigenvalues, loadings, scree plot, biplot</span>
        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/run_pca.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>
        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>
      </div>
      <div class="code-body">
        <pre><code>pca = PCA(n_components=11, random_state=42)
coords = pca.fit_transform(X)

eigenvalues  = pca.explained_variance_       # eigenvalues of the correlation matrix
eigenvectors = pca.components_               # rows are eigenvectors (loadings)
explained    = pca.explained_variance_ratio_
cum_explained = np.cumsum(explained)

&#8942;  # scree plot of eigenvalues, then a biplot of PC1/PC2 with variable loadings</code></pre>
        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>
      </div>
    </div>

    <ul class="linklist">
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/prep_unsupervised_data.py" target="_blank" rel="noopener">prep_unsupervised_data.py</a> <span>: builds the standardized 894&times;11 table from the metro panel</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/run_pca.py" target="_blank" rel="noopener">run_pca.py</a> <span>: eigen-decomposition, scree plot, biplot</span></li>
    </ul>

    <h2>Results</h2>
    {t_results}

    <figure>
      <img src="images/pca-scree.png" alt="Scree plot of eigenvalues by principal component">
      <figcaption><b>Figure.</b> Scree plot: percent of variance explained by each of the 11 components (bars) and the cumulative total (line). The curve bends sharply after component 2 and flattens near zero after component 5, the signature of a handful of collinear features rather than eleven independent ones.</figcaption>
    </figure>

    <div class="scroll">
      <table>
        <thead><tr><th>Component</th><th class="num">% variance</th><th class="num">Cumulative %</th></tr></thead>
        <tbody>
          <tr><td>PC1</td><td class="num">63.0</td><td class="num">63.0</td></tr>
          <tr><td>PC2</td><td class="num">24.2</td><td class="num">87.2</td></tr>
          <tr><td>PC3</td><td class="num">7.6</td><td class="num"><strong>94.8</strong></td></tr>
          <tr><td>PC4</td><td class="num">2.5</td><td class="num">97.3</td></tr>
          <tr><td>PC5</td><td class="num">2.4</td><td class="num">99.7</td></tr>
          <tr><td>PC6&ndash;PC11</td><td class="num">&lt;0.3 each</td><td class="num">100.0</td></tr>
        </tbody>
      </table>
    </div>

    <figure>
      <img src="images/pca-biplot.png" alt="Biplot of metro areas and variable loadings on PC1 and PC2">
      <figcaption><b>Figure.</b> Biplot: each point is a metro, projected onto PC1 and PC2; each arrow is one of the 11 original features, pointing in the direction it increases. Six features point almost identically along PC1, direct confirmation that they are measuring close to the same thing, while the price-change variables point in a separate direction along PC2.</figcaption>
    </figure>

    <div class="scroll">
      <table>
        <thead><tr><th>Feature</th><th class="num">PC1 loading</th><th class="num">PC2 loading</th></tr></thead>
        <tbody>
          <tr><td>Home value</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Price vs. national</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Price-to-income</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Years to down payment</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Monthly payment</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Payment % income</td><td class="num">0.378</td><td class="num">0.001</td></tr>
          <tr><td>Price percentile</td><td class="num">0.326</td><td class="num">0.060</td></tr>
          <tr><td>5yr price change</td><td class="num">0.120</td><td class="num">0.439</td></tr>
          <tr><td>Price volatility</td><td class="num">0.153</td><td class="num">-0.376</td></tr>
          <tr><td>3yr price change</td><td class="num">-0.003</td><td class="num">0.599</td></tr>
          <tr><td>1yr price change</td><td class="num">-0.026</td><td class="num">0.551</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Conclusions</h2>
    {t_concl}
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
      <img src="images/about-portrait.jpg" alt="Anjana Anand">
      <div>
        <h4>Anjana Anand</h4>
        <p class="role">MS Data Science Student, CU Boulder</p>
        <p>Anjana Anand is a graduate student in the Data Science program at CU Boulder,
        graduating in May 2027. She completed her BTech in AI and Data Science before moving
        to Boulder for her master's. She has worked on projects in NLP, computer vision, and
        time-series financial modeling. Outside the classroom, Anjana enjoys staying active
        and watching movies.</p>
        <p><a href="https://www.linkedin.com/in/anjana-anand-b63076398" target="_blank" rel="noopener">LinkedIn</a> &middot; <a href="https://github.com/anjana5anand" target="_blank" rel="noopener">GitHub</a></p>
      </div>
    </div>
"""


def nav(current):
    out = []
    for href, label, _sub, group in PAGES:
        if href == "eda.html":
            continue  # emitted together with dataprep.html, below
        if href == "dataprep.html":
            out.append('        <p class="group">{}</p>'.format(group))
            is_open = current in ("dataprep.html", "eda.html")
            out.append('        <details class="nav-group"{}>'.format(' open' if is_open else ''))
            out.append('          <summary>Data Prep &amp; EDA</summary>')
            for sub_href, sub_label in (("dataprep.html", "Data Prep"), ("eda.html", "EDA")):
                sub_cls = ' class="active"' if sub_href == current else ''
                out.append('          <a href="{}"{}>{}</a>'.format(sub_href, sub_cls, sub_label))
            out.append('        </details>')
            continue
        if group:
            out.append('        <p class="group">{}</p>'.format(group))
        cls = ' class="active"' if href == current else ''
        out.append('        <a href="{}"{}>{}</a>'.format(href, cls, label))
    return "\n".join(out)


def page(href, label, subtitle, body, show_title=True):
    title_block = (
        "      <h1>{label}</h1>\n      <p class=\"subtitle\">{subtitle}</p>\n      <hr class=\"rule-under\">\n"
        if show_title else ""
    ).format(label=label, subtitle=subtitle)
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
{title_block}{body}
    </main>

  </div>

  <script src="assets/ui.js" defer></script>
</body>
</html>
""".format(label=label, site=SITE_TITLE, sub=SITE_SUB, navlinks=nav(href),
           subtitle=subtitle, body=body, repo=REPO_URL, title_block=title_block)


figslots = '      <figure>\n        <a href="images/eda-01-large.png"><img src="images/eda-01.png" alt="Homeownership rate by age of householder, 1982 to 2025"></a>\n        <figcaption><b>Figure 12.</b> Homeownership rate by age of householder, 1982 to 2025. All three brackets peak in the mid 2000s and fall sharply through 2016. The 25 to 29 and 30 to 34 brackets remain well below their pre-2008 levels more than fifteen years later, while the under 25 bracket sits slightly above where it began.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-02-large.png"><img src="images/eda-02.png" alt="The twelve least affordable metropolitan areas, 2025"></a>\n        <figcaption><b>Figure 13.</b> The twelve least affordable metropolitan areas, 2025. San Jose tops the list at 27.1 times annual earnings, with Vineyard Haven and Jackson above 23. In these markets a typical home costs more than two decades of a young worker\'s entire gross pay.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-03-large.png"><img src="images/eda-03.png" alt="Correlation between national measures, 2000 to 2025"></a>\n        <figcaption><b>Figure 14.</b> Correlation between national measures, 2000 to 2025. The mortgage rate correlates with the payment burden at 0.78, more strongly than price-to-income does at 0.71. This is the numeric form of the argument that price alone does not determine affordability.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-04-large.png"><img src="images/eda-04.png" alt="Where the 894 metropolitan areas are, by state"></a>\n        <figcaption><b>Figure 15.</b> Where the 894 metropolitan areas are, by state. Texas contributes 67 metropolitan areas and Ohio 44, with the eight largest states accounting for 36 percent of the total. Coverage is uneven, so any unweighted national average leans toward these states.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-05-large.png"><img src="images/eda-05.png" alt="Affordability quartile membership by year"></a>\n        <figcaption><b>Figure 16.</b> Affordability quartile membership by year. Quartiles are recomputed within each year, so the four bands are equal by construction and the visible change is coverage. Zillow reported 444 metropolitan areas in 2000 and 894 in 2025, which matters when comparing distributions across years.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-06-large.png"><img src="images/eda-06.png" alt="Did expensive markets in 2000 grow faster since?"></a>\n        <figcaption><b>Figure 17.</b> Did expensive markets in 2000 grow faster since?. Across the 444 metros reported in both years the relationship is weakly positive, Pearson r = 0.30, with growth ranging from 38 to 505 percent. Starting price explains only a small part of what happened next, so expensive markets did not simply run away from cheap ones.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-07-large.png"><img src="images/eda-07.png" alt="Spread of metropolitan affordability, selected years"></a>\n        <figcaption><b>Figure 18.</b> Spread of metropolitan affordability, selected years. The median metro moved from 3.67 times earnings in 2000 to 4.25 in 2025, while the interquartile range widened from 2.98-4.75 to 3.21-5.93. The typical market worsened modestly; the spread between markets worsened considerably more.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-08-large.png"><img src="images/eda-08.png" alt="Metropolitan areas per state, shaded by median home value, 2025"></a>\n        <figcaption><b>Figure 19.</b> Metropolitan areas per state, shaded by median home value, 2025. Area shows how many metropolitan areas each state contains and shade shows the median home value among them. Hawaii and Massachusetts are small in count but darkest in value, while Texas and Ohio are large in count and light.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-09-large.png"><img src="images/eda-09.png" alt="Affordability within the twelve states with the most metros, 2025"></a>\n        <figcaption><b>Figure 20.</b> Affordability within the twelve states with the most metros, 2025. Median price-to-income runs from 2.72 in Illinois to 8.12 in California, and the width of each shape shows that states differ internally as much as they differ from one another. A state-level average would hide most of this.</figcaption>\n      </figure>\n      <figure>\n        <a href="images/eda-10-large.png"><img src="images/eda-10.png" alt="Is metropolitan affordability normally distributed?"></a>\n        <figcaption><b>Figure 21.</b> Is metropolitan affordability normally distributed?. The points bend away from the fitted line in the upper tail and the distribution carries a skewness of 2.76. Affordability is strongly right-skewed, which argues for a log transform or rank-based methods in the modelling sections rather than assuming normality.</figcaption>\n      </figure>'

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
            )
        elif href == "dataprep.html":
            body = DATAPREP_BODY.format(
                sources=COPY['PREP_SOURCES'],
                t_collect=COPY['PREP_COLLECT'],
                t_downloads=COPY['PREP_DOWNLOADS'],
                t_dataset=COPY['INTRO_DATASET'],
            )
        elif href == "eda.html":
            body = EDA_BODY.format(
                figslots=figslots,
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
        elif href == "clustering.html":
            body = CLUSTERING_BODY.format(
                t_overview1=COPY['CLUSTER_OVERVIEW_1'],
                t_overview2=COPY['CLUSTER_OVERVIEW_2'],
                t_dataprep=COPY['CLUSTER_DATAPREP'],
                t_results=COPY['CLUSTER_RESULTS'],
                t_concl=COPY['CLUSTER_CONCL'],
            )
        elif href == "pca.html":
            body = PCA_BODY.format(
                t_overview1=COPY['PCA_OVERVIEW_1'],
                t_overview2=COPY['PCA_OVERVIEW_2'],
                t_dataprep=COPY['PCA_DATAPREP'],
                t_results=COPY['PCA_RESULTS'],
                t_concl=COPY['PCA_CONCL'],
            )
        else:
            body = MODEL_BODY.format(
                slug=slug,
                t_why=todo("Why this method suits this question, in your own words."),
                t_assume=todo("What this model assumes about the data, and whether the data actually meets those assumptions."),
                t_prep=todo("What this method requires that the others do not, and what was done to meet it."),
                t_concl=todo("What the results mean for the homeownership question. Not a restatement of the metrics."),
            )
        with open(href, "w") as f:
            f.write(page(href, label, subtitle, body, show_title=(href != "index.html")))
        print("wrote", href)


if __name__ == "__main__":
    build_all()
