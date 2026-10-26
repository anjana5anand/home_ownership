NAIVE_BAYES_BODY = """
    <div class="meta">
      <dl>
        <dt>Category</dt><dd>Supervised &middot; classification (Naive Bayes)</dd>
        <dt>Target</dt><dd><code>affordability_class</code>: Affordable / Moderate / Burdened, 3 classes</dd>
        <dt>Data used</dt><dd><code>metro_2025_supervised.csv</code>, 894 metros &times; 4 predictors + label</dd>
      </dl>
    </div>

    <h2>Overview</h2>
    {t_overview1}

    <figure>
      <img src="images/theory-nb-independence.png" alt="Naive Bayes independence assumption: features point to a shared class node">
      <figcaption><b>Figure.</b> Naive Bayes assumes every predictor is conditionally independent of the others once the class is known, which is the &ldquo;naive&rdquo; part of the name.</figcaption>
    </figure>
    <figure>
      <img src="images/theory-nb-feature-types.png" alt="Multinomial NB sees counts; Bernoulli NB sees 0/1 features">
      <figcaption><b>Figure.</b> The two Naive Bayes variants used here differ only in how they read a feature: Multinomial NB treats each feature as a count (which quantile bin a metro falls into), Bernoulli NB treats it as present/absent (above or below the median).</figcaption>
    </figure>

    {t_overview2}

    <h2>Data Prep</h2>
    {t_dataprep}

    <figure class="sample">
      <img src="images/data-sample-supervised.png" alt="Sample rows of the labeled affordability-class dataset">
      <figcaption><b>Sample.</b> First rows of <code>metro_2025_supervised.csv</code>: 4 price-growth/volatility predictors, the payment-to-income ratio the label is built from, and the resulting 3-class label.
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised.csv" target="_blank" rel="noopener">Full file on GitHub &#8599;</a></figcaption>
    </figure>

    <figure class="sample">
      <img src="images/data-split-supervised.png" alt="Training and testing split sizes by affordability class">
      <figcaption><b>Sample.</b> The 75/25 train/test split, stratified by class so all three affordability classes are represented in the same proportion in both sets.
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised_train.csv" target="_blank" rel="noopener">Training set on GitHub &#8599;</a> &middot;
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised_test.csv" target="_blank" rel="noopener">Testing set on GitHub &#8599;</a></figcaption>
    </figure>

    <h2>Code</h2>
    <p>Python, using scikit-learn. Multinomial NB needs non-negative, count-like input, so each predictor is
    discretized into 4 quantile bins (fit on the training set only) before fitting; Bernoulli NB needs binary
    input, so each predictor is thresholded at its own training-set median.</p>

    <figure>
      <img src="images/nb-binning-illustration.png" alt="Quantile bin edges for two predictors, fit on the training set">
      <figcaption><b>Figure.</b> Quantile bin edges (orange dashed lines) for two of the four predictors, computed on the training set only and then applied to both the training and testing sets.</figcaption>
    </figure>

    <div class="codeblock">
      <div class="codehead">run_naive_bayes.py<span>Multinomial NB (binned) and Bernoulli NB (binarized)</span>
        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/run_naive_bayes.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>
        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>
      </div>
      <div class="code-body">
        <pre><code>binner = KBinsDiscretizer(n_bins=4, encode=&quot;ordinal&quot;, strategy=&quot;quantile&quot;)
X_train_binned = binner.fit_transform(X_train)
X_test_binned = binner.transform(X_test)

mnb = MultinomialNB()
mnb.fit(X_train_binned, y_train)
mnb_pred = mnb.predict(X_test_binned)

&#8942;  # Bernoulli NB: threshold each predictor at its training-set median instead

medians = X_train.median()
X_train_bin = (X_train &gt;= medians).astype(int)
bnb = BernoulliNB().fit(X_train_bin, y_train)</code></pre>
        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>
      </div>
    </div>

    <ul class="linklist">
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/prep_supervised_data.py" target="_blank" rel="noopener">prep_supervised_data.py</a> <span>: builds the labeled table and the stratified train/test split</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/run_naive_bayes.py" target="_blank" rel="noopener">run_naive_bayes.py</a> <span>: Multinomial NB and Bernoulli NB, confusion matrices, accuracy</span></li>
    </ul>

    <h2>Results</h2>
    {t_results}

    <div class="scroll">
      <table>
        <thead><tr><th>Model</th><th class="num">Test accuracy</th></tr></thead>
        <tbody>
          <tr><td>Multinomial NB (quantile-binned)</td><td class="num"><strong>49.6%</strong></td></tr>
          <tr><td>Bernoulli NB (median-binarized)</td><td class="num">53.1%</td></tr>
          <tr><td><em>Random guessing (3 balanced classes)</em></td><td class="num"><em>33.3%</em></td></tr>
        </tbody>
      </table>
    </div>

    <figure>
      <img src="images/nb-confusion-multinomial.png" alt="Multinomial NB confusion matrix on the test set">
      <figcaption><b>Figure.</b> Multinomial NB confusion matrix, test set (n = 224). Most errors land in the adjacent class (Affordable mistaken for Moderate, Moderate for Burdened) rather than at the opposite extreme, which is what a reasonable model's mistakes should look like on an ordered label.</figcaption>
    </figure>

    <figure>
      <img src="images/nb-confusion-bernoulli.png" alt="Bernoulli NB confusion matrix on the test set">
      <figcaption><b>Figure.</b> Bernoulli NB confusion matrix, test set (n = 224). Collapsing each predictor to a single above/below-median bit costs Bernoulli NB almost all of its ability to recognize the Moderate class, which gets predicted for only 1 of 75 metros that actually belong to it.</figcaption>
    </figure>

    <h2>Conclusions</h2>
    {t_concl}
"""

DECISION_TREES_BODY = """
    <div class="meta">
      <dl>
        <dt>Category</dt><dd>Supervised &middot; classification (Decision Trees)</dd>
        <dt>Target</dt><dd><code>affordability_class</code>: Affordable / Moderate / Burdened, 3 classes</dd>
        <dt>Data used</dt><dd><code>metro_2025_supervised.csv</code>, 894 metros &times; 4 predictors + label (same table used for Naive Bayes)</dd>
      </dl>
    </div>

    <h2>Overview</h2>
    {t_overview1}

    <figure>
      <img src="images/theory-decision-tree-concept.png" alt="Conceptual decision tree: a sequence of yes/no splits ending in a predicted class">
      <figcaption><b>Figure.</b> A decision tree is a sequence of yes/no questions about the predictors, each one splitting the data further, until a leaf is reached and a class is predicted.</figcaption>
    </figure>
    <figure>
      <img src="images/theory-gini-entropy.png" alt="Gini impurity and entropy as a function of class proportion">
      <figcaption><b>Figure.</b> Gini impurity and entropy measure the same thing on different scales: both are zero when a node is pure (every row the same class) and highest when classes are evenly mixed. A split is &ldquo;good&rdquo; when it lowers this impurity, weighted by how the data divides between the two children.</figcaption>
    </figure>

    {t_overview2}

    <div class="scroll">
      <table>
        <thead><tr><th>Node</th><th class="num">n</th><th>Class counts (Afford. / Mod. / Burd.)</th><th class="num">Gini</th><th class="num">Entropy</th></tr></thead>
        <tbody>
          <tr><td>Parent (root, before split)</td><td class="num">670</td><td>223 / 225 / 222</td><td class="num">0.667</td><td class="num">1.585</td></tr>
          <tr><td>Left child (5yr volatility &le; 6.44)</td><td class="num">419</td><td>166 / 170 / 83</td><td class="num">0.639</td><td class="num">1.520</td></tr>
          <tr><td>Right child (5yr volatility &gt; 6.44)</td><td class="num">251</td><td>57 / 55 / 139</td><td class="num">0.594</td><td class="num">1.438</td></tr>
          <tr><td><strong>Weighted average after split</strong></td><td class="num">670</td><td>&ndash;</td><td class="num"><strong>0.622</strong></td><td class="num"><strong>1.489</strong></td></tr>
          <tr><td><strong>Gain from this split</strong></td><td class="num">&ndash;</td><td>&ndash;</td><td class="num"><strong>0.044</strong></td><td class="num"><strong>0.096</strong></td></tr>
        </tbody>
      </table>
    </div>

    <h2>Data Prep</h2>
    {t_dataprep}

    <figure class="sample">
      <img src="images/data-sample-supervised.png" alt="Sample rows of the labeled affordability-class dataset">
      <figcaption><b>Sample.</b> First rows of <code>metro_2025_supervised.csv</code>, the same labeled table used for Naive Bayes.
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised.csv" target="_blank" rel="noopener">Full file on GitHub &#8599;</a></figcaption>
    </figure>

    <figure class="sample">
      <img src="images/data-split-supervised.png" alt="Training and testing split sizes by affordability class">
      <figcaption><b>Sample.</b> The same 75/25 stratified train/test split used for Naive Bayes.
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised_train.csv" target="_blank" rel="noopener">Training set on GitHub &#8599;</a> &middot;
      <a href="https://github.com/anjana5anand/home_ownership/blob/main/data_clean/metro_2025_supervised_test.csv" target="_blank" rel="noopener">Testing set on GitHub &#8599;</a></figcaption>
    </figure>

    <h2>Code</h2>
    <p>Python, using scikit-learn's <code>DecisionTreeClassifier</code> directly on the unscaled predictors;
    trees compare one feature to a threshold at a time, so standardizing is not required the way it was for
    k-means or PCA.</p>

    <div class="codeblock">
      <div class="codehead">run_decision_trees.py<span>three trees: gini/depth-3, entropy/depth-3, gini/unpruned</span>
        <a class="code-link" href="https://github.com/anjana5anand/home_ownership/blob/main/run_decision_trees.py" target="_blank" rel="noopener">View full file on GitHub &#8599;</a>
        <button class="code-toggle" type="button" aria-expanded="false">Show excerpt</button>
      </div>
      <div class="code-body">
        <pre><code>trees = {{
    &quot;Tree A (gini, depth=3)&quot;:    DecisionTreeClassifier(criterion=&quot;gini&quot;,    max_depth=3,    random_state=42),
    &quot;Tree B (entropy, depth=3)&quot;: DecisionTreeClassifier(criterion=&quot;entropy&quot;, max_depth=3,    random_state=42),
    &quot;Tree C (gini, unpruned)&quot;:   DecisionTreeClassifier(criterion=&quot;gini&quot;,    max_depth=None, random_state=42),
}}
&#8942;  # fit each on the training set, predict the test set, confusion matrix + accuracy</code></pre>
        <button class="code-close" type="button" aria-label="Collapse code excerpt">&times;</button>
      </div>
    </div>

    <ul class="linklist">
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/prep_supervised_data.py" target="_blank" rel="noopener">prep_supervised_data.py</a> <span>: builds the labeled table and the stratified train/test split</span></li>
      <li><a href="https://github.com/anjana5anand/home_ownership/blob/main/run_decision_trees.py" target="_blank" rel="noopener">run_decision_trees.py</a> <span>: three trees, confusion matrices, feature importance, the worked split example</span></li>
    </ul>

    <h2>Results</h2>
    {t_results}

    <div class="scroll">
      <table>
        <thead><tr><th>Tree</th><th class="num">Test accuracy</th><th class="num">Depth</th><th class="num">Leaves</th></tr></thead>
        <tbody>
          <tr><td>Tree A (gini, max depth 3)</td><td class="num"><strong>58.5%</strong></td><td class="num">3</td><td class="num">8</td></tr>
          <tr><td>Tree B (entropy, max depth 3)</td><td class="num">58.0%</td><td class="num">3</td><td class="num">8</td></tr>
          <tr><td>Tree C (gini, unpruned)</td><td class="num">48.2%</td><td class="num">22</td><td class="num">243</td></tr>
          <tr><td><em>Random guessing (3 balanced classes)</em></td><td class="num"><em>33.3%</em></td><td class="num">&ndash;</td><td class="num">&ndash;</td></tr>
        </tbody>
      </table>
    </div>

    <figure class="wide">
      <img src="images/dt-tree-gini.png" alt="Tree A: gini criterion, max depth 3">
      <figcaption><b>Figure.</b> Tree A, gini criterion, max depth 3. The root splits on 5-year price volatility; lower branches further split on 1-year and 5-year price change.</figcaption>
    </figure>

    <figure class="wide">
      <img src="images/dt-tree-entropy.png" alt="Tree B: entropy criterion, max depth 3">
      <figcaption><b>Figure.</b> Tree B, entropy criterion, max depth 3. Built on the same data with a different impurity measure; the structure is close to Tree A's but not identical, showing the two criteria usually agree without being guaranteed to.</figcaption>
    </figure>

    <figure class="wide">
      <img src="images/dt-tree-unpruned-top.png" alt="Tree C: gini criterion, unpruned, top 3 levels shown">
      <figcaption><b>Figure.</b> Tree C, grown without a depth limit, reaches 22 levels and 243 leaves; only the top 3 levels are shown here since the full tree is far too large to read. Despite fitting the training data far more closely, it scores lower on the test set than the two shallow trees.</figcaption>
    </figure>

    <figure>
      <img src="images/dt-confusion-tree-a.png" alt="Tree A confusion matrix">
      <figcaption><b>Figure.</b> Tree A confusion matrix. Errors again cluster in adjacent classes rather than jumping from Affordable straight to Burdened.</figcaption>
    </figure>
    <figure>
      <img src="images/dt-confusion-tree-c.png" alt="Tree C (unpruned) confusion matrix">
      <figcaption><b>Figure.</b> Tree C (unpruned) confusion matrix, for comparison. More metros are misclassified overall than with the shallow Tree A, the signature of overfitting: the unpruned tree memorized quirks of the 670 training metros that did not generalize to the 224 it had never seen.</figcaption>
    </figure>

    <figure>
      <img src="images/dt-feature-importance.png" alt="Feature importance for Tree A">
      <figcaption><b>Figure.</b> Which of the 4 predictors Tree A actually uses to split, weighted by how much each split reduced gini impurity.</figcaption>
    </figure>

    <h2>Conclusions</h2>
    {t_concl}
"""
