"""
Combines the three Soul Foods transaction CSVs in data/ into a single
formatted output file containing only: Sales, Date, Region for Pink Morsels.
"""
import glob
import os
import pandas as pd

DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "formatted_sales_data.csv")

def clean_price(value):
    """Strip $ and commas, return float."""
    if isinstance(value, str):
        value = value.replace("$", "").replace(",", "").strip()
    return float(value)

def main():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    csv_files = [f for f in csv_files if os.path.basename(f) != "formatted_sales_data.csv"]

    if not csv_files:
        raise SystemExit(f"No CSV files found in {DATA_DIR}/")

    frames = []
    for file in csv_files:
        df = pd.read_csv(file)
        # normalise column names to lowercase for consistent access
        df.columns = [c.strip().lower() for c in df.columns]
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    # keep only Pink Morsel rows (case-insensitive)
    combined = combined[combined["product"].str.strip().str.lower() == "pink morsel"]

    # compute sales = quantity * price
    combined["price"] = combined["price"].apply(clean_price)
    combined["sales"] = combined["quantity"].astype(float) * combined["price"]

    # build final output with required column names/order
    result = combined[["sales", "date", "region"]].rename(
        columns={"sales": "Sales", "date": "Date", "region": "Region"}
    )

    result.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(result)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()