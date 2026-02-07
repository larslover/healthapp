from django.db import models
from core.utils.processor import bmi_category
# ------------------------------
# Legacy table (existing data)
# ------------------------------
from django.db import models

from django.db import models
from datetime import datetime,date

# ------------------------------
# New system tables
# ------------------------------
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    # Basic student info
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, null=True, blank=True)
   
    
    father_or_guardian_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    
    
    known_earlier_disease = models.TextField(null=True, blank=True)
    

    # Use a ForeignKey to School
    school = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
   
    @property
    def age_in_years(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            # Adjust if birthday hasn't happened yet this year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None
    def age_at_date(self, ref_date):
        """Return age in months at a given date."""
        if self.date_of_birth and ref_date:
            delta = ref_date - self.date_of_birth
            return delta.days // 30
        return None

    def __str__(self):
        return self.name

from django.db import models
from .utils.processor import calculate_age_in_months, calculate_bmi, bmi_category, muac_category
class Screening(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='screenings')
    screen_date = models.DateField(null=True, blank=True)
    class_section = models.CharField(max_length=50, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    screening_year = models.IntegerField(db_index=True, null=True, blank=True)


    # Measurements
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    bmi_category = models.CharField(max_length=50, null=True, blank=True)
    muac = models.FloatField(null=True, blank=True)
    muac_sam = models.CharField(max_length=50, null=True, blank=True)

    # WHO categories
    weight_age = models.TextField(blank=True, null=True)
    length_age = models.TextField(blank=True, null=True)
    weight_height = models.TextField(blank=True, null=True)

    # Vision
    vision_both = models.CharField(max_length=50, null=True, blank=True)
    vision_left = models.CharField(max_length=10, blank=True, null=True)
    vision_right = models.CharField(max_length=10, blank=True, null=True)

    vision_problem = models.TextField(null=True, blank=True)

    # Meta data
    age_in_month = models.IntegerField(null=True, blank=True)
    covid = models.CharField(max_length=50, null=True, blank=True)
    
    
    age_screening = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-screen_date']

    def __str__(self):
        return f"{self.student.name} - {self.screen_date} ({self.class_section})"
    

    def calculate_metrics(self):
        from core.utils.processor import (
        
        weight_height_category,
        evaluate_vision
    )
        """Calculate all WHO metrics safely."""
        if not self.student:
            self.age_in_month = None
            self.bmi = None
            self.bmi_category = "N/A"
            self.muac_sam = "N/A"
            
            self.weight_height = "N/A"
            self.vision_problem = "N/A"
            return

        dob = getattr(self.student, "date_of_birth", None)
        if dob and self.screen_date:
            self.age_in_month = calculate_age_in_months(dob, self.screen_date)
        else:
            self.age_in_month = None

        # Convert to float safely
        weight = float(self.weight) if self.weight else None
        height = float(self.height) if self.height else None

        self.bmi = calculate_bmi(weight, height)

        self.bmi_category = (
            bmi_category(getattr(self.student, "gender", ""), self.age_in_month, self.bmi)
            if self.bmi is not None and self.age_in_month is not None
            else "N/A"
        )

        self.muac_sam = (
            muac_category(self.muac, self.age_in_month)
            if self.muac is not None and self.age_in_month is not None
            else "N/A"
        )

        gender = getattr(self.student, "gender", "")

       
       

        

        self.weight_height = (
            weight_height_category(weight, height, self.age_in_month, gender)
            if weight is not None and height is not None and self.age_in_month is not None
            else "N/A"
        )

     
    def save(self, *args, **kwargs):
        # Auto-calculate screening year from screen_date
        if self.screen_date:
            self.screening_year = self.screen_date.year
        else:
            self.screening_year = None

        self.calculate_metrics()
        super().save(*args, **kwargs)

from django.db import models
from core.models import Screening

class ScreeningCheck(models.Model):
    screening = models.OneToOneField(Screening, on_delete=models.CASCADE, related_name="checklist")

    # Preventive care
    deworming = models.CharField(max_length=50, blank=True, null=True)
    vaccination = models.CharField(max_length=255, blank=True, null=True)

    # Nutritional / medical conditions
    B1_severe_anemia = models.BooleanField(default=False)
    B2_vitA_deficiency = models.BooleanField(default=False)
    B3_vitD_deficiency = models.BooleanField(default=False)
    B4_goitre = models.BooleanField(default=False)
    B5_oedema = models.BooleanField(default=False)

    # Other medical conditions
    C1_convulsive_dis = models.BooleanField(default=False)
    C2_otitis_media = models.BooleanField(default=False)
    C3_dental_condition = models.BooleanField(default=False)
    C4_skin_condition = models.BooleanField(default=False)
    C5_rheumatic_heart_disease = models.BooleanField(default=False)
    C6_others_TB_asthma = models.BooleanField(default=False)

    # Development / learning difficulties
    D1_difficulty_seeing = models.BooleanField(default=False)
    D2_delay_in_walking = models.BooleanField(default=False)
    D3_stiffness_floppiness = models.BooleanField(default=False)
    D5_reading_writing_calculatory_difficulty = models.BooleanField(default=False)
    D6_speaking_difficulty = models.BooleanField(default=False)
    D7_hearing_problems = models.BooleanField(default=False)
    D8_learning_difficulties = models.BooleanField(default=False)

    D9_attention_difficulties = models.BooleanField(default=False)

    # Other observations
    E3_depression_sleep = models.BooleanField(default=False)
    E4_menarke = models.BooleanField(default=False)
    E5_regularity_period_difficulties = models.BooleanField(default=False)
    E6_UTI_STI = models.BooleanField(default=False)
    E7_discharge = models.BooleanField(default=False)
    E8_menstrual_pain = models.BooleanField(default=False)
    E9_remarks = models.TextField(blank=True, null=True)


    class Meta:
        verbose_name = "Screening Check"
        verbose_name_plural = "Screening Checks"

    def __str__(self):
        return f"{self.screening.student.name} - {self.screening.screen_date}"
