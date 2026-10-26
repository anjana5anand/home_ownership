
NB_OVERVIEW_1 = """
    <p>Naive Bayes is a classification method based on Bayes theorem, which calculates the probability of a
    class given the observed data by combining the probability of the data within each class with how common
    that class already is. It is called naive because it assumes every predictor contributes independently
    to that probability, ignoring any correlation between predictors, even though this assumption is rarely
    exactly true in real data. Despite this simplification, Naive Bayes classifiers tend to perform
    reasonably well and are fast to train, which is why they are a common first method tried for text
    classification tasks such as spam detection and sentiment analysis, as well as for general-purpose
    classification on tabular data like the one used in this project.</p>
"""

NB_OVERVIEW_2 = """
    <p>Two variants of Naive Bayes are compared here. Multinomial Naive Bayes models each predictor as a
    count, how many times something occurs or which category of a discrete scale it falls into, and
    estimates, for each class, the probability distribution over those counts. It requires non-negative
    input, so it is normally used with count data such as word frequencies in text, or, as done here, with
    continuous features that have been discretized into ordered bins. Bernoulli Naive Bayes instead models
    each predictor as a binary indicator, present or absent, true or false, above or below some threshold,
    and separately estimates the probability of that indicator being true within each class. Bernoulli NB
    explicitly accounts for a feature being absent as well as present, which matters when the absence of
    something is itself informative, while Multinomial NB only looks at the counts of the features that do
    occur.</p>
"""

NB_DATAPREP = """
    <p>Naive Bayes is a supervised method, so it needs labeled data: a class to predict for every row. This
    differs from clustering and PCA in Module 2, which required unlabeled numeric data only. Supervised
    methods also need the data split into a Training Set, used to fit the model's parameters, and a Testing
    Set, used only to check how the fitted model performs on metros it never saw during training. These two
    sets must be disjoint, contain no overlapping rows, because testing on rows the model already learned
    from would overstate how well it actually generalizes. Here the 894 metros are split 75/25 into 670
    training rows and 224 testing rows, using stratified sampling so the three affordability classes appear
    in the same proportion in both sets. The four predictors (1, 3, and 5 year price change, and 5 year price
    volatility) are left on their original numeric scale for Bernoulli NB's thresholding, and separately
    discretized into four bins for Multinomial NB, since that model needs count-like input rather than raw
    continuous numbers.</p>
"""

NB_RESULTS = """
    <p>Both Naive Bayes variants land well above the 33.3 percent random-guessing baseline for a 3-class
    problem but well below what would count as reliable prediction. Multinomial NB reaches 49.6 percent test
    accuracy and Bernoulli NB reaches 53.1 percent, so forcing each predictor down to a single above/below-
    median bit actually did slightly better here than keeping four quantile bins. Looking at the confusion
    matrices, most of both models' mistakes land in the class next to the true one (Affordable confused with
    Moderate, Moderate confused with Burdened) rather than at the opposite extreme, which suggests the
    predictors do carry some real signal about the ordering of affordability even where they fail to nail the
    exact class. Bernoulli NB's biggest weakness is the Moderate class, which it predicts for only 1 of 75
    metros that actually belong to it, collapsing most of that class into the model's prediction of Affordable
    instead.</p>
"""

NB_CONCL = """
    <p>Price growth and volatility alone, without being told how expensive a metro already is, can predict
    its current affordability tier only moderately better than chance. This says something about the housing
    affordability question this project is built around: a metro's trajectory does not fully determine its
    outcome, since two metros with similar recent price growth can land in different affordability classes
    depending on where their prices started. That is consistent with the Module 2 finding that price level
    and price growth are largely separate dimensions (PC1 versus PC2 in the PCA results), and it suggests
    that any model trying to predict or explain affordability for young buyers needs to include price level
    directly rather than relying on growth and volatility trends by themselves.</p>
"""

DT_OVERVIEW_1 = """
    <p>A decision tree is a supervised classification (or regression) method that predicts a class by asking
    a sequence of yes or no questions about the predictors, each one splitting the data into two smaller,
    more homogeneous groups, until a stopping point is reached and a class is assigned at each leaf. Decision
    trees are popular because the resulting tree can be read directly: unlike Naive Bayes, which only
    produces a probability from an equation, a tree shows exactly which feature and threshold led to each
    prediction, which makes it easy to explain to someone without a statistics background.</p>
"""

DT_OVERVIEW_2 = """
    <p>Each split in a tree is chosen to make the two resulting groups as pure as possible, meaning each
    group contains mostly one class rather than an even mix. Gini impurity and entropy are the two most
    common ways to measure how mixed a group is: both equal zero when a node is perfectly pure and both are
    highest when classes are evenly split. Information gain is the reduction in entropy (or the equivalent
    reduction in gini, sometimes called the gini gain) achieved by a split, the impurity of the parent node
    minus the weighted average impurity of its two children. The table below works through the actual root
    split chosen for Tree A on this project's data, splitting on 5-year price volatility at 6.44: the parent
    node's gini impurity of 0.667 falls to a weighted average of 0.622 across its two children, a gini gain
    of 0.044, and the parent's entropy of 1.585 falls to a weighted 1.489, an information gain of 0.096.
    Because there is no single rule for which feature to split on first when several give a similar
    improvement, and because a tree can keep splitting until every leaf is pure or runs out of data, an
    essentially unlimited number of different, equally valid trees can be grown from the same data just by
    varying the maximum depth, the impurity measure, or how ties between competing splits are broken.</p>
"""

DT_DATAPREP = """
    <p>Decision trees are also a supervised method and need the same kind of labeled, split data as Naive
    Bayes: a class to predict for every metro, and a disjoint Training Set and Testing Set so accuracy is
    measured on metros the tree never saw while growing. The same 894-metro table and the same 75/25
    stratified 670/224 split used for Naive Bayes are reused here, so the two methods can be compared fairly
    on identical data. Unlike Naive Bayes, trees do not need the predictors binned or binarized, since a
    split just compares one feature to a numeric threshold directly, so the four price-growth and volatility
    predictors are used here on their original continuous scale.</p>
"""

DT_RESULTS = """
    <p>The two shallow trees (max depth 3) perform almost identically regardless of which impurity measure
    built them: Tree A (gini) reaches 58.5 percent test accuracy and Tree B (entropy) reaches 58.0 percent,
    both well above the 33.3 percent random-guessing baseline and meaningfully better than either Naive Bayes
    variant. The unpruned Tree C tells a different story: grown with no depth limit, it reaches 22 levels and
    243 leaves, perfectly memorizing patterns in the 670 training metros, but its test accuracy actually
    falls to 48.2 percent, below even the shallow trees. This is a textbook case of overfitting: a tree
    flexible enough to carve out a leaf for nearly every unusual combination of training rows ends up
    matching noise in that training data rather than a pattern that generalizes to new metros.</p>
"""

DT_CONCL = """
    <p>Letting a model ask a sequence of questions about recent price growth and volatility predicts a
    metro's current affordability class meaningfully better than chance, and better than either Naive Bayes
    variant managed with the same four predictors, but a shallow, limited tree generalizes better than one
    left free to grow as deep as it wants. For this project's underlying question, that argues for favoring
    simpler, more constrained models of housing affordability over more complex ones chasing marginal gains
    on the training data, especially given how few predictors (only four) were available to the model and
    how much of affordability's story, shown already in Module 2, is really about price level rather than
    price movement.</p>
"""
