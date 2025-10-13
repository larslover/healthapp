from django import forms
from .models import Student, Screening, School

from django import forms
from core.models import Student, Screening

# core/forms.py
from django import forms
from .models import Student, Screening, School

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'date_of_birth', 'gender', 'roll_no', 'aadhaar_no',
            'father_or_guardian_name', 'mother_name', 'contact_number',
            'address', 'email', 'last_school_name', 'place_of_birth', 'known_earlier_disease'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'aadhaar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'father_or_guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'known_earlier_disease': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = [
            'screen_date', 'class_section', 'school', 'weight', 'height', 'bmi', 'bmi_category',
            'muac', 'muac_sam', 'vision_both', 'vison_left', 'vison_right', 'vision_problem',
            'age_in_month', 'deworming', 'vaccination', 'covid', 'tea_garden', 'status', 'age_screening'
        ]
        widgets = {
            'screen_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'class_section': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'step': '0.1', 'readonly': True, 'class': 'form-control'}),
            'bmi_category': forms.TextInput(attrs={'class': 'form-control'}),
            'muac': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'muac_sam': forms.TextInput(attrs={'class': 'form-control'}),
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
        }



class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
