# core/utils/processor.py

# =========================
# Database helper functions
# =========================




# =========================
# Health calculation utils
# =========================
from datetime import date
from .thresholds import bmi_thresholds_female, bmi_thresholds_male

# core/utils/processor.py
from core.utils.thresholds import vision_list, critical_vision_set

def evaluate_vision(left_vision: str, right_vision: str) -> str:
    """
    Determine if a student's vision is problematic.

    Args:
        left_vision (str): Left eye vision string from VISION_LIST.
        right_vision (str): Right eye vision string from VISION_LIST.

    Returns:
        str: 'yes' if vision is problematic, 'no' if normal, 'invalid' if inputs are invalid.
    """
    try:
        left_index = vision_list.index(left_vision)
        right_index = vision_list.index(right_vision)
    except ValueError:
        return "invalid"

    if left_vision in critical_vision_set or right_vision in critical_vision_set:
        return "yes"

    # If difference between eyes > 2 steps, also considered problematic
    if abs(left_index - right_index) > 2:
        return "yes"

    return "no"

# Before using in processor, convert keys to int
bmi_thresholds_female = {int(k): v for k, v in bmi_thresholds_female.items()}
bmi_thresholds_male   = {int(k): v for k, v in bmi_thresholds_male.items()}

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
    """
    Calculate BMI category based on WHO thresholds.
    Returns: 'severe underweight', 'underweight', 'normal', 'overweight', or 'obese'.
    """
    gender = (gender or "").lower()
    if gender not in ["male", "female"]:
        return "N/A"

    thresholds = bmi_thresholds_female if gender == "female" else bmi_thresholds_male

    try:
        age_months = int(age_months)
    except (TypeError, ValueError):
        return "N/A"

    # Only support ages 61–228 months (5–19 years)
    if age_months < 61 or age_months > 228 or age_months not in thresholds:
        return "N/A"

    severe, underweight, overweight, obese = thresholds[age_months]

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

from .thresholds import weight_female_thresholds, weight_male_thresholds


from .thresholds import weight_female_thresholds, weight_male_thresholds

def weight_age_category(weight, age_in_months, gender):
    """
    Classify weight-for-age category using WHO thresholds.
    Returns: 'Severely Underweight', 'Moderately Underweight', or 'Normal'.
    """

    # Guard against missing or invalid inputs
    if not (weight and age_in_months and gender):
        return "N/A"

    gender = gender.lower().strip()
    thresholds = weight_female_thresholds if gender == "female" else weight_male_thresholds

    # Use the nearest month in WHO table if exact age missing
    all_months = sorted(thresholds.keys())
    closest_age = min(all_months, key=lambda m: abs(m - age_in_months))

    lower, upper = thresholds[closest_age]

    # Smooth classification logic
    if weight < lower:
        return "Severely Underweight"
    elif weight < upper:
        return "Moderately Underweight"
    else:
        return "Normal"

from .thresholds import height_age_female_thresholds, height_age_male_thresholds

def height_age_category(height, age_in_months, gender):
    """
    Determine height-for-age (stunting) category based on WHO thresholds.
    Returns: 'Severe Stunting', 'Moderate Stunting', 'Normal', or 'N/A'.
    """

    # Validate inputs
    if not (height and age_in_months and gender):
        return "N/A"

    gender = gender.lower().strip()
    thresholds = height_age_female_thresholds if gender == "female" else height_age_male_thresholds

    # Find nearest available month
    all_months = sorted(thresholds.keys())
    closest_age = min(all_months, key=lambda m: abs(m - age_in_months))

    lower, upper = thresholds[closest_age]

    # Classification logic
    if height < lower:
        return "Severe Stunting"
    elif lower <= height < upper:
        return "Moderate Stunting"
    else:
        return "Normal"
from .thresholds import weight_height_female_thresholds, weight_height_male_thresholds

def weight_height_category(weight, height, age_in_months, gender):
    """
    Determine weight-for-height category based on WHO thresholds.
    Returns: 'Severe Acute Malnutrition', 'Moderate Acute Malnutrition', 
             'Normal', 'Overweight', 'Obese', or 'N/A'.
    """

    # Validate inputs
    if not (weight and height and age_in_months and gender):
        return "N/A"

    gender = gender.lower().strip()
    thresholds = weight_height_female_thresholds if gender == "female" else weight_height_male_thresholds

    # Find closest height in WHO table
    all_heights = sorted(thresholds.keys())
    closest_height = min(all_heights, key=lambda h: abs(h - height))

    # Extract thresholds for weight classification
    v1, v2, v3, v4 = thresholds[closest_height]

    if weight < v1:
        return "Severe Acute Malnutrition"
    elif weight < v2:
        return "Moderate Acute Malnutrition"
    elif v2 <= weight <= v3:
        return "Normal"
    elif v3 < weight <= v4:
        return "Overweight"
    elif weight > v4:
        return "Obese"
