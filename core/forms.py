from django import forms
from .models import Student, Screening, School

from django import forms
from core.models import Student, Screening

# core/forms.py
from django import forms
from .models import Student, Screening, School

from django import forms








from .models import Student, School
class StudentForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
       
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    school = forms.ModelChoiceField(
        queryset=School.objects.all().order_by('name'),
        required=False,
        empty_label='Select School',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Student
        fields = [
            'name', 'date_of_birth', 'gender', 'roll_no', 'aadhaar_no',
            'father_or_guardian_name', 'mother_name', 'contact_number',
            'address', 'email', 'last_school_name', 'place_of_birth',
            'known_earlier_disease', 'school', 'current_class_section',
            'current_teacher'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'aadhaar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_or_guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'known_earlier_disease': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'current_class_section': forms.TextInput(attrs={'class': 'form-control'}),
            'current_teacher': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = [
            'screen_date', 'class_section', 'school', 'weight', 'height', 'muac',
            'vision_both', 'vison_left', 'vison_right',
            
        ]
        widgets = {
            'screen_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'class_section': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'muac': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'vision_both': forms.TextInput(attrs={'class': 'form-control'}),
            'vison_left': forms.NumberInput(attrs={'class': 'form-control'}),
            'vison_right': forms.NumberInput(attrs={'class': 'form-control'}),
            'vision_problem': forms.Textarea(attrs={'class': 'form-control'}),
            'deworming': forms.TextInput(attrs={'class': 'form-control'}),
            'vaccination': forms.TextInput(attrs={'class': 'form-control'}),
            'covid': forms.TextInput(attrs={'class': 'form-control'}),
            'tea_garden': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'age_screening': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from core.models import ScreeningCheck

class ScreeningCheckForm(forms.ModelForm):
    class Meta:
        model = ScreeningCheck
        exclude = ['screening']  # linked automatically in the view
        widgets = {
            # Nutritional / medical conditions
            'B1_severe_anemia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B2_vitA_deficiency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B3_vitD_deficiency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B4_goitre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B5_oedema': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Other medical conditions
            'C1_convulsive_dis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C2_otitis_media': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C3_dental_condition': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C4_skin_condition': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C5_rheumatic_heart_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C6_others_TB_asthma': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Development / learning difficulties
            'D1_difficulty_seeing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D2_delay_in_walking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D3_stiffness_floppiness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D5_reading_writing_calculatory_difficulty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D6_speaking_difficulty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D7_hearing_problems': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D8_learning_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D9_attention_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Other observations
            'E3_depression_sleep': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E4_menarke': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E5_regularity_period_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E6_UTI_STI': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E7_discharge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E8_menstrual_pain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
