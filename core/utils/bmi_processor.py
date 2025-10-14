# core/utils/bmi_processor.py
from .bmi_thresholds import bmi_thresholds_female, bmi_thresholds_male

def bmi_category(gender: str, month: str, bmi_value: float) -> str:
    """Return BMI category string based on gender, age in months, and BMI."""
    gender = (gender or "").lower()
    if gender not in ["male", "female"]:
        return "N/A"

    thresholds = bmi_thresholds_female if gender == "female" else bmi_thresholds_male

    try:
        month_int = int(month)
    except (ValueError, TypeError):
        return "N/A"

    if month_int < 61 or month_int > 228 or month not in thresholds:
        return "N/A"

    severe, underweight, overweight, obese = thresholds[month]

    if bmi_value <= severe:
        return "severe underweight"
    elif bmi_value <= underweight:
        return "underweight"
    elif bmi_value < overweight:
        return "normal"
    elif bmi_value < obese:
        return "overweight"
    else:
        return "obese"
