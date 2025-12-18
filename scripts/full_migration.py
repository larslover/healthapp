import os
import sys
import sqlite3
from datetime import datetime, date

# --- Add project root to sys.path ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# --- Set Django settings ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.prod")

import django
django.setup()

from core.models import Student, Screening, ScreeningCheck, School
from core.utils.processor import weight_height_female_thresholds, weight_height_male_thresholds
def clean_contact(c):
    if not c:
        return None

    c = str(c).strip()

    # Extract only digits
    digits = "".join(ch for ch in c if ch.isdigit())

    # If length is unrealistic, skip it
    if len(digits) < 7 or len(digits) > 15:
        return None

    return digits

# -----------------------------
# Helpers
# -----------------------------
def parse_date_safe(dob_str):
    if not dob_str:
        return None
    dob_str = dob_str.strip()
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%y"]
    for fmt in formats:
        try:
            return datetime.strptime(dob_str, fmt).date()
        except ValueError:
            continue
    return None


def get_or_create_school(school_name):
    if not school_name:
        return None
    school, _ = School.objects.get_or_create(name=school_name.strip())
    return school


def text_to_bool(text):
    return str(text).strip().lower() == "yes"


def safe_float(value, min_value=0.1):
    try:
        f = float(value)
        return f if f > 0 else min_value
    except (TypeError, ValueError):
        return min_value


def safe_muac(raw):
    """Return MUAC as float or None if empty/invalid."""
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# -----------------------------
# Connect to SQLite
# -----------------------------
sqlite_db_path = "gracehealth.db"
conn = sqlite3.connect(sqlite_db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM student")
rows = cursor.fetchall()
print(f"Total records in SQLite: {len(rows)}")

# -----------------------------
# Migrate each row
# -----------------------------
for row in rows:

    # --- Student ---
    dob = parse_date_safe(row["date_of_birth"])
    student, _ = Student.objects.get_or_create(
        name=row["name"] or "Unnamed",
        date_of_birth=dob or date(2000, 1, 1),
        defaults={
            "gender": row["Gender"],
            "father_or_guardian_name": row["Father_or_guardian_name"],
            "mother_name": row["mother_name"],
            "contact_number": clean_contact(row["contact_number"]),

            "address": row["Address"],
            "known_earlier_disease": row["known_earlier_disease"],
            "school": get_or_create_school(row["school_name"]),
        }
    )

    # --- Screening ---
    screen_date = parse_date_safe(row["screen_date"]) or date.today()

    weight_val = safe_float(row["weight"])
    # Convert raw height to float, but return None if invalid/missing
    height_val = safe_float(row["height"], min_value=None)

    # Adjust to closest WHO height only if height is valid and student has gender
    if height_val is not None and student.gender:
        gender_lower = student.gender.lower().strip()
        thresholds = weight_height_female_thresholds if gender_lower == "female" else weight_height_male_thresholds

        # Get all numeric heights from thresholds
        all_heights = [
            float(h)
            for h in thresholds.keys()
            if str(h).replace(".", "", 1).isdigit()
        ]

        # Pick closest WHO height
        closest_height = min(all_heights, key=lambda h: abs(h - height_val))
        height_val = closest_height

    # Create Screening
    screening = Screening.objects.create(
        student=student,
        screen_date=screen_date,
        class_section=row["Class_section"],
        school=student.school,
        weight=weight_val,
        height=height_val,
        muac=safe_muac(row["muac"]),  # <-- FIXED MUAC
        vision_both=row["Vision_both"],
        vision_left=str(row["VISON_left"]) if row["VISON_left"] else None,
        vision_right=str(row["VISON_right"]) if row["VISON_right"] else None,
    )

    # --- ScreeningCheck ---
    ScreeningCheck.objects.create(
        screening=screening,
        deworming=row["deworming"],
        vaccination=row["vaccination"],
        B1_severe_anemia=text_to_bool(row["B1_severe_anemia"]),
        B2_vitA_deficiency=text_to_bool(row["B2_Vita_A_deficiency"]),
        B3_vitD_deficiency=text_to_bool(row["B3_Vit_D_deficiency"]),
        B4_goitre=text_to_bool(row["B4_Goitre"]),
        B5_oedema=text_to_bool(row["B5_Oedema"]),
        C1_convulsive_dis=text_to_bool(row["C1_convulsive_dis"]),
        C2_otitis_media=text_to_bool(row["C2_otitis_media"]),
        C3_dental_condition=text_to_bool(row["C3_dental_condition"]),
        C4_skin_condition=text_to_bool(row["C4_skin_condition"]),
        C5_rheumatic_heart_disease=text_to_bool(row["C5_rheumatic_heart_disease"]),
        C6_others_TB_asthma=text_to_bool(row["C6_others_TB_asthma"]),
        D1_difficulty_seeing=text_to_bool(row["D1_difficulty_seeing"]),
        D2_delay_in_walking=text_to_bool(row["D2_delay_in_walking"]),
        D3_stiffness_floppiness=text_to_bool(row["D3_stiffness_floppiness"]),
        D5_reading_writing_calculatory_difficulty=text_to_bool(row["D5_reading_writing_calculatory_difficulty"]),
        D6_speaking_difficulty=text_to_bool(row["D6_speaking_difficulty"]),
        D7_hearing_problems=text_to_bool(row["D7_hearing_problems"]),
        D8_learning_difficulties=text_to_bool(row["D8_learning"]),
        D9_attention_difficulties=text_to_bool(row["D9_attention"]),
        E3_depression_sleep=text_to_bool(row["E3_depression_sleep"]),
        E4_menarke=text_to_bool(row["E4_Menarke"]),
        E5_regularity_period_difficulties=text_to_bool(row["E5_regularity_period_difficulties"]),
        E6_UTI_STI=text_to_bool(row["E6_UTI_STI"]),
        E7_discharge=text_to_bool(row["E7"]),
        E8_menstrual_pain=text_to_bool(row["E8_menstrual_pain"]),
        E9_remarks=row["E9_remarks"],
    )

print(f"Migration completed: {len(rows)} students migrated.")
conn.close()
