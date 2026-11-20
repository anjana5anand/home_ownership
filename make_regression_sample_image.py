"""
Sample-data image for the Regression / AdaBoost Data Prep sections,
showing the two new Module 4 targets alongside the existing predictors:
payment_to_income_pct_25_34 (numeric target for linear regression) and
is_burdened (two-class label for logistic regression).
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
    fig, ax = plt.subplots(figsize=(10.6, 0.42 * (len(df) + 1) + 0.3), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axis("off")
    tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="upper center",
                   colWidths=col_widths)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10.5)
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

full = pd.read_csv(f"{OUT_DIR}/metro_2025_regression.csv")
sample = full.head(6)[["region_name", "zhvi_yoy_pct", "zhvi_3yr_pct", "zhvi_5yr_pct",
                        "zhvi_volatility_5yr", "payment_to_income_pct_25_34", "is_burdened"]].copy()
sample.columns = ["metro", "1yr chg %", "3yr chg %", "5yr chg %", "5yr volat.",
                   "payment %\nincome", "is_burdened"]
for c in ["1yr chg %", "3yr chg %", "5yr chg %", "5yr volat.", "payment %\nincome"]:
    sample[c] = sample[c].round(2)
render_table(sample, "First 6 of 894 rows, metro_2025_regression.csv: 4 predictors, payment % income\n(linear regression target), is_burdened (logistic regression target)",
             "data-sample-regression.png", col_widths=[0.19, 0.12, 0.12, 0.12, 0.13, 0.15, 0.17])

print("wrote data-sample-regression.png")
