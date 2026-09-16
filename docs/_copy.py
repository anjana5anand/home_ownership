# Draft prose. Written to be rewritten - Anjana's voice should replace this.
# Third person throughout: no "I", "me", "my".

INTRO_TOPIC = """
    <p>Homeownership remains the largest single component of wealth for most American households, and the
    age at which a household buys its first home shapes how much wealth it eventually accumulates. Over the
    past two decades that first purchase has moved steadily further out of reach for people in their twenties
    and early thirties. Census Housing Vacancy Survey figures show that among householders aged 25 to 29, the
    homeownership rate fell from 41.8 percent in 2006 to 30.9 percent in 2016, recovering only to 33.3 percent
    by 2025. Householders aged 30 to 34 followed the same path, from 57.4 percent down to 45.4 percent and
    back to 46.6 percent. Neither group has returned to where it stood before the 2008 financial crisis, more
    than fifteen years later. Across the same period the typical American home rose in value from roughly
    $132,000 to $370,000.</p>

    <p>The familiar explanation is that wages failed to keep pace with prices, and the nominal figures appear
    to confirm it. Median earnings for full-time workers aged 25 to 34 rose from $28,561 to $59,176 between
    2000 and 2025, which looks like a doubling of purchasing power. Adjusted for inflation, the same earnings
    move from $53,403 to $55,435 between 2000 and 2019, a gain of under four percent across nineteen
    years, before rising to $59,176 by 2025. The purchasing power of a young worker's paycheck was
    therefore close to flat for almost two decades while the price of the asset that worker was trying to buy
    nearly tripled. Ratios tell the same story from another angle: the price of a typical home rose from 4.6
    times a young worker's annual earnings in 2000 to 6.3 times in 2025. What that ratio conceals is the cost
    of borrowing, which moved in the opposite direction for most of the period and then reversed sharply, and
    which turns out to matter more than price alone.</p>
"""

INTRO_STAKE = """
    <p>The most directly affected group is the roughly one in three Americans aged 25 to 34 who rent and would
    prefer to own. For them the question is not abstract: the gap between renting and owning determines whether
    monthly housing costs build equity or disappear, and delay compounds, since a purchase postponed by ten
    years is ten years of equity never accumulated. Their parents are affected in turn, as families increasingly
    supply down-payment assistance that turns a market outcome into an inherited one, widening the distance
    between households that can offer such help and those that cannot.</p>

    <p>Lenders and homebuilders have a commercial stake in the same figures, since first-time buyers are the
    entry point to the housing market and a shrinking cohort of them constrains transaction volume throughout
    the chain. Municipal and state governments have a fiscal and practical stake: property taxes fund local
    services, and metropolitan areas where young workers cannot afford to buy face difficulty retaining
    teachers, nurses and other essential workers. Housing policy makers need to know whether the constraint is
    price, income, credit cost, or supply, because each points to a different intervention: zoning reform,
    down-payment assistance, interest-rate policy, or construction subsidy. Answering that question requires
    separating the components rather than treating affordability as a single number.</p>
"""

INTRO_GAPS = """
    <p>Tools for assessing housing affordability are widely available and mostly answer a narrow question.
    Mortgage calculators published by Zillow, NerdWallet and most retail banks tell an individual household
    what it can afford today, at today's rates, given today's income. They are useful for a decision and
    useless for a trend: they describe one household at one moment and say nothing about how the situation
    has changed or how it differs between places. Industry reporting fills part of that gap. The National
    Association of Realtors publishes an annual profile of home buyers and sellers, and Harvard's Joint Center
    for Housing Studies produces the <em>State of the Nation's Housing</em> series, both tracking first-time
    buyer age and homeownership rates over time.</p>

    <p>Research on why young-adult homeownership fell has concentrated on demographic explanation. A Joint
    Center analysis attributed part of the decline to later marriage, changing household composition and
    migration toward central cities, but concluded that demographic factors account for only about a quarter
    of the variation in whether a household owns or rents, leaving macroeconomic conditions and price as the
    larger share of the explanation. That leaves two gaps this project addresses. The first is that most
    public treatments measure affordability as a price-to-income ratio and ignore the cost of borrowing
    entirely, which is a serious omission: in 2021 the price-to-income ratio stood near a record 6.6 while the
    share of income required to service a mortgage was a moderate 26.5 percent, because money cost 2.96
    percent; by 2023 that share reached 41.5 percent, worse than the 2006 housing-bubble peak of 39.7 percent,
    on a price-to-income ratio that had barely moved. The second is that national aggregates conceal the
    geography almost entirely. In 2025 the price of a typical home ranged from 0.81 times a young worker's
    annual earnings in Helena, Arkansas to 27.1 times in San Jose, California, a spread across 894
    metropolitan areas that no national average can represent.</p>
"""

INTRO_BLUEPRINT = """
    <figure class="flow">
      <svg viewBox="0 0 960 300" role="img"
           aria-label="Project pipeline: three sources are collected, cleaned by three different transformations, engineered into two analysis tables, passed through two unsupervised and five supervised model families, and used to answer the ten research questions.">
        <defs>
          <marker id="fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
            <polygon points="0,1 9,5 0,9" fill="var(--accent)"/>
          </marker>
        </defs>

        <!-- stage headers -->
        <g font-family="var(--mono)" font-size="10" font-weight="700" letter-spacing="1.2" fill="var(--accent)">
          <text x="10"  y="22">01 &#183; COLLECT</text>
          <text x="210" y="22">02 &#183; CLEAN</text>
          <text x="410" y="22">03 &#183; ENGINEER</text>
          <text x="610" y="22">04 &#183; MODEL</text>
          <text x="810" y="22">05 &#183; ANSWER</text>
        </g>
        <g stroke="var(--rule)" stroke-width="1">
          <line x1="10"  y1="30" x2="175" y2="30"/>
          <line x1="210" y1="30" x2="375" y2="30"/>
          <line x1="410" y1="30" x2="575" y2="30"/>
          <line x1="610" y1="30" x2="775" y2="30"/>
          <line x1="810" y1="30" x2="950" y2="30"/>
        </g>

        <g font-size="11.5" fill="var(--ink)">
          <!-- 01 collect -->
          <rect x="10" y="100" width="165" height="26" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="20" y="117">Census HVS &#183; .xlsx</text>
          <rect x="10" y="132" width="165" height="26" rx="5" fill="var(--accent-wash)" stroke="var(--accent)"/>
          <text x="20" y="149" font-weight="650" fill="var(--accent)">FRED &#183; API</text>
          <rect x="10" y="164" width="165" height="26" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="20" y="181">Zillow ZHVI &#183; .csv</text>

          <!-- 02 clean -->
          <rect x="210" y="100" width="165" height="26" rx="5" fill="var(--panel)" stroke="var(--rule)"/>
          <text x="220" y="117">parse year-blocks</text>
          <rect x="210" y="132" width="165" height="26" rx="5" fill="var(--panel)" stroke="var(--rule)"/>
          <text x="220" y="149">collapse to annual</text>
          <rect x="210" y="164" width="165" height="26" rx="5" fill="var(--panel)" stroke="var(--rule)"/>
          <text x="220" y="181">reshape wide &#8594; long</text>

          <!-- 03 engineer -->
          <rect x="410" y="94" width="165" height="38" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="420" y="110">national_annual</text>
          <text x="420" y="125" font-size="10" fill="var(--muted)">26 rows &#215; 23 cols</text>
          <rect x="410" y="138" width="165" height="38" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="420" y="154">metro_year_panel</text>
          <text x="420" y="169" font-size="10" fill="var(--muted)">19,288 rows &#215; 25 cols</text>
          <text x="410" y="196" font-size="10" fill="var(--muted)">+ price-to-income, payment</text>
          <text x="410" y="209" font-size="10" fill="var(--muted)">burden, growth, volatility</text>

          <!-- 04 model -->
          <text x="610" y="52" font-size="9.5" font-weight="700" letter-spacing=".9" fill="var(--muted)">UNSUPERVISED</text>
          <rect x="610" y="58" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="74">Clustering</text>
          <rect x="610" y="86" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="102">PCA</text>

          <text x="610" y="130" font-size="9.5" font-weight="700" letter-spacing=".9" fill="var(--muted)">SUPERVISED</text>
          <rect x="610" y="136" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="152">Naive Bayes</text>
          <rect x="610" y="164" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="180">Decision Trees</text>
          <rect x="610" y="192" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="208">SVMs</text>
          <rect x="610" y="220" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="236">Regression</text>
          <rect x="610" y="248" width="165" height="24" rx="5" fill="var(--surface)" stroke="var(--rule)"/>
          <text x="620" y="264">Neural Networks</text>

          <!-- 05 answer -->
          <rect x="810" y="110" width="140" height="70" rx="6" fill="var(--accent-wash)" stroke="var(--accent)" stroke-width="1.6"/>
          <text x="880" y="140" text-anchor="middle" font-size="24" font-weight="650" fill="var(--accent)" font-family="var(--serif)">10</text>
          <text x="880" y="160" text-anchor="middle" font-size="11" fill="var(--accent)">research</text>
          <text x="880" y="173" text-anchor="middle" font-size="11" fill="var(--accent)">questions</text>
        </g>

        <!-- stage arrows -->
        <g stroke="var(--accent)" stroke-width="1.4" fill="none" marker-end="url(#fa)">
          <line x1="180" y1="145" x2="205" y2="145"/>
          <line x1="380" y1="145" x2="405" y2="145"/>
          <line x1="580" y1="145" x2="605" y2="145"/>
          <line x1="780" y1="145" x2="805" y2="145"/>
        </g>
      </svg>
      <figcaption><b>Figure 2.</b> The project pipeline from raw file to answered question. Only the FRED
      series arrive through an API; the other two sources are published as files, and all three need a
      different transformation before they can be joined on year.</figcaption>
    </figure>

    <p>The project proceeds in four stages. Collection draws on three sources: the Census Housing Vacancy
    Survey for homeownership by age of householder, the Federal Reserve Bank of St. Louis FRED API for
    earnings, mortgage rates, prices and inflation, and the Zillow Home Value Index for home values at
    metropolitan level. Cleaning reshapes each into tidy tables, which is non-trivial because none of the
    three arrives in an analysable form. The Census workbook repeats an entire year-block down the
    sheet, the FRED series arrive at three different frequencies, and the Zillow file is 319 columns wide.</p>

    <p>Feature engineering follows, producing the measures the analysis depends on: price-to-income,
    years required to save a down payment, monthly mortgage payment, and payment as a share of income,
    together with growth, volatility and rank measures computed for each metropolitan area. Modelling then
    addresses the research questions above in two groups. Unsupervised methods, clustering and
    principal component analysis, ask whether housing markets fall into recognisable types and which
    characteristics separate them. Supervised methods, naive Bayes, decision trees, support vector
    machines, regression and neural networks, ask whether a market's affordability can be predicted
    from its price behaviour, and which features carry that prediction. Each model is reported with its
    assumptions, the parameters explored, and an honest account of what its results do and do not establish.</p>
"""

INTRO_DATASET = """
    <p>Three sources were selected, each covering something the others cannot. The Census Housing Vacancy
    Survey provides the dependent variable of interest, homeownership by age of householder, and does so from
    1982 onward with age brackets narrow enough to separate 25-to-29-year-olds from 30-to-34-year-olds. That
    distinction matters, because the two groups sit on opposite sides of the typical first purchase and
    coarser sources that report a single &ldquo;under 35&rdquo; figure blur them together. The FRED API supplies
    the economic context: median weekly earnings by age bracket, the 30-year fixed mortgage rate, the national
    homeownership rate, median sales price, the Case&ndash;Shiller index, the Consumer Price Index and housing
    starts. Retrieving these programmatically rather than by download makes the collection reproducible and
    made it practical to add the mortgage-rate and inflation series that the affordability analysis turns on.
    The Zillow Home Value Index contributes the geographic dimension, reporting a typical home value for 894
    metropolitan areas every month since 2000.</p>

    <p>Several limitations follow from these choices and are carried through the analysis. None of the three
    sources is individual-level, so the project describes aggregate rates rather than the circumstances of
    particular households. Earnings are reported nationally rather than by metropolitan area, which means
    metro-level affordability measures compare local prices against a national income and cannot capture the
    fact that salaries in San Jose differ from salaries in Cleveland. The Zillow index covers the middle
    tier of the market, between the 33rd and 67th percentiles of value, and therefore excludes both the
    cheapest and most expensive segments. Homeownership figures are reported for the age of the householder
    rather than of every occupant, so a 27-year-old living in a parent's home is counted under that parent's
    age. Each of these is a genuine constraint on what the results can support, and each is noted again where
    it bears on a specific finding.</p>
"""

PREP_COLLECT = """
    <p>Data collection combined one programmatic source with two direct downloads, chosen so that each
    covered a dimension the others lacked: time depth from the Census survey, economic context from FRED,
    and geographic detail from Zillow. The FRED series were retrieved through the API described below, which
    returned 2,771 individual observations across eight series and saved each raw response to disk so that
    the collection step is auditable and repeatable. The two downloaded sources were taken from their
    publishers' own distribution pages rather than from any secondary aggregator, so that the files used
    here are the files those organisations publish.</p>
"""

PREP_DOWNLOADS = """
    <p>The Census Housing Vacancy Survey historical tables are published as Excel workbooks on the Census
    Bureau's website. Table 12 was used, which reports total households and owner-occupied households by age
    of householder annually from 1982. It was chosen over the Bureau's quarterly tables because those report
    a single combined figure for householders under 35, while Table 12 separates the age brackets this project
    depends on. The Zillow Home Value Index is published as a comma-separated file on Zillow's research
    portal. The metropolitan file for the middle price tier was used, giving a smoothed, seasonally adjusted
    typical home value for each of 894 metropolitan areas for every month since January 2000.</p>
"""

PREP_RAW = """
    <p>None of the three sources arrives in a form that can be analysed directly. The Census workbook is
    formatted for a human reader rather than a program: instead of one table with a year column, it repeats
    an entire block (a header row reading &ldquo;Age of Householder&rdquo;, then paired total and owner
    columns for several years) down the length of the sheet, so a parser has to locate each block,
    read the pairs beneath it, and reconcile years that appear more than once because the Bureau revises
    earlier estimates. Row labels carry trailing dot leaders and footnote letters that must be stripped
    before they can be matched.</p>

    <p>The FRED responses are clean JSON but arrive at three different frequencies (weekly for mortgage
    rates, monthly for the price and inflation indices, quarterly for earnings and the homeownership rate)
    and mark missing readings with the string &ldquo;.&rdquo; rather than a null value, which silently
    becomes text in any column read without care. The Zillow file is the opposite problem: technically clean,
    but 895 rows by 324 columns, with one column per month rather than one row per observation.</p>
"""

PREP_STEPS = """
    <p>Each source required a different transformation. The Census workbook was parsed block by block,
    extracting the age brackets of interest, stripping label formatting, and keeping the most recent estimate
    wherever a year appeared in more than one block; ownership rates were then computed as owner households
    divided by total households. The FRED observations were averaged within each calendar year to produce
    annual figures, weekly earnings were converted to annual by multiplying by 52, and earnings were
    additionally expressed in constant 2025 dollars using the Consumer Price Index so that real and nominal
    trends could be compared. The Zillow file was reshaped from wide to long, and the latest month reported
    in each year was taken as that year's value for each metropolitan area.</p>

    <p>One cleaning problem deserves specific mention because it failed silently rather than raising an error.
    The Zillow file's national row carries an empty state field, and grouping the reshaped data by its
    identifying columns discarded that row by default, since pandas excludes rows with missing grouping keys
    unless instructed otherwise. The national series disappeared, the subsequent join produced an empty table,
    and no exception was raised at any point. The fix was explicit, but the episode is the clearest argument
    in this project for checking row counts after every merge rather than trusting that a step succeeded
    because it did not crash.</p>
"""

PREP_EDA = """
    <p>Exploration of the cleaned tables shows a pattern more complicated than steady decline. Homeownership
    among young householders rises to a peak in the mid-2000s, collapses through the following decade, and
    recovers only partially, leaving both the 25-to-29 and 30-to-34 brackets well below where they stood
    before 2008. Affordability, measured as the share of income required to service a mortgage on a typical
    home, does not decline steadily either: it is worst in 2023 at 41.5 percent, better than at any point in
    the series in 2012 at 20.0 percent, and roughly equal in 2000 and 2019. The figures below examine each
    component in turn, ownership by age, earnings in nominal and real terms, prices, interest rates,
    and the geographic distribution across metropolitan areas, before the modelling sections take up
    the questions that require more than description.</p>

    <p>One result in the exploration runs against expectation and is worth stating plainly. Homeownership
    among householders under 25 rose over the period, from 21.7 percent in 2000 to 24.2 percent in 2025,
    while every older young-adult bracket fell. The most likely explanation is compositional rather than
    economic: if fewer people under 25 form independent households at all, those who do are drawn
    disproportionately from those able to buy. The data assembled here can establish that the divergence
    exists but cannot confirm the mechanism, and the finding is treated accordingly.</p>
"""


PREP_SOURCES = '\n    <h2><span class="srcnum">01</span>Census Housing Vacancy Survey, Table 12</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-hvs.png" alt="Raw sample of Census Housing Vacancy Survey, Table 12">\n      <figcaption><b>Figure 3.</b> The first fourteen rows of the workbook as published. Column headers sit several rows down, shaded cells are structurally blank rather than missing, and the whole year-block repeats further down the sheet for earlier years.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Locate each repeating <code>Age of Householder</code> block and read the paired total and owner columns beneath it.</li>\n      <li>Strip trailing dot leaders and footnote letters from row labels before they can be matched.</li>\n      <li>Resolve years that appear in more than one block, keeping the later revised estimate.</li>\n      <li>Convert counts stored as text into numbers.</li>\n      <li>Compute the ownership rate, which the file does not contain, as owner households divided by total households.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-hvs.png" alt="Cleaned output for Census Housing Vacancy Survey, Table 12">\n      <figcaption><b>Figure 4.</b> The result: one row per year and age bracket, with the rate computed. 220 rows covering 1982 to 2025 across five age brackets.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>parse_histtab12()</span></div>\n      <pre><code>def parse_histtab12(path=f&quot;{RAW}/histtab12.xlsx&quot;):\n    import openpyxl\n    ws = openpyxl.load_workbook(path, data_only=True)[&quot;Sheet1&quot;]\n    rows = list(ws.iter_rows(values_only=True))\n\n    targets = {&quot;less than 25 years&quot;: &quot;&lt;25&quot;, &quot;25 to 29 years&quot;: &quot;25-29&quot;,\n               &quot;30 to 34 years&quot;: &quot;30-34&quot;, &quot;35 to 39 years&quot;: &quot;35-39&quot;,\n               &quot;40 to 44 years&quot;: &quot;40-44&quot;}\n\n    records, i, n = [], 0, len(rows)\n    while i &lt; n:\n        if rows[i][0] and str(rows[i][0]).strip() == &quot;Age of Householder&quot;:\n            header = rows[i]\n            years = [(c, re.sub(r&quot;[a-zA-Z]&quot;, &quot;&quot;, str(header[c])))\n                     for c in range(1, len(header), 2) if header[c] is not None]\n            j = i + 3\n            while j &lt; n and not (rows[j][0] and str(rows[j][0]).strip() == &quot;Age of Householder&quot;):\n                label = clean_label(rows[j][0]) if rows[j][0] else None\n                if label:\n                    key = label.lower()\n                    for tlabel, code in targets.items():\n                        if tlabel in key:\n                            for col, y in years:\n                                total = rows[j][col] if col &lt; len(rows[j]) else None\n                                owner = rows[j][col + 1] if col + 1 &lt; len(rows[j]) else None\n                                if total is not None:\n                                    records.append((y, code, total, owner))\n                j += 1\n            i = j\n        else:\n            i += 1\n\n    df = pd.DataFrame(records, columns=[&quot;year_raw&quot;, &quot;age_bracket&quot;, &quot;total&quot;, &quot;owner&quot;])\n    df[&quot;year&quot;] = pd.to_numeric(df[&quot;year_raw&quot;].str.extract(r&quot;(\\d{4})&quot;)[0], errors=&quot;coerce&quot;)\n    df = df.dropna(subset=[&quot;year&quot;])\n    df[&quot;year&quot;] = df[&quot;year&quot;].astype(int)\n    # revised vintages repeat a year; the later block supersedes the earlier one\n    df = df.drop_duplicates(subset=[&quot;year&quot;, &quot;age_bracket&quot;], keep=&quot;last&quot;)\n    df[&quot;total&quot;] = pd.to_numeric(df[&quot;total&quot;], errors=&quot;coerce&quot;)\n    df[&quot;owner&quot;] = pd.to_numeric(df[&quot;owner&quot;], errors=&quot;coerce&quot;)\n    df[&quot;ownership_rate_pct&quot;] = (df[&quot;owner&quot;] / df[&quot;total&quot;] * 100).round(2)\n    df = df[[&quot;year&quot;, &quot;age_bracket&quot;, &quot;total&quot;, &quot;owner&quot;, &quot;ownership_rate_pct&quot;]]\n    df.columns = [&quot;year&quot;, &quot;age_bracket&quot;, &quot;total_households_thousands&quot;,\n                  &quot;owner_households_thousands&quot;, &quot;ownership_rate_pct&quot;]\n    return df.sort_values([&quot;year&quot;, &quot;age_bracket&quot;]).reset_index(drop=True)</code></pre>\n    </div>\n\n    <h2><span class="srcnum">02</span>BLS and Census via the FRED API</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-fred.png" alt="Raw sample of BLS and Census via the FRED API">\n      <figcaption><b>Figure 5.</b> Six observations from the MORTGAGE30US response. The series is weekly, and two realtime columns record when the figure was published rather than anything about housing.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Collapse eight series arriving weekly, monthly and quarterly onto a single annual grain.</li>\n      <li>Drop <code>realtime_start</code> and <code>realtime_end</code>, which carry no analytical information.</li>\n      <li>Treat the string <code>&quot;.&quot;</code> as missing, since reading it as a value turns the whole column into text.</li>\n      <li>Convert median weekly earnings to an annual figure.</li>\n      <li>Deflate nominal dollars to constant 2025 terms using the Consumer Price Index.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-fred.png" alt="Cleaned output for BLS and Census via the FRED API">\n      <figcaption><b>Figure 6.</b> The result: one row per year with every series on the same grain, four of thirteen columns shown. 2,771 raw observations reduce to 27 annual rows.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">fred_api_fetch.py<span>fetch_series()</span></div>\n      <pre><code>def fetch_series(series_id, key):\n    &quot;&quot;&quot;Return (metadata_dict, {year: [values]}).&quot;&quot;&quot;\n    meta_payload = api_get(&quot;series&quot;, {&quot;series_id&quot;: series_id, &quot;api_key&quot;: key, &quot;file_type&quot;: &quot;json&quot;})\n    meta = {}\n    if meta_payload and meta_payload.get(&quot;seriess&quot;):\n        s = meta_payload[&quot;seriess&quot;][0]\n        meta = {\n            &quot;series_id&quot;: series_id,\n            &quot;title&quot;: s.get(&quot;title&quot;),\n            &quot;units&quot;: s.get(&quot;units&quot;),\n            &quot;frequency&quot;: s.get(&quot;frequency&quot;),\n            &quot;seasonal_adjustment&quot;: s.get(&quot;seasonal_adjustment&quot;),\n            &quot;last_updated&quot;: s.get(&quot;last_updated&quot;),\n        }\n\n    obs = api_get(&quot;series/observations&quot;, {\n        &quot;series_id&quot;: series_id, &quot;api_key&quot;: key, &quot;file_type&quot;: &quot;json&quot;,\n        &quot;observation_start&quot;: START,\n    })\n    if not obs:\n        return meta, {}\n\n    os.makedirs(RAW_DIR, exist_ok=True)\n    with open(&quot;{}/{}.json&quot;.format(RAW_DIR, series_id), &quot;w&quot;) as f:\n        json.dump(obs, f)\n\n    by_year = defaultdict(list)\n    for o in obs.get(&quot;observations&quot;, []):\n        if o[&quot;value&quot;] in (&quot;.&quot;, &quot;&quot;, None):\n            continue                      # FRED marks missing readings with &quot;.&quot;\n        by_year[int(o[&quot;date&quot;][:4])].append(float(o[&quot;value&quot;]))\n    return meta, by_year</code></pre>\n    </div>\n\n    <h2><span class="srcnum">03</span>Zillow Home Value Index, metro</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-zhvi.png" alt="Raw sample of Zillow Home Value Index, metro">\n      <figcaption><b>Figure 7.</b> The file in its published shape, 895 rows by 324 columns. Eight columns are shown here; 313 further month columns continue to the right.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Reshape 319 month columns into rows, so each observation occupies one row.</li>\n      <li>Reduce each metro-year to a single value, taking the latest month reported in that year.</li>\n      <li>Fill the empty <code>StateName</code> on the national row, which a default groupby silently discards.</li>\n      <li>Separate the country row from the 894 metropolitan rows, since they feed different tables.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-zhvi.png" alt="Cleaned output for Zillow Home Value Index, metro">\n      <figcaption><b>Figure 8.</b> The result: one row per metropolitan area per year. The wide file becomes 20,209 long rows covering 2000 to 2026.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>parse_zhvi()</span></div>\n      <pre><code>def parse_zhvi(path=f&quot;{RAW}/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv&quot;):\n    wide = pd.read_csv(path)\n    id_cols = [&quot;RegionID&quot;, &quot;SizeRank&quot;, &quot;RegionName&quot;, &quot;RegionType&quot;, &quot;StateName&quot;]\n    date_cols = [c for c in wide.columns if c not in id_cols]\n\n    long = wide.melt(id_vars=id_cols, value_vars=date_cols,\n                     var_name=&quot;month&quot;, value_name=&quot;zhvi&quot;).dropna(subset=[&quot;zhvi&quot;])\n    long[&quot;year&quot;] = long[&quot;month&quot;].str.slice(0, 4).astype(int)\n    long[&quot;month_num&quot;] = long[&quot;month&quot;].str.slice(5, 7).astype(int)\n\n    # one value per metro-year: the latest month reported that year\n    long = long.sort_values([&quot;RegionID&quot;, &quot;year&quot;, &quot;month_num&quot;])\n    # StateName is empty for the national row; without dropna=False groupby\n    # silently discards it and the whole national series disappears.\n    long[&quot;StateName&quot;] = long[&quot;StateName&quot;].fillna(&quot;&quot;)\n    annual = long.groupby([&quot;RegionID&quot;, &quot;RegionName&quot;, &quot;RegionType&quot;, &quot;StateName&quot;, &quot;year&quot;],\n                          as_index=False, dropna=False).last()\n    annual = annual[[&quot;RegionID&quot;, &quot;RegionName&quot;, &quot;RegionType&quot;, &quot;StateName&quot;,\n                     &quot;year&quot;, &quot;zhvi&quot;, &quot;month_num&quot;]]\n    annual.columns = [&quot;region_id&quot;, &quot;region_name&quot;, &quot;region_type&quot;, &quot;state_name&quot;,\n                      &quot;year&quot;, &quot;zhvi&quot;, &quot;as_of_month&quot;]\n    annual[&quot;zhvi&quot;] = annual[&quot;zhvi&quot;].round(0)\n    return annual.sort_values([&quot;region_name&quot;, &quot;year&quot;]).reset_index(drop=True)</code></pre>\n    </div>\n\n    <h2>Merging the Sources</h2>\n\n    <p>Each source answers a different part of the question and none answers it alone. The Census survey\n    records whether young households own but says nothing about what a home costs or what they earn. FRED\n    records earnings and borrowing costs but only nationally. Zillow records prices across 894 metropolitan\n    areas but nothing about who buys. Affordability is a relationship between all three, so the measures this\n    project depends on, price against income and payment against income, exist only after the join.</p>\n\n    <p>Both merges use <code>year</code> as the key, because that is the finest grain the three sources share:\n    the Census and FRED series are national, so nothing narrower is available to join on.</p>\n\n    <h3>Merge 1: national_annual</h3>\n    <p>An <b>inner join on year</b> across the ownership table, the FRED annual table, and the national row of\n    the Zillow data. Inner rather than outer, because a year missing any of the three cannot support the\n    derived measures. The result spans 2000 to 2025 and is 26 rows rather than 44, since ownership data begins\n    in 1982 but prices and earnings begin in 2000, and 2026 ownership is not yet published. Five derived\n    columns are added after the join: price-to-income, years to a down payment, monthly mortgage payment,\n    payment as a share of income, and earnings in real terms.</p>\n\n    <figure class="sample">\n      <img src="images/merge-national.png" alt="First rows of national_annual after the merge">\n      <figcaption><b>Figure 9.</b> The merged national table, six of twenty-three columns shown. Ownership,\n      earnings, price and mortgage rate now sit on one row, which is what makes the payment burden in the\n      final column computable at all.</figcaption>\n    </figure>\n\n    <h3>Merge 2: metro_year_panel</h3>\n    <p>A <b>left join on year</b>, attaching each national row to every metropolitan area in that year. This is\n    one-to-many by design, and it has a consequence worth stating plainly: earnings and the mortgage rate are\n    identical across all 894 metros within a year and vary only down the time axis. They are national controls\n    rather than local measurements, and no model should treat them as distinguishing one city from another.\n    The result is 19,288 rows, 894 metros across 2000 to 2025.</p>\n\n    <figure class="sample">\n      <img src="images/merge-panel.png" alt="First rows of metro_year_panel after the merge">\n      <figcaption><b>Figure 10.</b> The merged metro panel, seven of twenty-five columns shown. Price varies by\n      metro while earnings do not, which is precisely why the price-to-income column differs between rows of\n      the same year.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>the merge and derived columns</span></div>\n      <pre><code># ---- national annual table -------------------------------------------------\n\nif os.path.exists(f&quot;{RAW}/fred/fred_annual.csv&quot;):\n    fred = pd.read_csv(f&quot;{RAW}/fred/fred_annual.csv&quot;)\n    log(&quot;\\nfred_annual.csv found - using API-sourced earnings and rates&quot;)\nelse:\n    e1 = pd.read_csv(f&quot;{RAW}/LEU0252887100Q.csv&quot;)\n    e2 = pd.read_csv(f&quot;{RAW}/LEU0252888500Q.csv&quot;)\n    for d, col in ((e1, &quot;median_weekly_earnings_20_24&quot;), (e2, &quot;median_weekly_earnings_25_34&quot;)):\n        d.columns = [&quot;observation_date&quot;, col]\n        d[&quot;year&quot;] = d[&quot;observation_date&quot;].str.slice(0, 4).astype(int)\n    fred = (e1.groupby(&quot;year&quot;)[&quot;median_weekly_earnings_20_24&quot;].mean().round(2).reset_index()\n            .merge(e2.groupby(&quot;year&quot;)[&quot;median_weekly_earnings_25_34&quot;].mean().round(2).reset_index(),\n                   on=&quot;year&quot;))\n    fred[&quot;annual_earnings_20_24&quot;] = (fred[&quot;median_weekly_earnings_20_24&quot;] * 52).round(0)\n    fred[&quot;annual_earnings_25_34&quot;] = (fred[&quot;median_weekly_earnings_25_34&quot;] * 52).round(0)\n    log(&quot;\\nfred_annual.csv NOT found - falling back to the downloaded CSVs.&quot;)\n    log(&quot;  Run fred_api_fetch.py to satisfy the API requirement and add mortgage rates.&quot;)\n\nown_wide = own_annual.pivot(index=&quot;year&quot;, columns=&quot;age_bracket&quot;,\n                            values=&quot;ownership_rate_pct&quot;).reset_index()\nown_wide.columns = [&quot;year&quot;] + [f&quot;ownership_rate_{c.replace(&#x27;&lt;&#x27;, &#x27;lt&#x27;).replace(&#x27;-&#x27;, &#x27;_&#x27;)}_pct&quot;\n                               for c in own_wide.columns[1:]]\n\nnational_zhvi = (zhvi[zhvi.region_type == &quot;country&quot;][[&quot;year&quot;, &quot;zhvi&quot;]]\n                 .rename(columns={&quot;zhvi&quot;: &quot;national_zhvi&quot;}))\n\nnational = own_wide.merge(fred, on=&quot;year&quot;).merge(national_zhvi, on=&quot;year&quot;)\nnational[&quot;price_to_income_25_34&quot;] = (national[&quot;national_zhvi&quot;] /\n                                     national[&quot;annual_earnings_25_34&quot;]).round(2)\nnational[&quot;years_to_down_payment_25_34&quot;] = (\n    (DOWN_PAYMENT * national[&quot;national_zhvi&quot;]) /\n    (national[&quot;annual_earnings_25_34&quot;] * SAVINGS_RATE)).round(1)\nif &quot;mortgage_rate_30yr_pct&quot; in national.columns:\n    national[&quot;monthly_payment_usd&quot;] = national.apply(\n        lambda r: monthly_payment(r[&quot;national_zhvi&quot;], r[&quot;mortgage_rate_30yr_pct&quot;]), axis=1).round(0)\n    national[&quot;payment_to_income_pct_25_34&quot;] = (\n        national[&quot;monthly_payment_usd&quot;] * 12 / national[&quot;annual_earnings_25_34&quot;] * 100).round(1)\nnational.to_csv(f&quot;{OUT}/national_annual.csv&quot;, index=False)\nlog(f&quot;national_annual.csv               {len(national):&gt;6,} rows  &quot;\n    f&quot;{national.year.min()}-{national.year.max()}  {national.shape[1]} columns&quot;)\n\n# ---- metro-year panel with engineered features -----------------------------\n\npanel = zhvi[zhvi.region_type == &quot;msa&quot;].copy()\npanel = panel[panel.year.between(2000, 2025)].sort_values([&quot;region_id&quot;, &quot;year&quot;])\n\ng = panel.groupby(&quot;region_id&quot;)[&quot;zhvi&quot;]\npanel[&quot;zhvi_yoy_pct&quot;]   = (g.pct_change(1) * 100).round(2)\npanel[&quot;zhvi_3yr_pct&quot;]   = (g.pct_change(3) * 100).round(2)\npanel[&quot;zhvi_5yr_pct&quot;]   = (g.pct_change(5) * 100).round(2)\npanel[&quot;zhvi_volatility_5yr&quot;] = (panel.groupby(&quot;region_id&quot;)[&quot;zhvi_yoy_pct&quot;]\n                                .transform(lambda s: s.rolling(5, min_periods=3).std()).round(2))\n\ncarry = [&quot;year&quot;, &quot;national_zhvi&quot;, &quot;annual_earnings_25_34&quot;, &quot;annual_earnings_20_24&quot;,\n         &quot;ownership_rate_25_29_pct&quot;, &quot;ownership_rate_30_34_pct&quot;]\nfor optional in [&quot;mortgage_rate_30yr_pct&quot;, &quot;annual_earnings_25_34_real2025&quot;]:\n    if optional in national.columns:\n        carry.append(optional)\npanel = panel.merge(national[carry], on=&quot;year&quot;, how=&quot;left&quot;)\npanel[&quot;zhvi_vs_national&quot;] = (panel[&quot;zhvi&quot;] / panel[&quot;national_zhvi&quot;]).round(3)\npanel[&quot;zhvi_pctile_in_year&quot;] = (panel.groupby(&quot;year&quot;)[&quot;zhvi&quot;]\n                                .rank(pct=True).mul(100).round(1))\npanel[&quot;price_to_income_25_34&quot;] = (panel[&quot;zhvi&quot;] / panel[&quot;annual_earnings_25_34&quot;]).round(2)\npanel[&quot;years_to_down_payment_25_34&quot;] = (\n    (DOWN_PAYMENT * panel[&quot;zhvi&quot;]) /\n    (panel[&quot;annual_earnings_25_34&quot;] * SAVINGS_RATE)).round(1)\nif &quot;mortgage_rate_30yr_pct&quot; in panel.columns:\n    panel[&quot;monthly_payment_usd&quot;] = (\n        panel[&quot;zhvi&quot;] * (1 - DOWN_PAYMENT)\n        * (panel[&quot;mortgage_rate_30yr_pct&quot;] / 1200)\n        * (1 + panel[&quot;mortgage_rate_30yr_pct&quot;] / 1200) ** 360\n        / ((1 + panel[&quot;mortgage_rate_30yr_pct&quot;] / 1200) ** 360 - 1)).round(0)\n    panel[&quot;payment_to_income_pct_25_34&quot;] = (\n        panel[&quot;monthly_payment_usd&quot;] * 12 / panel[&quot;annual_earnings_25_34&quot;] * 100).round(1)\n\npanel[&quot;affordability_quartile&quot;] = (panel.groupby(&quot;year&quot;)[&quot;price_to_income_25_34&quot;]\n                                   .transform(lambda s: pd.qcut(s, 4, duplicates=&quot;drop&quot;,\n                                                                labels=False) + 1\n                                              if s.notna().sum() &gt;= 4 else pd.Series(index=s.index, dtype=&quot;float&quot;)))\npanel[&quot;affordability_quartile&quot;] = panel[&quot;affordability_quartile&quot;].map(\n    {1: &quot;Q1_most_affordable&quot;, 2: &quot;Q2&quot;, 3: &quot;Q3&quot;, 4: &quot;Q4_least_affordable&quot;})\npanel.to_csv(f&quot;{OUT}/metro_year_panel.csv&quot;, index=False)\nlog(f&quot;metro_year_panel.csv              {len(panel):&gt;6,} rows  &quot;\n    f&quot;{panel.region_id.nunique()} metros  {panel.shape[1]} columns&quot;)\n\nif os.path.exists(f&quot;{RAW}/acs/acs_metro_annual.csv&quot;):\n    log(&quot;\\nacs_metro_annual.csv found - join it for metro-level ownership rates.&quot;)\nelse:\n    log(&quot;\\nacs_metro_annual.csv NOT found - metro-level ownership rate unavailable.&quot;)\n    log(&quot;  Run acs_api_fetch.py if the target for Part 2 should be a real ownership rate.&quot;)</code></pre>\n    </div>\n'
