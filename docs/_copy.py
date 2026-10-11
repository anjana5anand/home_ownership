# Draft prose. Written to be rewritten - Anjana's voice should replace this.
# Third person throughout: no "I", "me", "my".

INTRO_TOPIC = """
    <p>Owning homes has been one of the largest most defining components of wealth for most households. The
    age at which one buys their first home shapes how much wealth will potentially accumulate depending on
    size, location etc. Homes that could have been bought by someone in their mid 20s to mid 30s 2 decades ago
    is now steadily moving out of reach for people now in their mid 20s to 30s. Census housing vacancy surveys
    show that among households aged 25-29 years dropped 41.8% in 2006 to 30.9% in 2016, recovering only to
    33.3 percent by 2025. 30-34 year old home owners followed the same path, from 57.4 percent down to 45.4
    percent and back to 46.6 percent. Neither group has returned to where it stood before the 2008 financial
    crisis, more than fifteen years later. Across the same period the typical American home rose in value from
    roughly $132,000 to $370,000.</p>

    <p>The most well-known explanation for this is that wages failed to keep up with prices of homes. Median
    earnings of a full-time worker aged 25-34 rose from $28,561 to $59,176 between 2000 and 2025, which looks
    like a doubling of purchasing power. Adjusted for inflation, the same earnings move from $53,403 to
    $55,435 between 2000 and 2019. A gain of under four percent across nineteen years, before rising to
    $59,176 by 2025. A young worker's paycheck was therefore close to flat for almost 2 decades while the
    price of homes that workers are trying to buy has almost tripled. Ratios tell the same story from another
    angle: the price of a typical home rose from 4.6 times a young worker's annual earnings in 2000 to 6.3
    times in 2025.</p>

    <p>The mortgage rate is yet another aspect of affordability. The mortgage rate of a conventional 30-year
    loan went into record low levels by the end of 2021 before sharply going up again within the next few
    years, making the costs of purchasing a property much higher even though the price stays the same.
    Combined with an increasing housing price trend instead of decreasing one, it makes the calculations of
    acquiring a first property much more difficult for young people in nearly all regions of the country.
    This project will investigate the issue of housing affordability in the major metropolitan areas of the
    U.S.</p>

    <figure>
      <img src="images/intro-rates-vs-prices.png" alt="U.S. median home value and average 30-year mortgage rate by year, 2000 to 2025">
      <figcaption><b>Figure.</b> U.S. median home value (Zillow ZHVI) against the average 30-year mortgage rate, 2000 to 2025. Home values kept climbing even as the mortgage rate spiked after 2021, stacking two affordability pressures on top of each other at the same time.</figcaption>
    </figure>
"""

INTRO_STAKE = """
    <p>The group that is directly affected is one in three Americans aged 25-34 who rent and would prefer to
    own homes. The gap between renting and owning determines whether monthly housing costs build equity or
    disappear. This delay compounds since a purchase postponed by 10 years is 10 years of equity never
    accumulated. Families are increasingly supplying down-payment assistance that turns a market outcome into
    an inherited one which widens the distance between households that can offer such help and those that
    cannot.</p>

    <p>Lenders and homebuilders have a commercial stake in this since first time buyers are the entry point to
    the housing market and shrinking cohort of them constrains transaction volume throughout the chain.
    Municipal and state governments have a fiscal and practical stake. Property taxes fund local services and
    metropolitan area where young workers cannot afford to buy face difficulty retaining teachers, nurses and
    other essential workers. Housing policy makers need to know whether the constraint is price, income,
    credit cost, or supply, because each points to a different intervention: zoning reform, down-payment
    assistance, interest-rate policy, or construction subsidy.</p>
"""

INTRO_GAPS = """
    <p>The tools for measuring housing affordability are readily available and mainly address a single issue.
    The mortgage calculator available from Zillow, NerdWallet, and virtually all retail banks informs a
    particular household of its affordability at current interest rates, based on current income. They are
    useful to make a decision but not so much to capture a trend. They describe one household at one moment
    and fail to say anything about how the situation has changed or how it differs between places. Industry
    reporting does fill parts of that gap. The National Association of Realtors publishes their annual
    Buyer-Seller Profile while Harvard's Joint Center for Housing Studies publishes their &ldquo;State of the
    Nation's Housing&rdquo; reports that look at first-time buyer age and homeownership trends over the
    years.</p>

    <p>Research on why young-adult homeownership fell has concentrated on demographic explanation. A joint
    center analysis attributed part of the decline to later marriage, changing household composition and
    migration toward central cities, but concluded that demographic factors account for only about a quarter
    of the variation in whether a household owns or rents, leaving macroeconomic conditions and price as the
    larger share of the explanation.</p>

    <p>That leaves 2 gaps in this project to address. The first is that most public treatments measure
    affordability as a price-to-income ratio and ignore the cost of borrowing entirely which is a serious
    omission. In 2021 the price-to-income ratio stood near a record 6.6 while the share of income required to
    service a mortgage was a moderate 26.5 percent, because money cost 2.96 percent; by 2023 that share
    reached 41.5 percent, worse than the 2006 housing-bubble peak of 39.7 percent, on a price-to-income ratio
    that had barely moved. Secondly, the national aggregates mask the geography almost entirely. In 2025 the
    price of a typical home ranged from 0.81 times a young worker's annual earnings in Helena, Arkansas to
    27.1 times in San Jose, California, a spread across 894 metropolitan areas that no national average can
    represent.</p>
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
"""

INTRO_DATASET = """
    <p>Three sources were selected, each covering something the others cannot. The project is centered on
    three sources: the Census Housing Vacancy Survey for homeownership by age of householder, the Federal
    Reserve Bank of St. Louis FRED API for earnings, mortgage rates, prices and inflation, and the Zillow Home
    Value Index for home values at metropolitan level. Cleaning reshapes each into tidy tables, which is
    non-trivial because none of the three arrives in an analysable form. The Census workbook repeats an entire
    year-block down the sheet, the FRED series arrive at three different frequencies, and the Zillow file is
    319 columns wide. Dependent variable, the homeownership by age of householder is provided by the Census
    Housing Vacancy Survey starting in 1982 and using age categories fine enough to distinguish between those
    aged 25 to 29 and those aged 30 to 34. This is important since the two age categories are on either side
    of the normal first purchase and data sources using a broader &ldquo;under 35&rdquo; category lump them
    together. Economic variables include the median weekly earnings by age category, the 30-year fixed
    mortgage rate, national homeownership rate, median sales price, the Case&ndash;Shiller index, the Consumer
    Price Index and housing starts and are obtained through the FRED API. Getting the data programmatically
    from an API rather than downloaded ensures reproducibility and enabled inclusion of the mortgage rate and
    inflation data that are key to the affordability analysis. The geographical component of the data comes
    from the Zillow Home Value Index that reports a median home value in 894 metro areas monthly since
    2000.</p>

    <p>Several limitations follow from these choices and are carried through the analysis. None of the three
    sources is individual-level, so the project describes aggregate rates rather than the circumstances of
    particular households. Earnings are reported nationally rather than by metropolitan area, which means
    metro-level affordability measures compare local prices against a national income and cannot capture the
    fact that salaries in San Jose differ from salaries in Cleveland. The Zillow index covers the middle tier
    of the market, between the 33rd and 67th percentiles of value, and therefore excludes both the cheapest
    and most expensive segments. Homeownership figures are reported for the age of the householder rather
    than of every occupant, so a 27-year-old living in a parent's home is counted under that parent's age.
    Each of these is a genuine constraint on what the results can support, and each is noted again where it
    bears on a specific finding.</p>

    <p>Next comes feature engineering, which generates the variables used in the analysis: price-to-income
    ratio, number of years needed to accumulate savings for a down-payment, mortgage payment per month, and
    the payment ratio relative to income, alongside measures of growth, volatility, and ranking for each metro
    area.</p>

    <p>The modelling stage answers the research questions posed above in two classes. Clustering and
    principal component analysis, unsupervised models, seek whether there are types of housing market, and
    how they differ. Naive Bayes, decision trees, support vector machines, regression and neural networks,
    supervised models, seek whether the affordability of a market can be predicted by its pricing
    characteristics, and which variables contain that information. Each model is described in turn, outlining
    its underlying assumptions, parameter space, and limitations on what its findings mean.</p>
"""

PREP_COLLECT = """
    <p>One programmatic course combined with 2 direct downloads. This was chosen so that each one covered
    a dimension the others lacked. Time depth is covered from the census survey, economic context from
    FRED and geographic details from Zillow. The FRED dataset was retrieved through the API described
    below which returned 2771 individual observations across 8 series and saved each raw response to disk
    so that the collection step is auditable and repeatable. The two downloaded sources were taken from
    their publishers' own distribution pages.</p>
"""

PREP_DOWNLOADS = """
    <p>Historical Census Housing Vacancy Survey tables were provided as Excel files available on the
    website of the Census Bureau. Table 12 was used, showing the number of total households and
    owner-occupied households by age of the householder each year since 1982. This table was selected
    over the quarterly tables provided by the Bureau due to the fact that the latter provide one total
    figure for all householders under 35 years old, whereas Table 12 breaks down this age category into
    age ranges that are needed for this project. Zillow Home Value Index was available as a comma-delimited
    file on the research section of Zillow. The metropolitan file in the middle price range was used to
    provide a typical home value in 894 metropolitan areas since January 2000.</p>
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


PREP_SOURCES = '\n    <h2><span class="srcnum">01</span>Census Housing Vacancy Survey, Table 12</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-hvs.png" alt="Raw sample of Census Housing Vacancy Survey, Table 12">\n      <figcaption><b>Figure 3.</b> The first fourteen rows of the workbook as published. Column headers sit several rows down, shaded cells are structurally blank rather than missing, and the whole year-block repeats further down the sheet for earlier years.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Locate each repeating <code>Age of Householder</code> block and read the paired total and owner columns beneath it.</li>\n      <li>Strip trailing dot leaders and footnote letters from row labels before they can be matched.</li>\n      <li>Resolve years that appear in more than one block, keeping the later revised estimate.</li>\n      <li>Convert counts stored as text into numbers.</li>\n      <li>Compute the ownership rate, which the file does not contain, as owner households divided by total households.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-hvs.png" alt="Cleaned output for Census Housing Vacancy Survey, Table 12">\n      <figcaption><b>Figure 4.</b> The result: one row per year and age bracket, with the rate computed. 220 rows covering 1982 to 2025 across five age brackets.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>parse_histtab12()</span>\n        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/build_datasets.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>\n        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>\n      </div>\n      <div class="code-body">\n        <pre><code>def parse_histtab12(path=f&quot;{RAW}/histtab12.xlsx&quot;):\n    import openpyxl\n    ws = openpyxl.load_workbook(path, data_only=True)[&quot;Sheet1&quot;]\n    rows = list(ws.iter_rows(values_only=True))\n\n    targets = {&quot;less than 25 years&quot;: &quot;&lt;25&quot;, &quot;25 to 29 years&quot;: &quot;25-29&quot;,\n               &quot;30 to 34 years&quot;: &quot;30-34&quot;, &quot;35 to 39 years&quot;: &quot;35-39&quot;,\n               &quot;40 to 44 years&quot;: &quot;40-44&quot;}\n\n    records, i, n = [], 0, len(rows)\n    while i &lt; n:\n        if rows[i][0] and str(rows[i][0]).strip() == &quot;Age of Householder&quot;:\n            &#8942;  # walk each repeating year-block, match age labels, dedupe revised years</code></pre>\n        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>\n      </div>\n    </div>\n\n    <h2><span class="srcnum">02</span>BLS and Census via the FRED API</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-fred.png" alt="Raw sample of BLS and Census via the FRED API">\n      <figcaption><b>Figure 5.</b> Six observations from the MORTGAGE30US response. The series is weekly, and two realtime columns record when the figure was published rather than anything about housing.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Collapse eight series arriving weekly, monthly and quarterly onto a single annual grain.</li>\n      <li>Drop <code>realtime_start</code> and <code>realtime_end</code>, which carry no analytical information.</li>\n      <li>Treat the string <code>&quot;.&quot;</code> as missing, since reading it as a value turns the whole column into text.</li>\n      <li>Convert median weekly earnings to an annual figure.</li>\n      <li>Deflate nominal dollars to constant 2025 terms using the Consumer Price Index.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-fred.png" alt="Cleaned output for BLS and Census via the FRED API">\n      <figcaption><b>Figure 6.</b> The result: one row per year with every series on the same grain, four of thirteen columns shown. 2,771 raw observations reduce to 27 annual rows.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">fred_api_fetch.py<span>fetch_series()</span>\n        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/fred_api_fetch.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>\n        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>\n      </div>\n      <div class="code-body">\n        <pre><code>def fetch_series(series_id, key):\n    &quot;&quot;&quot;Return (metadata_dict, {year: [values]}).&quot;&quot;&quot;\n    meta_payload = api_get(&quot;series&quot;, {&quot;series_id&quot;: series_id, &quot;api_key&quot;: key, &quot;file_type&quot;: &quot;json&quot;})\n    meta = {}\n    if meta_payload and meta_payload.get(&quot;seriess&quot;):\n        s = meta_payload[&quot;seriess&quot;][0]\n        meta = {&quot;series_id&quot;: series_id, &quot;title&quot;: s.get(&quot;title&quot;), &quot;units&quot;: s.get(&quot;units&quot;), &#8230;}\n\n    obs = api_get(&quot;series/observations&quot;, {\n        &quot;series_id&quot;: series_id, &quot;api_key&quot;: key, &quot;file_type&quot;: &quot;json&quot;,\n        &quot;observation_start&quot;: START,\n    })\n    &#8942;  # writes the raw response to disk, then collapses to annual values, skipping FRED&#x27;s &quot;.&quot; missing marker</code></pre>\n        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>\n      </div>\n    </div>\n\n    <h2><span class="srcnum">03</span>Zillow Home Value Index, metro</h2>\n\n    <h3>Raw sample</h3>\n    <figure class="sample">\n      <img src="images/raw-zhvi.png" alt="Raw sample of Zillow Home Value Index, metro">\n      <figcaption><b>Figure 7.</b> The file in its published shape, 895 rows by 324 columns. Eight columns are shown here; 313 further month columns continue to the right.</figcaption>\n    </figure>\n\n    <h3>What needs to change</h3>\n    <ul class="tight">\n      <li>Reshape 319 month columns into rows, so each observation occupies one row.</li>\n      <li>Reduce each metro-year to a single value, taking the latest month reported in that year.</li>\n      <li>Fill the empty <code>StateName</code> on the national row, which a default groupby silently discards.</li>\n      <li>Separate the country row from the 894 metropolitan rows, since they feed different tables.</li>\n    </ul>\n\n    <h3>Cleaned output</h3>\n    <figure class="sample">\n      <img src="images/clean-zhvi.png" alt="Cleaned output for Zillow Home Value Index, metro">\n      <figcaption><b>Figure 8.</b> The result: one row per metropolitan area per year. The wide file becomes 20,209 long rows covering 2000 to 2026.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>parse_zhvi()</span>\n        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/build_datasets.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>\n        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>\n      </div>\n      <div class="code-body">\n        <pre><code>def parse_zhvi(path=f&quot;{RAW}/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv&quot;):\n    wide = pd.read_csv(path)\n    id_cols = [&quot;RegionID&quot;, &quot;SizeRank&quot;, &quot;RegionName&quot;, &quot;RegionType&quot;, &quot;StateName&quot;]\n    date_cols = [c for c in wide.columns if c not in id_cols]\n\n    long = wide.melt(id_vars=id_cols, value_vars=date_cols,\n                     var_name=&quot;month&quot;, value_name=&quot;zhvi&quot;).dropna(subset=[&quot;zhvi&quot;])\n    long[&quot;year&quot;] = long[&quot;month&quot;].str.slice(0, 4).astype(int)\n\n    # StateName is empty for the national row; without dropna=False groupby\n    # silently discards it and the whole national series disappears.\n    long[&quot;StateName&quot;] = long[&quot;StateName&quot;].fillna(&quot;&quot;)\n    &#8942;  # groups to one value per metro-year, keeping the latest month reported</code></pre>\n        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>\n      </div>\n    </div>\n\n    <h2>Merging the Sources</h2>\n\n    <p>Each source answers a different part of the question and none answers it alone. The Census survey\n    records whether young households own but says nothing about what a home costs or what they earn. FRED\n    records earnings and borrowing costs but only nationally. Zillow records prices across 894 metropolitan\n    areas but nothing about who buys. Affordability is a relationship between all three, so the measures this\n    project depends on, price against income and payment against income, exist only after the join.</p>\n\n    <p>Both merges use <code>year</code> as the key, because that is the finest grain the three sources share:\n    the Census and FRED series are national, so nothing narrower is available to join on.</p>\n\n    <h3>Merge 1: national_annual</h3>\n    <p>An <b>inner join on year</b> across the ownership table, the FRED annual table, and the national row of\n    the Zillow data. Inner rather than outer, because a year missing any of the three cannot support the\n    derived measures. The result spans 2000 to 2025 and is 26 rows rather than 44, since ownership data begins\n    in 1982 but prices and earnings begin in 2000, and 2026 ownership is not yet published. Five derived\n    columns are added after the join: price-to-income, years to a down payment, monthly mortgage payment,\n    payment as a share of income, and earnings in real terms.</p>\n\n    <figure class="sample">\n      <img src="images/merge-national.png" alt="First rows of national_annual after the merge">\n      <figcaption><b>Figure 9.</b> The merged national table, six of twenty-three columns shown. Ownership,\n      earnings, price and mortgage rate now sit on one row, which is what makes the payment burden in the\n      final column computable at all.</figcaption>\n    </figure>\n\n    <h3>Merge 2: metro_year_panel</h3>\n    <p>A <b>left join on year</b>, attaching each national row to every metropolitan area in that year. This is\n    one-to-many by design, and it has a consequence worth stating plainly: earnings and the mortgage rate are\n    identical across all 894 metros within a year and vary only down the time axis. They are national controls\n    rather than local measurements, and no model should treat them as distinguishing one city from another.\n    The result is 19,288 rows, 894 metros across 2000 to 2025.</p>\n\n    <figure class="sample">\n      <img src="images/merge-panel.png" alt="First rows of metro_year_panel after the merge">\n      <figcaption><b>Figure 10.</b> The merged metro panel, seven of twenty-five columns shown. Price varies by\n      metro while earnings do not, which is precisely why the price-to-income column differs between rows of\n      the same year.</figcaption>\n    </figure>\n\n    <h3>Code used</h3>\n    <div class="codeblock">\n      <div class="codehead">build_datasets.py<span>the merge and derived columns</span>\n        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/build_datasets.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>\n        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>\n      </div>\n      <div class="code-body">\n        <pre><code># ---- national annual table -------------------------------------------------\nnational = own_wide.merge(fred, on=&quot;year&quot;).merge(national_zhvi, on=&quot;year&quot;)\nnational[&quot;price_to_income_25_34&quot;] = (national[&quot;national_zhvi&quot;] /\n                                     national[&quot;annual_earnings_25_34&quot;]).round(2)\n&#8942;  # years to down payment, monthly payment, and payment-to-income follow the same pattern\nnational.to_csv(f&quot;{OUT}/national_annual.csv&quot;, index=False)\n\n# ---- metro-year panel with engineered features -----------------------------\npanel = zhvi[zhvi.region_type == &quot;msa&quot;].copy()\npanel = panel[panel.year.between(2000, 2025)].sort_values([&quot;region_id&quot;, &quot;year&quot;])\n&#8942;  # growth, volatility, percentile rank, and affordability quartile computed per metro\npanel[&quot;affordability_quartile&quot;] = (panel.groupby(&quot;year&quot;)[&quot;price_to_income_25_34&quot;]\n                                   .transform(lambda s: pd.qcut(s, 4, duplicates=&quot;drop&quot;, labels=False) + 1\n                                              if s.notna().sum() &gt;= 4 else pd.Series(index=s.index, dtype=&quot;float&quot;)))\npanel.to_csv(f&quot;{OUT}/metro_year_panel.csv&quot;, index=False)</code></pre>\n        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>\n      </div>\n    </div>\n'

CLUSTER_OVERVIEW_1 = """
    <p>Clustering groups observation by similarity without the labels of the groups or what it should look
    like which is why its called unsupervised learning. 2 methods are used here. Partitional methods, k
    means is the standard example. Start by choosing a number of clusters k, place k centroids, and
    iteratively reassign each point to its nearest centroid and recompute the centroids until the
    assignments stop changing. Hierarchical clustering methods instead build a tree then merges. Every
    observation starts as its own cluster, and at each step the two closest clusters are merged, continuing
    until everything belongs to one cluster. Cutting that tree at a chosen height produces clusters at any
    k the reader wants, a flexibility k-means does not have on its own.</p>
"""

CLUSTER_OVERVIEW_2 = """
    <p>Both of these methods depends on the distance between observations and the choice of distance metric
    is not neutral. The k-means run here uses ordinary Euclidean distance on the standardized features,
    which treats each metro as a point in an eleven-dimensional space and measures straight-line closeness.
    The hierarchical clustering instead uses cosine distance, which measures the angle between two metros'
    feature vectors rather than their magnitude.</p>

    <p>On this particular dataset this distinction is very important since many of the created features
    (the home value, the price-to-income ratio, the monthly payment, etc.) show almost perfect correlation
    with each other. The cosine distance defines groupings of metro areas having similar feature profiles,
    and therefore this method offers an alternative way of detecting patterns compared to the Euclidean
    distance method. In this case clustering is used for discovering new information rather than predicting
    something.</p>
"""

CLUSTER_DATAPREP = """
    <p>Clustering and PCA both require unlabeled, numeric data on comparable scales. The input here is the
    2025 cross-section of the metro-year panel: one row per metropolitan area, 894 of them, with eleven
    engineered numeric features describing each metro's home value, price growth, volatility and
    affordability relative to a national income benchmark. No ownership rate, age bracket or other outcome
    variable is included, since adding one would make this a labeled rather than unlabeled dataset. All
    eleven features were standardized to zero mean and unit variance before either method ran, because the
    raw columns sit on very different scales (dollars in the hundreds of thousands next to percentages and
    small ratios) and an unscaled distance would be dominated by whichever column happens to have the
    largest numbers.</p>
"""

CLUSTER_RESULTS = """
    <p>The silhouette method was run across every k from 2 to 10 for k-means, and hierarchical clustering
    was cut at the height suggested by its own largest internal gap. Both methods point to the same answer
    from two different directions.</p>
"""

CLUSTER_CONCL = """
    <p>Both methods agree that American metropolitan housing markets split most cleanly into two groups
    rather than many: the silhouette method selects k = 2 for k-means, with an average silhouette score of
    about 0.43, and the hierarchical dendrogram's largest internal gap also points to two clusters when cut.
    The two methods assign metros to those two groups quite similarly, with an Adjusted Rand Index of about
    0.74 between k-means and hierarchical clustering at the same k, a reasonably strong agreement for two
    algorithms measuring similarity in different ways (Euclidean versus cosine distance). Looking at what
    separates the two clusters, the divide tracks overall affordability: the smaller cluster of 196 metros
    averages a home value near $542,000 and a payment-to-income burden above 56 percent, while the larger
    cluster of 698 metros averages a home value near $229,000 and a burden near 24 percent. This is
    consistent with earlier EDA findings that metropolitan markets differ far more from each other than any
    single national trend would suggest, and it gives a first, purely data-driven answer to the research
    question of whether a young buyer's chances depend heavily on which metro they live in: the data say
    yes, and the split looks closer to binary, affordable versus not, than finely graded.</p>
"""

PCA_OVERVIEW_1 = """
    <p>Principal component analysis consolidates a set of correlated numeric features as a smaller set of
    new uncorrelated axes called principal components, each a linear combination of the original features.
    The first principle component is the single direction through the data that captures most variance,
    the second is the direction orthogonal to the first that captures the most of what remains and so on.
    Once the input variables have been scaled, the principal components are precisely the eigenvectors of
    the correlation matrix of the input variables, with their variance explained being their respective
    eigenvalues. If a small number of the components account for the majority of the total variance, then
    there must have been much redundant information contained within the input variables.</p>
"""

PCA_OVERVIEW_2 = """
    <p>This project's eleven engineered features turn out to be a useful illustration of a common challenge
    with high-dimensional data: several of them are not really independent pieces of information.
    Price-to-income, monthly payment, years to a down payment and the price-versus-national ratio are all
    simple rescalings of the same home value figure against a national income or rate that does not vary
    across metros within a single year, so they sit close to collinear with one another. Highly collinear,
    high-dimensional data like this can make distance-based methods and models harder to interpret, because
    several columns are effectively voting on the same underlying signal rather than contributing
    independent information. PCA is one standard way to surface and correct for exactly this problem, since
    collinear features collapse onto the same principal component rather than inflating the apparent
    dimensionality of the data.</p>
"""

PCA_DATAPREP = """
    <p>PCA requires the same kind of input as clustering: unlabeled, numeric data on comparable scales. The
    identical 894-metro, eleven-feature 2025 cross-section used for clustering is used here, standardized
    the same way. Reusing one prepared dataset for both unsupervised methods keeps the comparison between
    them fair, since neither method is given an advantage from different preprocessing.</p>
"""

PCA_RESULTS = """
    <p>Eleven principal components were extracted (one per original feature), and their eigenvalues and
    loadings were inspected directly rather than only their plotted shape.</p>
"""

PCA_CONCL = """
    <p>Three principal components recover most of the information in the original eleven features: the
    first two alone explain about 87.2 percent of the total variance (63.0 percent and 24.2 percent
    respectively), and a third component pushes the cumulative total to 94.8 percent. That is a large
    reduction, from eleven dimensions down to three, and it follows directly from the collinearity described
    above rather than showing that the underlying affordability problem is actually simple. The loadings on
    the first component are almost identical in size and sign across home value, price-to-income, monthly
    payment, price-versus-national and years to a down payment, confirming that PC1 is best read as a
    single generalized &ldquo;expensiveness&rdquo; axis built from several near-duplicate measurements of
    the same thing. The second component instead loads most heavily on the one-year, three-year and
    five-year price-growth variables, a genuinely separate axis: a metro can be expensive without having
    grown quickly recently, or the reverse. Read together, the two components suggest a metro's affordability
    situation is well described by two underlying ideas, how expensive it already is and how fast it has
    been getting more so, rather than needing all eleven engineered features to tell a complete story.</p>
"""
