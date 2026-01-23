from django import forms
from .models import Student, Screening, School, ScreeningCheck
from django import forms

# -------------------------------
# Student Form
# -------------------------------
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
            'name', 'date_of_birth', 'gender',
            'father_or_guardian_name', 'mother_name', 'contact_number',
            'address',
            'known_earlier_disease', 'school'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            'father_or_guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
           
            
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'known_earlier_disease': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
           
            
        }


# -------------------------------
# Screening Form
# -------------------------------


vision_list = [
    "3/30", "3/24", "3/19", "3/15", "3/12", "3/9.5", "3/7.5", "3/6", "3/4.8",
    "3/3.8", "3/3", "3/2.4", "3/1.9", "3/1.5", "3/1.2", "Not able"
]
VISION_CHOICES = [("", "-- Select Vision --")] + [(v, v) for v in vision_list]


VISION_PROBLEM_CHOICES = [
    ('N/A', 'N/A'),
    ('Yes', 'Yes'),
    ('No', 'No'),
]

from django import forms
from django.utils import timezone
from .models import Screening

class ScreeningForm(forms.ModelForm):

    vision_left = forms.ChoiceField(
        choices=VISION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    vision_right = forms.ChoiceField(
        choices=VISION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    vision_problem = forms.ChoiceField(
        choices=VISION_PROBLEM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select fw-bold'})
    )

    class Meta:
        model = Screening
        fields = [
            'screen_date',
            'class_section',
            'age_screening',
            'weight',
            'height',
            'muac',
            'vision_left',
            'vision_right',
            'vision_problem',
        ]
        widgets = {
            'screen_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'class_section': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'muac': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'age_screening': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'background-color:#e9ecef;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ⛔ Block future dates instantly in date picker
        self.fields['screen_date'].widget.attrs['max'] = (
            timezone.localdate().isoformat()
        )
# -------------------------------
# Screening Check Form
# -------------------------------
class ScreeningCheckForm(forms.ModelForm):
    CHOICES = [
        ('Unknown', 'Unknown'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    deworming = forms.ChoiceField(
        choices=CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    vaccination = forms.ChoiceField(
        choices=CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ScreeningCheck
        exclude = ['screening']
        widgets = {
            # -------- Nutritional Conditions --------
            'B1_severe_anemia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B2_vitA_deficiency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B3_vitD_deficiency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B4_goitre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'B5_oedema': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # -------- Medical Conditions --------
            'C1_convulsive_dis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C2_otitis_media': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C3_dental_condition': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C4_skin_condition': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C5_rheumatic_heart_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'C6_others_TB_asthma': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # -------- Developmental / Learning --------
            'D1_difficulty_seeing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D2_delay_in_walking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D3_stiffness_floppiness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D5_reading_writing_calculatory_difficulty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D6_speaking_difficulty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D7_hearing_problems': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D8_learning_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'D9_attention_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # -------- Other Observations --------
            'E3_depression_sleep': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E4_menarke': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E5_regularity_period_difficulties': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E6_UTI_STI': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E7_discharge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E8_menstrual_pain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'E9_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter doctor’s remarks...'
            }),
        }

        labels = {
            # -------- Nutritional --------
            'B1_severe_anemia': 'B1: Severe Anemia',
            'B2_vitA_deficiency': 'B2: Vitamin A Deficiency',
            'B3_vitD_deficiency': 'B3: Vitamin D Deficiency',
            'B4_goitre': 'B4: Goitre',
            'B5_oedema': 'B5: Oedema',

            # -------- Medical --------
            'C1_convulsive_dis': 'C1: Convulsive Disorders',
            'C2_otitis_media': 'C2: Otitis Media',
            'C3_dental_condition': 'C3: Dental Condition',
            'C4_skin_condition': 'C4: Skin Condition',
            'C5_rheumatic_heart_disease': 'C5: Rheumatic Heart Disease',
            'C6_others_TB_asthma': 'C6: Respiratory Problem (Suggestive of Asthma/TB)',

            # -------- Developmental --------
            'D1_difficulty_seeing': 'D1: Vision problem (night vision or day vision),',
            'D2_delay_in_walking': 'D2: Delay in walking',
            'D3_stiffness_floppiness': 'D3: Stiffness / Floppiness/reduced strengthin in arms/legs',
            'D5_reading_writing_calculatory_difficulty': 'D5: Reading / writing / calculatory difficulties',
            'D6_speaking_difficulty': 'D6: Difficulty in speaking',
            'D7_hearing_problems': 'D7: Difficulty in hearing',
            'D8_learning_difficulties': 'D8: Learning difficulties',
            'D9_attention_difficulties': 'D9: Attention difficulties',

            # -------- Other --------
            'E3_depression_sleep': 'E3: Feeling unduly tired/depressed',
            'E4_menarke': 'E4: Menstrual Cycle started?',
            'E5_regularity_period_difficulties': 'E5: Irregular periods?',
            'E6_UTI_STI': 'E6: Pain/burning while urinating?',
            'E7_discharge': 'E7: Discharge/foul smell from genito/urinary area?',
            'E8_menstrual_pain': 'E8: Menstrual Pain',
            
            'E9_remarks': 'Doctor’s Remarks',
        }

# -------------------------------
# School Form
# -------------------------------
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
