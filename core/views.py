
from core.utils.processor import bmi_category
from django.shortcuts import get_object_or_404, redirect, render
from .models import Screening, ScreeningCheck
from .forms import ScreeningForm, ScreeningCheckForm  # We'll create these forms
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student
from .forms import StudentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import ExtractYear
from .models import Student, Screening, ScreeningCheck, School
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm

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

from django.utils.safestring import mark_safe
import json
from .models import School, Student, Screening, ScreeningCheck
from .utils.processor import muac_category  # assuming you already have this function
from .models import Student, School, Screening, ScreeningCheck
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ScreeningForm, ScreeningCheckForm
from .models import Student
from datetime import date
from core.utils.processor import calculate_age_in_months
from core.models import School, Student, Screening
from datetime import datetime

from django.db.models import Max

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.utils.processor import weight_height_category


def login_view(request):
    if request.user.is_authenticated:
        return redirect('screened_students')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('screened_students')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html')

def legacy_students_view(request):
    students = LegacyStudent.objects.all()[:50]  # read only
    return render(request, 'core/legacy_students.html', {'students': students})

@login_required(login_url='login')
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('screened_students')  # redirect back to the student list
    else:
        form = StudentForm()

    return render(request, 'core/student_create.html', {'form': form})

@login_required(login_url='login')
def screening_summary(request):
    schools = School.objects.all()
    students = Student.objects.none()
    selected_school_id = request.GET.get('school')
    selected_student_id = request.GET.get('student')

    student = None
    screenings = []
    checklist_groups = {}

    chart_labels = []
    chart_bmi = []
    chart_weight = []
    chart_height = []
    chart_muac = []
    chart_age = []

    if selected_school_id:
        students = Student.objects.filter(school_id=selected_school_id)

    if selected_student_id:
        student = get_object_or_404(Student, id=selected_student_id)
        screenings = Screening.objects.filter(student=student).order_by('screen_date')

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
            # Checklist data
            try:
                checklist = ScreeningCheck.objects.get(screening=s)
                s.checklist_dict = {field: getattr(checklist, field, False) 
                                    for group in checklist_groups.values() for field in group}
            except ScreeningCheck.DoesNotExist:
                s.checklist_dict = None

            # Age in months for MUAC/BMI logic
            if student.date_of_birth:
                months = (s.screen_date.year - student.date_of_birth.year) * 12 + (s.screen_date.month - student.date_of_birth.month)
                if s.screen_date.day < student.date_of_birth.day:
                    months -= 1
                s.age_in_months = months
            else:
                s.age_in_months = 0

                    # MUAC category (only for 6–60 months)
            if 6 <= s.age_in_months <= 60 and s.muac is not None:
                s.muac_category = muac_category(s.muac, s.age_in_months)
            else:
                s.muac_category = "N/A"

            # Weight-for-Height category (for 24–60 months)
            if s.weight and s.height and student.gender:
                s.weight_for_height = weight_height_category(
                    s.weight,
                    s.height,
                    s.age_in_months,
                    student.gender
                )
            else:
                s.weight_for_height = "N/A"
            # Chart data
            chart_labels.append(s.screen_date.strftime("%Y-%m-%d"))
            chart_bmi.append(s.bmi if s.bmi is not None else 0)
            chart_weight.append(s.weight if s.weight is not None else 0)
            chart_height.append(s.height if s.height is not None else 0)
            chart_muac.append(s.muac if s.muac is not None else 0)

            # Age in decimal years for chart
            if student.date_of_birth:
                years = s.screen_date.year - student.date_of_birth.year
                months = s.screen_date.month - student.date_of_birth.month
                if s.screen_date.day < student.date_of_birth.day:
                    months -= 1
                if months < 0:
                    years -= 1
                    months += 12
                chart_age.append(round(years + months/12, 2))
            else:
                chart_age.append(0)

        # Convert to JSON for JS charts
        chart_labels = mark_safe(json.dumps(chart_labels))
        chart_bmi = mark_safe(json.dumps(chart_bmi))
        chart_weight = mark_safe(json.dumps(chart_weight))
        chart_height = mark_safe(json.dumps(chart_height))
        chart_muac = mark_safe(json.dumps(chart_muac))
        chart_age = mark_safe(json.dumps(chart_age))
    else:
        chart_labels = chart_bmi = chart_weight = chart_height = chart_muac = chart_age = mark_safe("[]")

    context = {
        "schools": schools,
        "students": students,
        "selected_school_id": int(selected_school_id) if selected_school_id else None,
        "selected_student_id": int(selected_student_id) if selected_student_id else None,
        "student": student,
        "screenings": screenings,
        "checklist_groups": checklist_groups,
        "chart_labels": chart_labels,
        "chart_bmi": chart_bmi,
        "chart_weight": chart_weight,
        "chart_height": chart_height,
        "chart_muac": chart_muac,
        "chart_age": chart_age,
    }

    return render(request, "core/screening_summary.html", context)


@login_required(login_url='login')
def screened_students(request):
    # Filters
    selected_year = request.GET.get("year")
    selected_school_id = request.GET.get("school")
    selected_student_id = request.GET.get("selected_student")

    # Base queryset
    students = Student.objects.all()
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)

    # Prepare student data for table
    students_data = []
    for student in students:
        screenings = Screening.objects.filter(student=student)
        if selected_year:
            screenings = screenings.filter(screen_date__year=selected_year)

        latest_screening = screenings.last() if screenings.exists() else None

        # Calculate age in months at latest screening
        # Calculate and format age
        age_in_months = None
        formatted_age = "—"
        if latest_screening and student.date_of_birth:
            age_in_months = calculate_age_in_months(student.date_of_birth, latest_screening.screen_date)
            formatted_age = format_age(student.date_of_birth, latest_screening.screen_date)

        students_data.append({
            "student": student,
            "screenings": screenings,
            "age_in_months": age_in_months,
            "age_display": formatted_age,  # 👈 new field
        })


    # Inline edit forms for selected student
    student_form = screening_form = checklist_form = None
    selected_student = None
    if selected_student_id:
        selected_student = get_object_or_404(Student, pk=selected_student_id)
        screening = Screening.objects.filter(student=selected_student).last()
        if not screening:
            screening = Screening(student=selected_student)
            screening.save()  # 👈 Save before using in get_or_create

        checklist, _ = ScreeningCheck.objects.get_or_create(screening=screening)


        if request.method == "POST":
            student_form = StudentForm(request.POST, instance=selected_student)
            screening_form = ScreeningForm(request.POST, instance=screening)
            checklist_form = ScreeningCheckForm(request.POST, instance=checklist)
            if student_form.is_valid() and screening_form.is_valid() and checklist_form.is_valid():
                student_form.save()
                screening_form.save()
                checklist_form.save()
                return redirect("screened_students")
        else:
            student_form = StudentForm(instance=selected_student)
            screening_form = ScreeningForm(instance=screening)
            checklist_form = ScreeningCheckForm(instance=checklist)

    # Years for dropdown filter
    years_qs = Screening.objects.dates("screen_date", "year", order="DESC")
    years = [d.year for d in years_qs]

    context = {
        "students_data": students_data,
        "selected_year": selected_year,
        "selected_school_id": int(selected_school_id) if selected_school_id else None,
        "selected_student": selected_student,
        "student_form": student_form,
        "screening_form": screening_form,
        "checklist_form": checklist_form,
        "schools": School.objects.all(),
        "years": years,
    }
    return render(request, "core/screened_students.html", context)
def calculate_age_in_months(dob, screen_date):
    """Return total months as integer."""
    if not dob or not screen_date:
        return None
    months = (screen_date.year - dob.year) * 12 + (screen_date.month - dob.month)
    if screen_date.day < dob.day:
        months -= 1
    return months

def format_age(dob, screen_date):
    """Return formatted string like '5y 3m'."""
    months = calculate_age_in_months(dob, screen_date)
    if months is None or months < 0:
        return "—"
    years, rem = divmod(months, 12)
    if years and rem:
        return f"{years}y {rem}m"
    elif years:
        return f"{years}y"
    return f"{rem}m"

@login_required(login_url='login')
def add_screening(request):
    students = Student.objects.all().order_by('name')
    schools = School.objects.all()
    selected_student_id = request.POST.get("student") or request.GET.get("student")
    student = None
    age_in_months = None

    if selected_student_id:
        student = get_object_or_404(Student, id=selected_student_id)

        # calculate age if screening date is provided
        screen_date_str = request.POST.get("screen_date") or request.GET.get("screen_date")
        if student.date_of_birth and screen_date_str:
            screen_date = datetime.strptime(screen_date_str, "%Y-%m-%d").date()
            age_in_months = calculate_age_in_months(student.date_of_birth, screen_date)

    if request.method == "POST":
        if not student:
            messages.error(request, "Please select a student first.")
            return redirect("screening_add")

        screening_form = ScreeningForm(request.POST)
        screening_check_form = ScreeningCheckForm(request.POST)

        if screening_form.is_valid() and screening_check_form.is_valid():
            screening = screening_form.save(commit=False)
            screening.student = student
            try:
                screening.calculate_metrics()
            except Exception as e:
                messages.error(request, f"Error calculating metrics: {e}")
                return render(request, "core/screening_list.html", {
                    "students": students,
                    "schools": schools,
                    "screening_form": screening_form,
                    "screening_check_form": screening_check_form,
                    "age_in_months": age_in_months,
                })

            screening.save()

            check = screening_check_form.save(commit=False)
            check.screening = screening
            check.save()

            messages.success(request, f"Screening for {student.name} saved successfully!")
            return redirect("screening_list")
        else:
            # show errors for debugging
            print("Screening Form Errors:", screening_form.errors)
            print("Checklist Form Errors:", screening_check_form.errors)

    else:
        screening_form = ScreeningForm(initial={'school': student.school.id} if student else None)
        screening_check_form = ScreeningCheckForm()

    return render(request, "core/screening_list.html", {
        "students": students,
        "schools": schools,
        "screening_form": screening_form,
        "screening_check_form": screening_check_form,
        "age_in_months": age_in_months,
        "student": student,
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
