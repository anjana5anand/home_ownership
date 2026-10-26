"""
Small reference images for the Naive Bayes / Decision Trees Data Prep
sections: a sample of the labeled dataset, and the train/test split.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = "data_clean"
IMG_DIR = "docs/images"

SURFACE = "#fcfcfb"
HEADER_BG = "#ede7dc"
INK = "#0b0b0b"
MUTED = "#5a544c"
GRID = "#e7e3dc"

def render_table(df, title, fname, col_widths=None):
    fig, ax = plt.subplots(figsize=(10.2, 0.42 * (len(df) + 1) + 0.3), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axis("off")
    tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="upper center",
                   colWidths=col_widths)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.8)
    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor(GRID)
        if row == 0:
            cell.set_facecolor(HEADER_BG)
            cell.set_text_props(weight="bold", color=INK)
        else:
            cell.set_facecolor(SURFACE)
            cell.set_text_props(color=INK)
    ax.set_title(title, fontsize=13, color=MUTED, pad=10)
    fig.subplots_adjust(top=0.82, bottom=0.02, left=0.02, right=0.98)
    fig.savefig(f"{IMG_DIR}/{fname}", facecolor=SURFACE)
    plt.close(fig)

full = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised.csv")
sample = full.head(6)[["region_name", "zhvi_yoy_pct", "zhvi_3yr_pct", "zhvi_5yr_pct",
                        "zhvi_volatility_5yr", "payment_to_income_pct_25_34", "affordability_class"]].copy()
sample.columns = ["metro", "1yr chg %", "3yr chg %", "5yr chg %", "5yr volatility", "payment % income", "class"]
for c in ["1yr chg %", "3yr chg %", "5yr chg %", "5yr volatility", "payment % income"]:
    sample[c] = sample[c].round(2)
render_table(sample, "First 6 of 894 rows, metro_2025_supervised.csv (4 predictors + label shown)",
             "data-sample-supervised.png", col_widths=[0.17, 0.13, 0.13, 0.13, 0.14, 0.18, 0.15])

train = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_test.csv")

split_summary = pd.DataFrame({
    "set": ["Training", "Testing", "Total"],
    "n_metros": [len(train), len(test), len(train) + len(test)],
    "Affordable": [
        (train.affordability_class == "Affordable").sum(),
        (test.affordability_class == "Affordable").sum(),
        (full.affordability_class == "Affordable").sum(),
    ],
    "Moderate": [
        (train.affordability_class == "Moderate").sum(),
        (test.affordability_class == "Moderate").sum(),
        (full.affordability_class == "Moderate").sum(),
    ],
    "Burdened": [
        (train.affordability_class == "Burdened").sum(),
        (test.affordability_class == "Burdened").sum(),
        (full.affordability_class == "Burdened").sum(),
    ],
})
render_table(split_summary, "75/25 stratified train/test split (random_state=42), by affordability class",
             "data-split-supervised.png")

print("wrote data-sample-supervised.png and data-split-supervised.png")
