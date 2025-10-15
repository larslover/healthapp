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
            'screen_date', 'class_section', 'school', 'weight', 'height', 'bmi', 'bmi_category',
            'muac', 'muac_sam', 'vision_both', 'vison_left', 'vison_right', 'vision_problem',
            'age_in_month', 'deworming', 'vaccination', 'covid', 'tea_garden', 'status', 'age_screening','weight_age', 'length_age', 'weight_height'
        ]
        widgets = {
            'screen_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'class_section': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
           'weight': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control', 'id': 'id_weight'}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control', 'id': 'id_height'}),
            'bmi': forms.NumberInput(attrs={'step': '0.1', 'readonly': True, 'class': 'form-control', 'id': 'id_bmi'}),

            'bmi_category': forms.TextInput(attrs={'readonly': True,
            'class': 'form-control',
        '   id': 'id_bmi_category'    }),
            'muac': forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'form-control',
            'id': 'id_muac'            # make sure JS matches this ID
                    }),
            'muac_sam': forms.TextInput(attrs={
                'readonly': True,          # auto-populated like BMI category
                'class': 'form-control',
                'id': 'id_muac_sam'        # match JS
            }),
            'vision_both': forms.TextInput(attrs={'class': 'form-control'}),
            'vison_left': forms.NumberInput(attrs={'class': 'form-control'}),
            'vison_right': forms.NumberInput(attrs={'class': 'form-control'}),
            'vision_problem': forms.Textarea(attrs={'class': 'form-control'}),
            'age_in_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'deworming': forms.TextInput(attrs={'class': 'form-control'}),
            'vaccination': forms.TextInput(attrs={'class': 'form-control'}),
            'covid': forms.TextInput(attrs={'class': 'form-control'}),
            'tea_garden': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'age_screening': forms.TextInput(attrs={'class': 'form-control'}),
            'weight_age': forms.TextInput(attrs={'class': 'form-control'}),
            'length_age': forms.TextInput(attrs={'class': 'form-control'}),
            'weight_height': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make age_in_month read-only
        if 'age_in_month' in self.fields:
            self.fields['age_in_month'].disabled = True



class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
