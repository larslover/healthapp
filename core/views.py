
from core.utils.processor import bmi_category
from .forms import StudentForm
from django.db.models.functions import ExtractYear
from .models import Student, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from .models import Screening, School,LegacyStudent
from django.http import JsonResponse
from core.legacy_helpers import get_all_students, search_students
from core.utils.processor import calculate_bmi, bmi_category, muac_category, calculate_age_in_months
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, School, Screening, ScreeningCheck
from .forms import ScreeningForm, ScreeningCheckForm
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
import json
from .models import School, Student, Screening, ScreeningCheck
from .utils.processor import muac_category  # assuming you already have this function
from datetime import date
from core.utils.processor import calculate_age_in_months
from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from core.utils.processor import weight_height_category

from core.utils.weight_height_male_thresholds import weight_height_male_thresholds
from core.utils.weight_height_female_thresholds import weight_height_female_thresholds
from core.utils.bmi_thresholds_male import bmi_thresholds_male
from core.utils.bmi_thresholds_female import bmi_thresholds_female
import pandas as pd
from django.utils.safestring import mark_safe
import json
from pathlib import Path



def get_who_reference_curves(chart_mode, gender):
    """
    Returns WHO reference curves (−3SD to +3SD) for BMI-for-Age or Weight-for-Height.
    """
    if chart_mode == "bmi":
        data = (
             bmi_thresholds_male if gender == "male" else bmi_thresholds_female
        )
    else:  # weight-for-height
        data = (
            weight_height_male_thresholds
            if gender == "male"
            else weight_height_female_thresholds
        )

    sd_labels = ["−3SD", "−2SD", "−1SD", "Median", "+1SD", "+2SD", "+3SD"]

    # Convert keys to numbers and sort safely
    x_values = sorted(float(k) for k in data.keys())
    x_str_values = [str(x).rstrip("0").rstrip(".") if "." in str(x) else str(x) for x in x_values]

    curves = {}
    for i, label in enumerate(sd_labels):
        y_values = []
        for x_str in x_str_values:
            try:
                y_values.append(data[x_str][i])
            except KeyError:
                # skip missing points instead of crashing
                continue
        curves[label] = {"x": x_values[:len(y_values)], "y": y_values}

    return curves

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
# core/views.py (snippet)
import json
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from .models import School, Student, Screening, ScreeningCheck
from .utils.processor import muac_category, weight_height_category, bmi_category, calculate_age_in_months

# -------------------------
# Module-level helper funcs
# -------------------------

def get_checklist_for_screening(screening, checklist_groups):
    """Return a dict of checklist boolean fields for the screening or None."""
    try:
        checklist = ScreeningCheck.objects.get(screening=screening)
        return {field: getattr(checklist, field, False)
                for group in checklist_groups.values() for field in group}
    except ScreeningCheck.DoesNotExist:
        return None


def muac_category_for(screening, student):
    """Return MUAC category only for 6–60 months, else 'N/A'."""
    if not student.date_of_birth or screening.muac is None:
        return "N/A"
    age_m = calculate_age_in_months(student.date_of_birth, screening.screen_date)
    if 6 <= age_m <= 60:
        return muac_category(screening.muac, age_m)
    return "N/A"


def determine_growth_for_screening(screening, student):
    """
    Decide growth indicator and category for a single screening.
    Returns tuple: (indicator_label, category_label, chart_value_or_none, age_months)
    chart_value_or_none is the numeric value to plot (BMI or computed Wt/H BMI-equivalent),
    or None when we shouldn't plot this screening.
    """
    if not student or not student.date_of_birth:
        return "N/A", "N/A", None, 0

    age_m = calculate_age_in_months(student.date_of_birth, screening.screen_date) or 0

    # Ensure we have numeric weight/height/bmi as required
    has_w_h = screening.weight is not None and screening.height is not None
    has_bmi = screening.bmi is not None

    gender = (student.gender or "").lower()

    # Weight-for-Height window: 24–60 months
    if 24 <= age_m <= 60 and has_w_h and gender in ("male", "female"):
        cat = weight_height_category(screening.weight, screening.height, age_m, gender)
        # compute the BMI-equivalent value for plotting (weight / height^2) so the axis is comparable
        plot_val = screening.weight / ((screening.height / 100) ** 2) if screening.height != 0 else None
        return "Weight-for-Height", cat, round(plot_val, 2) if plot_val is not None else None, age_m

    # BMI-for-age: > 60 months
    if age_m > 60 and has_bmi and gender in ("male", "female"):
        cat = bmi_category(screening.bmi, age_m, gender)
        return "BMI-for-Age", cat, round(screening.bmi, 2), age_m

    # Too young / insufficient data
    return "Too young / Insufficient data", "N/A", None, age_m


def build_chart_data_for_student(screenings, student):
    """
    Decide chart_mode based on latest screening age:
      - If any screening has age > 60 months => 'bmi' mode
      - else => 'wfh' (weight-for-height) mode

    Returns:
      (chart_mode, labels_json, values_json, refs_json, who_curves_json)
    """
    if not screenings:
        return "none", mark_safe("[]"), mark_safe("[]"), mark_safe("[]"), mark_safe("{}")

    # Compute ages for each screening
    ages = [calculate_age_in_months(student.date_of_birth, s.screen_date) or 0 for s in screenings]
    latest_age = max(ages) if ages else 0
    chart_mode = "bmi" if latest_age > 60 else "wfh"

    labels, values, refs = [], [], []

    for s in screenings:
        indicator, category, plot_value, age_m = determine_growth_for_screening(s, student)

        if plot_value is None:
            continue

        if chart_mode == "bmi" and indicator == "BMI-for-Age":
            labels.append(age_m)  # x-axis = age (months)
            values.append(plot_value)
            refs.append(category)
        elif chart_mode == "wfh" and indicator == "Weight-for-Height":
            labels.append(s.height)  # x-axis = height (cm)
            values.append(plot_value)
            refs.append(category)

    # Get WHO reference curves for current chart type + gender
    gender = "male" if student.gender.lower().startswith("m") else "female"
    who_curves = get_who_reference_curves(chart_mode, gender)

    # Format background SD lines for plotting (like BMI chart)
    background_lines = []
    for label, curve in who_curves.items():
        background_lines.append({
            "label": label,  # e.g. "-2SD"
            "x": curve["x"],
            "y": curve["y"],
        })

    combined_data = {
        "background": background_lines,  # seven WHO reference lines
        "student": {
            "x": labels,
            "y": values,
            "categories": refs,
        },
    }

    return (
        chart_mode,
        mark_safe(json.dumps(labels)),
        mark_safe(json.dumps(values)),
        mark_safe(json.dumps(refs)),
        mark_safe(json.dumps(combined_data)),  # contains both student + reference lines
    )

# -------------------------
# The view
# -------------------------

@login_required(login_url='login')
def screening_summary(request):
    schools = School.objects.all()
    students = Student.objects.none()
    selected_school_id = request.GET.get('school')
    selected_student_id = request.GET.get('student')

    student = None
    screenings = []
    checklist_groups = {}

    # default empty chart data
    chart_mode = "none"
    chart_labels = mark_safe("[]")
    chart_values = mark_safe("[]")
    chart_reference = mark_safe("[]")
    chart_who_curves = mark_safe("[]")

    if selected_school_id:
        students = Student.objects.filter(school_id=selected_school_id)

    if selected_student_id:
        student = get_object_or_404(Student, id=selected_student_id)
        screenings = list(Screening.objects.filter(student=student).order_by('screen_date'))

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

        # annotate screenings with checklist and MUAC category, and keep them for template rendering
        for s in screenings:
            s.checklist_dict = get_checklist_for_screening(s, checklist_groups)
            s.muac_category = muac_category_for(s, student)

            # also fill growth indicator/category/age for template use
            indicator, category, plot_value, age_m = determine_growth_for_screening(s, student)
            s.growth_indicator = indicator
            s.growth_category = category
            s.age_in_months = age_m

        # build chart data consistently
        chart_mode, chart_labels, chart_values, chart_reference, chart_who_curves = build_chart_data_for_student(screenings, student)


    context = {
    "schools": schools,
    "students": students,
    "selected_school_id": int(selected_school_id) if selected_school_id else None,
    "selected_student_id": int(selected_student_id) if selected_student_id else None,
    "student": student,
    "screenings": screenings,
    "checklist_groups": checklist_groups,
    "chart_mode": chart_mode,
    "chart_labels": chart_labels,
    "chart_values": chart_values,
    "chart_reference": chart_reference,
    "chart_who_curves": chart_who_curves,  # ← add this line
    }


    return render(request, "core/screening_summary.html", context)

from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student, Screening, ScreeningCheck, School
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Student, School, Screening, ScreeningCheck
from core.forms import StudentForm, ScreeningForm, ScreeningCheckForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def screened_students(request):
    selected_year = request.GET.get("year")
    selected_school_id = request.GET.get("school")
    selected_student_id = request.GET.get("selected_student")

    # === Filter base queryset ===
    students = Student.objects.all()
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)

    # === Build student data for listing ===
    students_data = []
    for student in students:
        screenings = Screening.objects.filter(student=student)
        if selected_year:
            screenings = screenings.filter(screen_date__year=selected_year)

        formatted_age = "—"
        if student.date_of_birth:
            formatted_age = format_age(student.date_of_birth, date.today())

        students_data.append({
            "student": student,
            "screenings": screenings,
            "age_display": formatted_age,
        })

    # === Handle selected student ===
    student_form = screening_form = checklist_form = None
    selected_student = None

    if selected_student_id:
        selected_student = get_object_or_404(Student, pk=selected_student_id)
        screening = Screening.objects.filter(student=selected_student).last()
        if not screening:
            screening = Screening.objects.create(student=selected_student)
        checklist, _ = ScreeningCheck.objects.get_or_create(screening=screening)

        if request.method == "POST":
            print("🧾 POST DATA:", request.POST)
            student_form = StudentForm(request.POST, instance=selected_student)
            screening_form = ScreeningForm(request.POST, instance=screening)
            checklist_form = ScreeningCheckForm(request.POST, instance=checklist)

            if student_form.is_valid() and screening_form.is_valid() and checklist_form.is_valid():
                student = student_form.save(commit=False)

                # ✅ Robust school handling
                school_id = request.POST.get("school")
                if school_id and school_id.strip():
                    try:
                        student.school = School.objects.get(pk=int(school_id))
                        print(f"✅ Assigned school: {student.school}")
                    except (ValueError, School.DoesNotExist):
                        print("⚠️ Invalid school ID submitted")
                elif school_id == "":
                    # Explicitly cleared
                    student.school = None
                # else: keep existing if not included

                student.save()
                screening_form.save()
                checklist_form.save()

                print(f"✅ Saved student: {student.name} | Final school: {student.school}")
                return redirect("screened_students")

        else:
            student_form = StudentForm(instance=selected_student)
            screening_form = ScreeningForm(instance=screening)
            checklist_form = ScreeningCheckForm(instance=checklist)
            print(f"🧩 Editing {selected_student.name} | Current school: {selected_student.school}")

    # === Years dropdown ===
    years_qs = Screening.objects.dates("screen_date", "year", order="DESC")
    years = [d.year for d in years_qs]

    # === Render ===
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


def format_age(dob, current_date):
    """Return formatted string like '5y 3m'."""
    months = calculate_age_in_months(dob, current_date)
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
# ------------------------------

# -------------------------------
# Screening Views
# -------------------------------






