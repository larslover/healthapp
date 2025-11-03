import pandas as pd
import json

# Path to your WHO Weight-for-Height boys file
excel_path = "/Users/larslover/Downloads/wfh_boys_2-to-5-years_zscores.xlsx"

# Read the Excel file
df = pd.read_excel(excel_path)

# Expected columns in WHO format
# Height | L | M | S | SD3neg | SD2neg | SD1neg | SD0 | SD1 | SD2 | SD3
expected_cols = ["Height", "L", "M", "S", "SD3neg", "SD2neg", "SD1neg", "SD0", "SD1", "SD2", "SD3"]
df.columns = expected_cols[:len(df.columns)]  # truncate in case of header mismatches

# Extract thresholds as a dictionary
weight_height_male_thresholds = {}

for _, row in df.iterrows():
    height = round(float(row["Height"]), 1)
    thresholds = (
        float(row["SD3neg"]),
        float(row["SD2neg"]),
        float(row["SD1neg"]),
        float(row["SD0"]),
        float(row["SD1"]),
        float(row["SD2"]),
        float(row["SD3"]),
    )
    weight_height_male_thresholds[height] = thresholds

# Output path
output_path = "/Users/larslover/healthapp/core/utils/weight_height_male_thresholds.py"

# Save to .py
with open(output_path, "w") as f:
    f.write("# WHO Weight-for-Height (Boys, 2–5 years)\n")
    f.write("weight_height_male_thresholds = ")
    f.write(json.dumps(weight_height_male_thresholds, indent=4))

print(f"✅ Extracted {len(weight_height_male_thresholds)} height entries and saved to {output_path}")
