import pdfplumber
import re
import json
from pathlib import Path

# Paths
pdf_path = Path("/Users/larslover/Downloads/bmifa-boys-5-19years-z.pdf")
output_path = Path("/Users/larslover/healthapp/core/utils/bmi_thresholds_boys.py")

bmi_thresholds_girls = {}

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.splitlines():
            # Match lines like: 5: 1 61 -0.8886 15.2441 0.09692 11.8 12.7 13.9 15.2 16.9 18.9 21.3
            match = re.match(
                r"^\d+:\s*\d+\s+(\d+)\s+-?\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+([\d\s\.]+)$",
                line,
            )
            if match:
                month = int(match.group(1))
                values = [float(v) for v in match.group(2).split()]
                if len(values) == 7:
                    bmi_thresholds_girls[month] = tuple(values)

# Write to its own file (safe)
output_path.write_text(
    "bmi_thresholds_girls = " + json.dumps(bmi_thresholds_girls, indent=4)
)

print(f"✅ Extracted {len(bmi_thresholds_girls)} entries → {output_path}")
