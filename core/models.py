from django.db import models

# ------------------------------
# Legacy table (existing data)
# ------------------------------
from django.db import models

class LegacyStudent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    date_of_birth = models.TextField(blank=True, null=True)
    gender = models.TextField(db_column='Gender', blank=True, null=True)
    class_section = models.TextField(db_column='Class_section', blank=True, null=True)
    roll_no = models.IntegerField(db_column='Roll_no', blank=True, null=True)
    aadhaar_no = models.IntegerField(db_column='Aadhaar_No', blank=True, null=True)
    father_or_guardian_name = models.TextField(db_column='Father_or_guardian_name', blank=True, null=True)
    mother_name = models.TextField(blank=True, null=True)
    contact_number = models.IntegerField(blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    name_teacher = models.TextField(db_column='Name_teacher', blank=True, null=True)
    school_name = models.TextField(blank=True, null=True)
    last_school_name = models.TextField(blank=True, null=True)
    place_of_birth = models.TextField(blank=True, null=True)
    known_earlier_disease = models.TextField(blank=True, null=True)
    covid_vacc_number = models.IntegerField(blank=True, null=True)
    covd_vacc_last_date = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    BMI = models.TextField(blank=True, null=True)
    Vision_both = models.TextField(blank=True, null=True)
    VISON_left = models.IntegerField(blank=True, null=True)
    VISON_right = models.IntegerField(blank=True, null=True)
    VISION_problem = models.TextField(blank=True, null=True)
    B1_severe_anemia = models.TextField(blank=True, null=True)
    B2_Vita_A_deficiency = models.TextField(blank=True, null=True)
    B3_Vit_D_deficiency = models.TextField(blank=True, null=True)
    B4_Goitre = models.TextField(blank=True, null=True)
    B5_Oedema = models.TextField(blank=True, null=True)
    C1_convulsive_dis = models.TextField(blank=True, null=True)
    C2_otitis_media = models.TextField(blank=True, null=True)
    C3_dental_condition = models.TextField(blank=True, null=True)
    C4_skin_condition = models.TextField(blank=True, null=True)
    C5_rheumatic_heart_disease = models.TextField(blank=True, null=True)
    C6_others_TB_asthma = models.TextField(blank=True, null=True)
    D1_difficulty_seeing = models.TextField(blank=True, null=True)
    D2_delay_in_walking = models.TextField(blank=True, null=True)
    D3_stiffness_floppiness = models.TextField(blank=True, null=True)
    D5_reading_writing_calculatory_difficulty = models.TextField(blank=True, null=True)
    D6_speaking_difficulty = models.TextField(blank=True, null=True)
    D7_hearing_problems = models.TextField(blank=True, null=True)
    D8_learning_difficulties = models.TextField(blank=True, null=True)  
    D9_attention_difficulties = models.TextField(db_column='D9_attention_difficulties', blank=True, null=True)

    E3_depression_sleep = models.TextField(blank=True, null=True)
    E4_Menarke = models.TextField(blank=True, null=True)
    E5_regularity_period_difficulties = models.TextField(blank=True, null=True)
    E6_UTI_STI = models.TextField(blank=True, null=True)
    E7_discharge = models.TextField(db_column='E7_Discharge', blank=True, null=True)

    E8_menstrual_pain = models.TextField(blank=True, null=True)
    E9_remarks = models.TextField(blank=True, null=True)
    BMI_category = models.TextField(blank=True, null=True)
    weight_age = models.TextField(blank=True, null=True)
    length_age = models.TextField(blank=True, null=True)
    weight_height = models.TextField(blank=True, null=True)
    age_in_month = models.IntegerField(blank=True, null=True)
    deworming = models.TextField(blank=True, null=True)
    vaccination = models.TextField(blank=True, null=True)
    covid = models.TextField(blank=True, null=True)
    tea_garden = models.TextField(blank=True, null=True)
    screen_date = models.TextField(blank=True, null=True)
    age_screening = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    muac = models.IntegerField(blank=True, null=True)
    muac_sam = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Django won't touch this table
        db_table = 'student'
        app_label = 'core'  # if model lives in core app

    def __str__(self):
        return self.name or "Unnamed Legacy Student"


# ------------------------------
# New system tables
# ------------------------------
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

from django.db import models

class Student(models.Model):
    # Basic student info
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, null=True, blank=True)
    roll_no = models.IntegerField(null=True, blank=True)
    aadhaar_no = models.CharField(max_length=20, null=True, blank=True)
    father_or_guardian_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    last_school_name = models.CharField(max_length=255, null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    known_earlier_disease = models.TextField(null=True, blank=True)

    # Use a ForeignKey to School
    school = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    current_class_section = models.CharField(max_length=50, null=True, blank=True)
    current_teacher = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Screening(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='screenings')
    screen_date = models.DateField(null=True, blank=True)
    class_section = models.CharField(max_length=50, null=True, blank=True)  # moved here
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)  # optional

    # health measurements
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    bmi_category = models.CharField(max_length=50, null=True, blank=True)
    muac = models.FloatField(null=True, blank=True)
    muac_sam = models.CharField(max_length=50, null=True, blank=True)

    # additional health/vision fields
    vision_both = models.CharField(max_length=50, null=True, blank=True)
    vison_left = models.IntegerField(null=True, blank=True)
    vison_right = models.IntegerField(null=True, blank=True)
    vision_problem = models.TextField(null=True, blank=True)

    # optional tracking
    age_in_month = models.IntegerField(null=True, blank=True)
    deworming = models.CharField(max_length=50, null=True, blank=True)
    vaccination = models.CharField(max_length=255, null=True, blank=True)
    covid = models.CharField(max_length=50, null=True, blank=True)
    tea_garden = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    age_screening = models.CharField(max_length=50, null=True, blank=True)
    def calculate_bmi(self):
        """Calculate BMI based on weight and height."""
        if not self.weight or not self.height or self.height == 0:
            return None  # Cannot calculate
        bmi = self.weight / ((self.height / 100) ** 2)
        self.bmi = round(bmi, 2)  # store BMI rounded to 2 decimal places
        return self.bmi

    class Meta:
        ordering = ['-screen_date']

    def __str__(self):
        return f"{self.student.name} - {self.screen_date} ({self.class_section})"
