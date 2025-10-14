# core/utils/processor.py

# =========================
# Database helper functions
# =========================




# =========================
# Health calculation utils
# =========================
from datetime import date
from .thresholds import bmi_thresholds_female, bmi_thresholds_male

def calculate_age_in_months(dob: date, reference_date: date) -> int:
    months = (reference_date.year - dob.year) * 12 + (reference_date.month - dob.month)
    if reference_date.day < dob.day:
        months -= 1
    return months

def calculate_bmi(weight: float, height_cm: float) -> float | None:
    if not weight or not height_cm or height_cm == 0:
        return None
    return round(weight / ((height_cm / 100) ** 2), 2)

def bmi_category(gender: str, age_months: int, bmi_value: float) -> str:
    gender = (gender or "").lower()
    if gender not in ["male", "female"]:
        return "N/A"
    thresholds = bmi_thresholds_female if gender == "female" else bmi_thresholds_male
    age_str = str(age_months)
    if age_months < 61 or age_months > 228 or age_str not in thresholds:
        return "N/A"
    severe, underweight, overweight, obese = thresholds[age_str]
    if bmi_value <= severe:
        return "severe underweight"
    elif bmi_value <= underweight:
        return "underweight"
    elif bmi_value < overweight:
        return "normal"
    elif bmi_value < obese:
        return "overweight"
    return "obese"

def muac_category(muac_value: float, age_months: int) -> str:
    if age_months < 6 or age_months > 60:
        return "N/A"
    return "normal" if muac_value >= 11.5 else "severe acute malnutrition"
