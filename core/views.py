
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


from django.shortcuts import render, get_object_or_404
from .models import Student, School, Screening, ScreeningCheck
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ScreeningForm, ScreeningCheckForm
from .models import Student

from datetime import date
from core.utils.processor import calculate_age_in_months


from core.models import School, Student, Screening
from datetime import datetime

from .models import Student, Screening, School
from django.db.models import Max
from django.db.models import Max
from datetime import date


# core/views.py


from django.shortcuts import render, get_object_or_404
from core.models import Screening
from django.shortcuts import render, get_object_or_404

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

from django.shortcuts import render, get_object_or_404
from .models import Screening, ScreeningCheck, School
from django.shortcuts import render, get_object_or_404
from .models import Student, School, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm

def screening_summary(request):
    schools = School.objects.all()
    students = Student.objects.none()
    selected_school_id = request.GET.get('school')
    selected_student_id = request.GET.get('student')

    selected_school = None
    student = None
    screenings = []
    checklist_groups = {}

    if selected_school_id:
        selected_school = get_object_or_404(School, id=selected_school_id)
        students = Student.objects.filter(school=selected_school)

    if selected_student_id:
        student = get_object_or_404(Student, id=selected_student_id)
        screenings = Screening.objects.filter(student=student).order_by('-screen_date')

        checklist_groups = {
            "Preventive Care": ["deworming", "vaccination"],
            "Nutritional / Medical Conditions": [
                "B1_severe_anemia", "B2_vitA_deficiency", "B3_vitD_deficiency",
                "B4_goitre", "B5_oedema"
            ],
            "Other Medical Conditions": [
                "C1_convulsive_dis", "C2_otitis_media", "C3_dental_condition",
                "C4_skin_condition", "C5_rheumatic_heart_disease", "C6_others_TB_asthma"
            ],
            "Development / Learning": [
                "D1_difficulty_seeing", "D2_delay_in_walking", "D3_stiffness_floppiness",
                "D5_reading_writing_calculatory_difficulty", "D6_speaking_difficulty",
                "D7_hearing_problems", "D8_learning_difficulties", "D9_attention_difficulties"
            ],
            "Other Observations": [
                "E3_depression_sleep", "E4_menarke", "E5_regularity_period_difficulties",
                "E6_UTI_STI", "E7_discharge", "E8_menstrual_pain", "E9_remarks"
            ]
        }

        for s in screenings:
            try:
                checklist = ScreeningCheck.objects.get(screening=s)
                # Convert ScreeningCheck object to dict safely
                s.checklist_dict = {field: getattr(checklist, field, False) for group in checklist_groups.values() for field in group}
            except ScreeningCheck.DoesNotExist:
                s.checklist_dict = None

    context = {
        "schools": schools,
        "students": students,
        "selected_school_id": int(selected_school_id) if selected_school_id else None,
        "selected_student_id": int(selected_student_id) if selected_student_id else None,
        "student": student,
        "screenings": screenings,
        "checklist_groups": checklist_groups,
    }

    return render(request, "core/screening_summary.html", context)

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
