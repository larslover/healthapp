import pandas as pd
from pathlib import Path

# Path to your Excel file (adjust if needed)
excel_path = Path("/Users/larslover/Downloads/wfh_girls_2-to-5-years_zscores.xlsx")

# Read the file — if it's not the first sheet, specify sheet_name
df = pd.read_excel(excel_path)

# Normalize column names (strip spaces and lowercase)
df.columns = [str(c).strip().lower() for c in df.columns]

# Expected columns based on your screenshot
expected = ["height", "sd3neg", "sd2neg", "sd1neg", "sd0", "sd1", "sd2", "sd3"]
missing = [c for c in expected if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

# Build dictionary
thresholds = {}
for _, row in df.iterrows():
    height = round(float(row["height"]), 1)
    thresholds[height] = (
        round(float(row["sd3neg"]), 2),
        round(float(row["sd2neg"]), 2),
        round(float(row["sd1neg"]), 2),
        round(float(row["sd0"]), 2),
        round(float(row["sd1"]), 2),
        round(float(row["sd2"]), 2),
        round(float(row["sd3"]), 2),
    )

# Output path for your project
output_path = Path("/Users/larslover/healthapp/core/utils/weight_height_girls.py")

# Write the dictionary to file
with open(output_path, "w") as f:
    f.write("# Auto-generated from WHO reference data\n")
    f.write("# Height (cm) → (−3SD, −2SD, −1SD, median, +1SD, +2SD, +3SD)\n\n")
    f.write("weight_height_female_thresholds = {\n")
    for h, v in thresholds.items():
        f.write(f"    {h}: {v},\n")
    f.write("}\n")

print(f"✅ Extracted {len(thresholds)} height thresholds")
print(f"Saved to: {output_path}")
