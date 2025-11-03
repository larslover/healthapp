from datetime import date

# === Import WHO reference thresholds ===
from core.utils.bmi_thresholds_boys import bmi_thresholds_male
from core.utils.bmi_thresholds_girls import bmi_thresholds_female
from core.utils.thresholds import (
    vision_list,
    critical_vision_set,

)
from core.utils.weight_height_female_thresholds import weight_height_female_thresholds
from core.utils.weight_height_male_thresholds import weight_height_male_thresholds



# ============================================================
# Vision Evaluation
# ============================================================
def evaluate_vision(left_vision: str, right_vision: str) -> str:
    """
    Determine if a student's vision is problematic.

    Returns:
        'yes'      -> if vision is problematic,
        'no'       -> if normal,
        'invalid'  -> if input not recognized.
    """
    try:
        left_index = vision_list.index(left_vision)
        right_index = vision_list.index(right_vision)
    except ValueError:
        return "invalid"

    if left_vision in critical_vision_set or right_vision in critical_vision_set:
        return "yes"

    # If difference between eyes > 2 steps → problematic
    if abs(left_index - right_index) > 2:
        return "yes"

    return "no"


# ============================================================
# Age, BMI, and MUAC Calculations
# ============================================================
def calculate_age_in_months(dob: date, reference_date: date) -> int:
    """Calculate a student's age in months."""
    months = (reference_date.year - dob.year) * 12 + (reference_date.month - dob.month)
    if reference_date.day < dob.day:
        months -= 1
    return months


def calculate_bmi(weight: float, height_cm: float) -> float | None:
    """Calculate BMI given weight (kg) and height (cm)."""
    if not weight or not height_cm or height_cm == 0:
        return None
    return round(weight / ((height_cm / 100) ** 2), 2)


def bmi_category(gender: str, age_months: int, bmi_value: float) -> str:
    """
    Classify BMI based on WHO 5–19 years reference data (−3SD to +3SD).

    Returns:
        'severe underweight', 'moderate underweight', 'mild underweight',
        'normal', 'overweight', 'obese', or 'N/A'.
    """
    gender = str(gender or "").lower()
    if gender not in ["male", "female"]:
        return "N/A"

    thresholds = bmi_thresholds_female if gender == "female" else bmi_thresholds_male

    try:
        age_months = int(age_months)
    except (TypeError, ValueError):
        return "N/A"

    if age_months not in thresholds:
        return "N/A"

    minus3SD, minus2SD, minus1SD, median, plus1SD, plus2SD, plus3SD = thresholds[age_months]

    if bmi_value < minus3SD:
        return "severe underweight"
    elif bmi_value < minus2SD:
        return "moderate underweight"
    elif bmi_value < minus1SD:
        return "mild underweight"
    elif bmi_value < plus1SD:
        return "normal"
    elif bmi_value < plus2SD:
        return "overweight"
    else:
        return "obese"


def muac_category(muac_value: float, age_months: int) -> str:
    """
    Classify MUAC (Mid-Upper Arm Circumference) for ages 6–60 months.
    Returns: 'normal', 'severe acute malnutrition', or 'N/A'.
    """
    if age_months < 6 or age_months > 60:
        return "N/A"
    return "normal" if muac_value >= 11.5 else "severe acute malnutrition"


# ============================================================
# Weight-for-Height Category
# ============================================================
def weight_height_category(weight: float, height: float, age_in_months: int, gender: str) -> str:
    """
    Determine weight-for-height category based on WHO thresholds.
    Only for ages 24–60 months inclusive.
    """

    if not (weight and height and gender):
        return "N/A"

    # Age restriction
    if age_in_months < 24 or age_in_months > 60:
        return "N/A"

    gender = gender.lower().strip()
    thresholds = (
        weight_height_female_thresholds
        if gender == "female"
        else weight_height_male_thresholds
    )

    # Find closest available height
    all_heights = sorted(thresholds.keys())
    closest_height = min(all_heights, key=lambda h: abs(h - height))

    # Unpack WHO SD lines
    sd3neg, sd2neg, sd1neg, sd0, sd1, sd2, sd3 = thresholds[closest_height]

    # Classify
    if weight < sd3neg:
        return "Severe Acute Malnutrition"
    elif weight < sd2neg:
        return "Moderate Acute Malnutrition"
    elif sd2neg <= weight <= sd1:
        return "Normal"
    elif sd1 < weight <= sd2:
        return "Overweight"
    elif weight > sd2:
        return "Obese"
    return "N/A"
