
from core.utils.processor import bmi_category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, School,LegacyStudent
from .forms import StudentForm, ScreeningForm, SchoolForm
from django.http import JsonResponse
from core.legacy_helpers import get_all_students, search_students
from core.utils.processor import calculate_bmi, bmi_category, muac_category, calculate_age_in_months
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, School, Screening, ScreeningCheck
from .forms import ScreeningForm, ScreeningCheckForm
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, Screening
from .forms import ScreeningForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ScreeningForm, ScreeningCheckForm
from .models import Student

from datetime import date
from core.utils.processor import calculate_age_in_months
from core.utils.processor import calculate_age_in_months
from core.models import School
from django.shortcuts import render
from core.models import School, Student, Screening
from datetime import datetime

from django.shortcuts import render
from core.models import School, Screening
from core.utils.processor import calculate_age_in_months
# core/views.py
from django.shortcuts import render, get_object_or_404
from .models import Screening
from django.shortcuts import render, get_object_or_404
from core.models import Screening
from django.shortcuts import render, get_object_or_404
from .models import Screening
from django.contrib import messages

def legacy_students_view(request):
    students = LegacyStudent.objects.all()[:50]  # read only
    return render(request, 'core/legacy_students.html', {'students': students})

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('screened_students')  # redirect back to the student list
    else:
        form = StudentForm()

    return render(request, 'core/student_create.html', {'form': form})



def screening_detail(request, screening_id):
    # Get the Screening object
    screening = get_object_or_404(Screening, id=screening_id)

    # Prepare checklist fields grouped
    checklist_groups = {
        "Preventive Care": [
            ("deworming", "Deworming"),
            ("vaccination", "Vaccination")
        ],
        "Nutritional / Medical Conditions": [
            ("B1_severe_anemia", "Severe Anemia"),
            ("B2_vitA_deficiency", "Vitamin A Deficiency"),
            ("B3_vitD_deficiency", "Vitamin D Deficiency"),
            ("B4_goitre", "Goitre"),
            ("B5_oedema", "Oedema")
        ],
        "Other Medical Conditions": [
            ("C1_convulsive_dis", "Convulsive Disorders"),
            ("C2_otitis_media", "Otitis Media"),
            ("C3_dental_condition", "Dental Condition"),
            ("C4_skin_condition", "Skin Condition"),
            ("C5_rheumatic_heart_disease", "Rheumatic Heart Disease"),
            ("C6_others_TB_asthma", "Others (TB / Asthma)")
        ],
        "Development / Learning Difficulties": [
            ("D1_difficulty_seeing", "Difficulty Seeing"),
            ("D2_delay_in_walking", "Delay in Walking"),
            ("D3_stiffness_floppiness", "Stiffness / Floppiness"),
            ("D5_reading_writing_calculatory_difficulty", "Reading/Writing/Calculatory Difficulty"),
            ("D6_speaking_difficulty", "Speaking Difficulty"),
            ("D7_hearing_problems", "Hearing Problems"),
            ("D8_learning_difficulties", "Learning Difficulties"),
            ("D9_attention_difficulties", "Attention Difficulties")
        ],
        "Other Observations": [
            ("E3_depression_sleep", "Depression / Sleep Issues"),
            ("E4_menarke", "Menarke"),
            ("E5_regularity_period_difficulties", "Period Regularity Difficulties"),
            ("E6_UTI_STI", "UTI / STI"),
            ("E7_discharge", "Discharge"),
            ("E8_menstrual_pain", "Menstrual Pain")
        ]
    }

    # Optional: if checklist exists, convert to dict for easy access in template
    checklist_data = {}
    if screening.checklist:
        # Iterate over all fields in checklist
        for group_fields in checklist_groups.values():
            for field_name, _ in group_fields:
                checklist_data[field_name] = getattr(screening.checklist, field_name, False)
        # Add remarks if present
        checklist_data["E9_remarks"] = getattr(screening.checklist, "E9_remarks", "")

    context = {
        "screening": screening,
        "checklist_groups": checklist_groups,
        "screening_checklist": checklist_data
    }

    return render(request, "core/screening_detail.html", context)

from django.shortcuts import render
from .models import Student, Screening, School
from django.db.models import Max
from django.db.models import Max
from datetime import date

def screened_students(request):
    students = Student.objects.all().order_by('name')
    schools = School.objects.all()
    
    # Filter by school if requested
    selected_school_id = request.GET.get("school")
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)

    # Filter by year if requested
    selected_year = request.GET.get("year")
    if selected_year:
        students = students.filter(screenings__screen_date__year=selected_year).distinct()


    students_data = []
    for student in students:
        last_screening = Screening.objects.filter(student=student).order_by('-screen_date').first()
        age_in_months = None
        if last_screening and student.date_of_birth and last_screening.screen_date:
            age_in_months = (last_screening.screen_date.year - student.date_of_birth.year) * 12 + \
                            (last_screening.screen_date.month - student.date_of_birth.month)
        students_data.append({
            'student': student,
            'last_screening': last_screening,
            'age_in_months': age_in_months,
        })

    # For the filter dropdowns
    years = Screening.objects.dates('screen_date', 'year', order='DESC')
    
    context = {
        'students_data': students_data,
        'schools': schools,
        'selected_school_id': int(selected_school_id) if selected_school_id else None,
        'years': [y.year for y in years],
        'selected_year': int(selected_year) if selected_year else None,
    }
    return render(request, "core/screened_students.html", context)



def calculate_age_in_months(dob, screen_date):
    """Helper function to calculate age in months."""
    return (screen_date.year - dob.year) * 12 + (screen_date.month - dob.month)

def add_screening(request):
    students = Student.objects.all().order_by('name')
    schools = School.objects.all()

    selected_student_id = request.POST.get("student") or request.GET.get("student")
    student = None
    age_in_months = None
    initial_data = {}

    if selected_student_id:
        student = get_object_or_404(Student, id=selected_student_id)
        initial_data['school'] = student.school.id if student.school else None

        # calculate age if screening date is provided
        screen_date_str = request.POST.get("screen_date") or request.GET.get("screen_date")
        if student.date_of_birth and screen_date_str:
            screen_date = datetime.strptime(screen_date_str, "%Y-%m-%d").date()
            age_in_months = calculate_age_in_months(student.date_of_birth, screen_date)

    if request.method == "POST":
        screening_form = ScreeningForm(request.POST, initial=initial_data)
        screening_check_form = ScreeningCheckForm(request.POST)
        if screening_form.is_valid() and screening_check_form.is_valid():
            # Save Screening
            screening = screening_form.save(commit=False)
            screening.student = student
            screening.calculate_metrics()  # if this is a custom method
            screening.save()

            # Save ScreeningCheck
            check = screening_check_form.save(commit=False)
            check.screening = screening   # link checklist to the screening
            check.save()

            messages.success(request, f"Screening for {student.name} saved successfully!")
            return redirect("screening_list")
    else:
        screening_form = ScreeningForm(initial=initial_data)
        screening_check_form = ScreeningCheckForm()

    return render(request, "core/screening_list.html", {
        "students": students,
        "schools": schools,
        "screening_form": screening_form,
        "screening_check_form": screening_check_form,
        "age_in_months": age_in_months,
    })

def ajax_student_search(request):
    q = request.GET.get('q', '')
    school_id = request.GET.get('school')
    students = search_students(query=q, school_id=school_id)

    results = [
        {
            'id': s.id,
            'name': s.name,
            'class_section': s.class_section or '',
            'school_name': s.school_name or ''
        }
        for s in students
    ]
    return JsonResponse({'results': results})

def dashboard_view(request):
    return render(request, "core/dashboard.html")

# -------------------------------
# Student Views
# -------------------------------
def student_list(request):
    return render(request, 'core/screened_students.html', {})


def student_detail(request, pk):
    return render(request, 'core/student_detail.html', {})

def student_update(request, pk):
    return render(request, 'core/student_form.html', {})

def student_delete(request, pk):
    return render(request, 'core/student_confirm_delete.html', {})

# -------------------------------
# Screening Views
# -------------------------------
def screening_list(request):
    return render(request, 'core/screening_list.html', {})

def screening_create(request):
    return render(request, 'core/screening_form.html', {})

def screening_detail(request, pk):
    return render(request, 'core/screening_detail.html', {})

def screening_update(request, pk):
    return render(request, 'core/screening_form.html', {})

def screening_delete(request, pk):
    return render(request, 'core/screening_confirm_delete.html', {})

# -------------------------------
# School Views
# -------------------------------
def school_list(request):
    return render(request, 'core/school_list.html', {})

def school_create(request):
    return render(request, 'core/school_form.html', {})

# -------------------------------
# Reports & Statistics
# -------------------------------
def report_summary(request):
    return render(request, 'core/report_summary.html', {})

def statistics(request):
    return render(request, 'core/statistics.html', {})
