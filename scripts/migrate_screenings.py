import os
import sys
from datetime import datetime

# -----------------------------
# Django Setup
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.dev")

import django
django.setup()

# -----------------------------
# Imports
# -----------------------------
from core.models import Student, School, LegacyStudent, Screening, ScreeningCheck

# -----------------------------
# Helper functions
# -----------------------------
def parse_date(date_str):
    """Try multiple date formats safely."""
    if not date_str:
        return None
    date_str = str(date_str).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def yes_to_bool(val):
    """Convert legacy 'Yes'/'No' or truthy string to boolean."""
    return str(val).strip().lower() == 'yes'

# -----------------------------
# Migration
# -----------------------------
legacy_students = LegacyStudent.objects.all()
total = legacy_students.count()
print(f"Found {total} legacy students.\n")

created_screenings = 0

for idx, legacy in enumerate(legacy_students, 1):

    # --- Find or Create School ---
    school_obj = None
    if legacy.school_name:
        school_obj, _ = School.objects.get_or_create(name=legacy.school_name.strip())

    # --- Find or Create Student ---
    student, _ = Student.objects.get_or_create(
        name=legacy.name or f"Unnamed Student {idx}",
        defaults={
            "date_of_birth": parse_date(legacy.date_of_birth),
            "gender": legacy.gender,
            "father_or_guardian_name": legacy.father_or_guardian_name,
            "mother_name": legacy.mother_name,
            "contact_number": str(legacy.contact_number) if legacy.contact_number else None,
            "address": legacy.address,
            "school": school_obj,
            "known_earlier_disease": legacy.known_earlier_disease,
        }
    )

    # --- Create Screening ---
    screening = Screening.objects.create(
        student=student,
        screen_date=parse_date(legacy.screen_date),
        class_section=legacy.class_section,
        school=school_obj,
        weight=to_float(legacy.weight),
        height=to_float(legacy.height),
        muac=to_float(legacy.muac),
        vision_both=legacy.Vision_both,
        vision_left=legacy.VISON_left,
        vision_right=legacy.VISON_right,
        covid=legacy.covid,
    )

    # --- Create ScreeningCheck ---
    ScreeningCheck.objects.create(
        screening=screening,
        deworming=legacy.deworming,
        vaccination=legacy.vaccination,
        B1_severe_anemia=yes_to_bool(legacy.B1_severe_anemia),
        B2_vitA_deficiency=yes_to_bool(legacy.B2_Vita_A_deficiency),
        B3_vitD_deficiency=yes_to_bool(legacy.B3_Vit_D_deficiency),
        B4_goitre=yes_to_bool(legacy.B4_Goitre),
        B5_oedema=yes_to_bool(legacy.B5_Oedema),
        C1_convulsive_dis=yes_to_bool(legacy.C1_convulsive_dis),
        C2_otitis_media=yes_to_bool(legacy.C2_otitis_media),
        C3_dental_condition=yes_to_bool(legacy.C3_dental_condition),
        C4_skin_condition=yes_to_bool(legacy.C4_skin_condition),
        C5_rheumatic_heart_disease=yes_to_bool(legacy.C5_rheumatic_heart_disease),
        C6_others_TB_asthma=yes_to_bool(legacy.C6_others_TB_asthma),
        D1_difficulty_seeing=yes_to_bool(legacy.D1_difficulty_seeing),
        D2_delay_in_walking=yes_to_bool(legacy.D2_delay_in_walking),
        D3_stiffness_floppiness=yes_to_bool(legacy.D3_stiffness_floppiness),
        D5_reading_writing_calculatory_difficulty=yes_to_bool(legacy.D5_reading_writing_calculatory_difficulty),
        D6_speaking_difficulty=yes_to_bool(legacy.D6_speaking_difficulty),
        D7_hearing_problems=yes_to_bool(legacy.D7_hearing_problems),
        D8_learning_difficulties=yes_to_bool(legacy.D8_learning_difficulties),
        D9_attention_difficulties=yes_to_bool(legacy.D9_attention_difficulties),
        E3_depression_sleep=yes_to_bool(legacy.E3_depression_sleep),
        E4_menarke=yes_to_bool(legacy.E4_Menarke),
        E5_regularity_period_difficulties=yes_to_bool(legacy.E5_regularity_period_difficulties),
        E6_UTI_STI=yes_to_bool(legacy.E6_UTI_STI),
        E7_discharge=yes_to_bool(legacy.E7_discharge),
        E8_menstrual_pain=yes_to_bool(legacy.E8_menstrual_pain),
        E9_remarks=legacy.E9_remarks,
    )

    created_screenings += 1
    print(f"[{idx}/{total}] Migrated screening for {student.name}")

print(f"\n🎉 Migration complete! Successfully created {created_screenings} screenings.\n")
