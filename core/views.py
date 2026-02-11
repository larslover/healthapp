# Standard library
from datetime import datetime, date
import json
import os
import time
from pathlib import Path
import logging

# Third-party
import pandas as pd
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Max, Prefetch
from django.db.models.functions import ExtractYear
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.contrib.auth import authenticate, login
from django.db.models import Q


# Local apps
from core.models import Student, School, Screening, ScreeningCheck
from core.forms import StudentForm, ScreeningForm, ScreeningCheckForm, CLASS_CHOICES,SchoolForm
from core.services.statistics import get_screening_statistics
from core.utils.processor import (
    calculate_age_in_months,
    bmi_category,
    muac_category,
    weight_height_category,
    calculate_bmi
)
from core.utils.weight_height_male_thresholds import weight_height_male_thresholds
from core.utils.weight_height_female_thresholds import weight_height_female_thresholds
from core.utils.bmi_thresholds_male import bmi_thresholds_male
from core.utils.bmi_thresholds_female import bmi_thresholds_female

# core/views.py
from django.shortcuts import render
from core.models import School, Screening
from core.forms import CLASS_CHOICES
from core.services.statistics import get_screening_statistics
import logging

logger = logging.getLogger(__name__)  # recommended way to log
# core/views.py
from core.services.statistics import get_screening_statistics
from core.models import School
from core.forms import CLASS_CHOICES
from django.shortcuts import render
from core.models import Screening

# core/views.py
from django.shortcuts import render
from core.models import Screening, School
from core.forms import CLASS_CHOICES
from core.services.statistics import get_screening_statistics
from django.http import JsonResponse
from .models import Screening

from django.http import JsonResponse
from .models import Screening
from django.http import JsonResponse
from django.db.models import Q
# core/views.py
from django.http import JsonResponse
from core.models import Screening, ScreeningCheck

def stat_students_ajax(request):
    """
    Return students filtered by selected KPI, school, year, class.
    """
    type_filter = request.GET.get("type") or ""  # KPI field name
    school = request.GET.get("school")
    year = request.GET.get("year")
    selected_class = request.GET.get("student_class") or request.GET.get("class")

    print("AJAX filter values:", type_filter, school, year, selected_class)

    # Base queryset
    screenings = Screening.objects.select_related("student", "school", "checklist")

    if year:
        screenings = screenings.filter(screening_year=year)
    if school:
        screenings = screenings.filter(school_id=school)
    if selected_class:
        screenings = screenings.filter(class_section=selected_class)

    # 🔹 Debug: before KPI filter
    print("Screenings before KPI filter:", screenings.count())

    # Filter by KPI
    if type_filter:
        # These are fields on ScreeningCheck
        checklist_fields = [f.name for f in ScreeningCheck._meta.get_fields()
                            if f.get_internal_type() == "BooleanField"]

        if type_filter in checklist_fields:
            screenings = screenings.filter(
                checklist__isnull=False,
                **{f"checklist__{type_filter}": True}
            )
        # Special cases for Screening fields
        elif type_filter == "vision":
            screenings = screenings.filter(vision_problem=True)
        elif type_filter == "muac":
            screenings = screenings.filter(muac_status="SAM")
        else:
            print("Unknown KPI field:", type_filter)

    # 🔹 Debug: after KPI filter
    print("Screenings after KPI filter:", screenings.count())

    # Build student list
    students = []
    for s in screenings:
        students.append({
            "id": s.student.id,
            "name": s.student.name,
            "class": s.class_section,
            "school": s.school.name if s.school else "",
        })

    return JsonResponse({
        "title": type_filter.replace("_", " ").title() if type_filter else "All Students",
        "students": students
    })

def statistics(request):
    # ---- Selected filters ----
    selected_year = request.GET.get("year")
    selected_school = request.GET.get("school", "")
    selected_class = request.GET.get("class", "")

    # ---- Default year (latest) ----
    if not selected_year:
        selected_year = (
            Screening.objects
            .exclude(screening_year__isnull=True)
            .values_list("screening_year", flat=True)
            .distinct()
            .order_by("-screening_year")
            .first()
        )

    # ---- Fetch statistics ----
    stats = get_screening_statistics(
        screening_year=selected_year,
        school_id=selected_school or None,
        class_section=selected_class or None,
    )

    # ---- Year dropdown ----
    years = (
        Screening.objects
        .exclude(screening_year__isnull=True)
        .values_list("screening_year", flat=True)
        .distinct()
        .order_by("-screening_year")
    )

        # ---- Checklist KPI cards ----
    checklist_stats = [
        {
            "key": field,  # ✅ important for data-type
            "label": field.replace("_", " ").title(),
            "value": count,
            "danger": True,
        }
        for field, count in stats.get("checklist", {}).items()
        if count > 0
    ]

    return render(
        request,
        "core/statistics.html",
        {
            "stats": stats,
            "year": selected_year,
            "years": years,
            "schools": School.objects.all(),
            "class_choices": CLASS_CHOICES,
            "selected_school": selected_school,  # ✅ FIX
            "selected_class": selected_class,
            "checklist_stats": checklist_stats,
        }
    )

def get_classes_for_school(request):
    year = request.GET.get("year")
    school_id = request.GET.get("school")

    if not year:
        return JsonResponse({"classes": []})

    qs = Screening.objects.filter(screening_year=year)
    if school_id:
        qs = qs.filter(school_id=school_id)

    # Get distinct classes, normalize names
    db_classes = (
        qs.values_list("class_section", flat=True)
        .exclude(class_section__isnull=True)
        .exclude(class_section__exact="")
    )
    normalized_classes = sorted({cls.strip().title() for cls in db_classes})

    return JsonResponse({"classes": normalized_classes})

@require_POST
def delete_screening(request, screening_id):
    screening = get_object_or_404(Screening, id=screening_id)
    student_id = screening.student_id
    screening.delete()

    url = reverse("screened_students")
    return redirect(f"{url}?selected_student={student_id}")


@transaction.atomic
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("screened_students")  # change to your list view name

    return redirect("screened_students")


def service_worker(request):
    sw_path = os.path.join('healthapp', 'service-worker.js')
    with open(static(sw_path).replace('/static/', 'healthapp/static/healthapp/'), 'r') as f:
        js = f.read()
    return HttpResponse(js, content_type='application/javascript')


def school_create(request):
    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('screened_students')
    else:
        form = SchoolForm()
    return render(request, 'core/school_form.html', {'form': form})

def growth_reference_api(request):
    try:
        gender = request.GET.get("gender")
        weight = float(request.GET.get("weight"))
        height = float(request.GET.get("height"))
        dob = request.GET.get("dob")
        screen_date = request.GET.get("screen_date")

        if not (dob and screen_date):
            return JsonResponse({"error": "missing dates"}, status=400)

        from datetime import datetime
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        screen_date = datetime.strptime(screen_date, "%Y-%m-%d").date()

        age_months = calculate_age_in_months(dob, screen_date)

        response = {"age_months": age_months}

        # ----------------------------
        # Under 5 years → Weight-for-Height only
        # ----------------------------
        if age_months <= 60:
            wfh_cat = weight_height_category(weight, height, age_months, gender)
            response["weight_for_height"] = wfh_cat
            return JsonResponse(response)

        # ----------------------------
        # Over 5 years → BMI-for-age only
        # ----------------------------
        bmi = calculate_bmi(weight, height)
        bmi_cat = bmi_category(gender, age_months, bmi)

        response["bmi"] = bmi
        response["bmi_category"] = bmi_cat

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_who_reference_curves(chart_mode, gender):
    """
    Returns WHO reference curves (-3SD to +3SD) for BMI-for-age or Weight-for-height.
    Supports both float and string keys in the WHO data files.
    """
    if chart_mode == "bmi":
        from core.utils.bmi_thresholds_male import bmi_thresholds_male as male_data
        from core.utils.bmi_thresholds_female import bmi_thresholds_female as female_data
        data = male_data if gender == "male" else female_data
    elif chart_mode == "wfh":
        from core.utils.weight_height_male_thresholds import weight_height_male_thresholds as male_data
        from core.utils.weight_height_female_thresholds import weight_height_female_thresholds as female_data
        data = male_data if gender == "male" else female_data
    else:
        return {}

    sd_labels = ["-3SD", "-2SD", "-1SD", "Median", "+1SD", "+2SD", "+3SD"]

    try:
        x_values = sorted(float(k) for k in data.keys())
    except Exception:
        x_values = sorted(data.keys())

    curves = {}
    for i, label in enumerate(sd_labels):
        x_list, y_list = [], []
        for x in x_values:
    # Normalize key lookup
            key_str = str(int(x)) if float(x).is_integer() else str(x)
            val = data.get(x) or data.get(key_str)
            if val and i < len(val):
                x_list.append(x)
                y_list.append(val[i])
                curves[label] = {"x": x_list, "y": y_list}

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
        return "Weight-for-Height", cat, round(screening.weight, 2), age_m  # <-- use actual weight


    # BMI-for-age: > 60 months
    if age_m > 60 and has_bmi and gender in ("male", "female"):
        cat = bmi_category(screening.bmi, age_m, gender)
        return "BMI-for-Age", cat, round(screening.bmi, 2), age_m

    # Too young / insufficient data
    return "Too young / Insufficient data", "N/A", None, age_m
def get_who_wfh_curves(gender):
    data = (
        weight_height_female_thresholds
        if gender == "female"
        else weight_height_male_thresholds
    )

    curves = {
        "-3SD": {"x": [], "y": []},
        "-2SD": {"x": [], "y": []},
        "-1SD": {"x": [], "y": []},
        "Median": {"x": [], "y": []},
        "+1SD": {"x": [], "y": []},
        "+2SD": {"x": [], "y": []},
        "+3SD": {"x": [], "y": []},
    }

    for height, values in data.items():
        for i, key in enumerate(curves.keys()):
            curves[key]["x"].append(float(height))
            curves[key]["y"].append(float(values[i]))

    return curves


def build_chart_data_for_student(screenings, student):
    if not screenings:
        empty = mark_safe("[]")
        return empty, empty, empty, empty, empty, empty, empty, empty

    bmi_labels, bmi_values, bmi_categories = [], [], []
    wfh_labels, wfh_values, wfh_categories = [], [], []

    for s in screenings:
        indicator, category, plot_value, age_m = determine_growth_for_screening(s, student)
        if plot_value is None:
            continue

        if indicator == "BMI-for-Age":
            bmi_labels.append(age_m)
            bmi_values.append(plot_value)
            bmi_categories.append(category)

        elif indicator == "Weight-for-Height":
            wfh_labels.append(float(s.height))   # X = height (cm)
            wfh_values.append(float(s.weight))   # Y = weight (kg)
            wfh_categories.append(category)

    # WHO reference curves
    gender = "male" if student.gender.lower().startswith("m") else "female"

    who_bmi_curves = get_who_reference_curves("bmi", gender)
    who_wfh_curves = get_who_wfh_curves(gender)

    return (
        mark_safe(json.dumps(bmi_labels)),
        mark_safe(json.dumps(bmi_values)),
        mark_safe(json.dumps(bmi_categories)),
        mark_safe(json.dumps(wfh_labels)),
        mark_safe(json.dumps(wfh_values)),
        mark_safe(json.dumps(wfh_categories)),
        mark_safe(json.dumps(who_bmi_curves)),
        mark_safe(json.dumps(who_wfh_curves)),
    )

# -------------------------
# The view
# -------------------------




@login_required(login_url='login')
def screening_summary(request):
    from core.utils.processor import (
    calculate_age_in_months,
    calculate_bmi,
    bmi_category,
    muac_category,
    weight_height_category,
)


    # -----------------------------------
    # 1. GET FILTER PARAMETERS
    # -----------------------------------
    selected_school_id = request.GET.get('school')
    student_name_query = request.GET.get('student_name', '').strip()
    selected_student_id = request.GET.get('selected_student')

    # -----------------------------------
    # 2. SCHOOLS LIST
    # -----------------------------------
    schools = School.objects.all()

    # -----------------------------------
    # 3. FILTER STUDENTS
    # -----------------------------------
    students_qs = Student.objects.all()

    if selected_school_id and selected_school_id not in ("None", ""):
        students_qs = students_qs.filter(school_id=selected_school_id)

    if student_name_query:
        students_qs = students_qs.filter(name__icontains=student_name_query)

    students_qs = students_qs.order_by("name")

    # Pagination
    paginator = Paginator(students_qs, 10)
    page_number = request.GET.get("page")
    students_page = paginator.get_page(page_number)

    # -----------------------------------
    # 4. DEFAULTS FOR CHART (always defined!)
    # -----------------------------------
    chart_mode = "none"
    bmi_labels = bmi_values = bmi_categories = mark_safe("[]")
    wfh_labels = wfh_values = wfh_categories = mark_safe("[]")
    chart_who_bmi_curves = mark_safe("{}")
    chart_who_wfh_curves = mark_safe("{}")


    # -----------------------------------
    # 5. CHECKLIST GROUPS (static)
    # -----------------------------------
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

    # -----------------------------------
    # 6. LOAD SCREENINGS FOR SELECTED STUDENT
    # -----------------------------------
    student = None
    screenings = []

    if selected_student_id and selected_student_id not in ("None", ""):
        student = get_object_or_404(Student, id=selected_student_id)

        screenings = list(
            Screening.objects.filter(student=student).order_by("screen_date")
        )

        # Enrich screenings
        for s in screenings:
            s.checklist_dict = get_checklist_for_screening(s, checklist_groups)

            if student.date_of_birth:
                s.age_in_months = calculate_age_in_months(
                    student.date_of_birth, s.screen_date
                )

                # BMI
                s.bmi = calculate_bmi(s.weight, s.height)
                s.bmi_category = (
                    bmi_category(student.gender, s.age_in_months, s.bmi)
                    if s.bmi else "N/A"
                )

                # MUAC
                s.muac_category = (
                    muac_category(s.muac, s.age_in_months)
                    if s.muac else "N/A"
                )

                # Weight-for-Height
                s.wfh_category = (
                    weight_height_category(
                        s.weight,
                        s.height,
                        s.age_in_months,
                        student.gender
                    )
                    if s.weight and s.height else "N/A"
                )
            else:
                s.age_in_months = 0
                s.bmi = None
                s.bmi_category = "N/A"
                s.muac_category = "N/A"
                s.wfh_category = "N/A"

        # -----------------------------------
        # 7. Build Chart Data (safe)
        # -----------------------------------
        if student.date_of_birth:
            (
                bmi_labels,
                bmi_values,
                bmi_categories,
                wfh_labels,
                wfh_values,
                wfh_categories,
                chart_who_bmi_curves,
                chart_who_wfh_curves,
            ) = build_chart_data_for_student(screenings, student)

            # For now default to BMI chart
            chart_mode = "bmi"

    # -----------------------------------
    # 8. CONTEXT
    # -----------------------------------
    context = {
        "schools": schools,
        "students_page": students_page,
        "selected_school_id": int(selected_school_id) if selected_school_id and selected_school_id not in ("None", "") else None,
        "student_name": student_name_query,
        "selected_student_id": int(selected_student_id) if selected_student_id and selected_student_id not in ("None", "") else None,
        "student": student,
        "screenings": screenings,
        "checklist_groups": checklist_groups,

        # Chart Data
        "chart_mode": chart_mode,
        "bmi_labels": bmi_labels,
        "bmi_values": bmi_values,
        "bmi_categories": bmi_categories,
        "wfh_labels": wfh_labels,
        "wfh_values": wfh_values,
        "wfh_categories": wfh_categories,
        "chart_who_bmi_curves": chart_who_bmi_curves,
        "chart_who_wfh_curves": chart_who_wfh_curves,

    }

    return render(request, "core/screening_summary.html", context)

logger = logging.getLogger(__name__)


@login_required(login_url='login')
def screened_students(request):
    selected_school_id = request.GET.get("school")
    if selected_school_id in [None, "", "None"]:
        selected_school_id = None
    else:
        selected_school_id = int(selected_school_id)

    selected_student_id = request.GET.get("selected_student")
    name_query = request.GET.get("name", "").strip()

    student_form = None
    screening_forms = []
    selected_student = None

    if selected_student_id:
        selected_student = get_object_or_404(Student, pk=selected_student_id)

        # --- All screenings for this student ---
        screenings = Screening.objects.filter(student=selected_student).order_by('-screen_date')

        # If POST, save student info first
        if request.method == "POST":
            student_form = StudentForm(request.POST, instance=selected_student)
            if student_form.is_valid():
                student = student_form.save(commit=False)
                school_id = request.POST.get("school")
                if school_id:
                    try:
                        student.school = School.objects.get(pk=int(school_id))
                    except School.DoesNotExist:
                        student.school = None
                student.save()

            # Save all screenings
            for screening in screenings:
                prefix = f'screening_{screening.id}'
                screening_form = ScreeningForm(request.POST, instance=screening, prefix=prefix)
                checklist, _ = ScreeningCheck.objects.get_or_create(screening=screening)
                checklist_form = ScreeningCheckForm(request.POST, instance=checklist, prefix=prefix)
                if screening_form.is_valid() and checklist_form.is_valid():
                    screening_form.save()
                    checklist_form.save()

            return redirect(f"{request.path}?selected_student={selected_student.id}&school={selected_school_id}&name={name_query}")

        else:
            # GET: prepare forms for all screenings with unique prefixes
            student_form = StudentForm(instance=selected_student)
            for screening in screenings:
                prefix = f'screening_{screening.id}'
                screening_form = ScreeningForm(instance=screening, prefix=prefix)
                checklist, _ = ScreeningCheck.objects.get_or_create(screening=screening)
                checklist_form = ScreeningCheckForm(instance=checklist, prefix=prefix)
                screening_forms.append({
                    "screening_form": screening_form,
                    "checklist_form": checklist_form
                })

    # --- Student filtering & pagination ---
    students = Student.objects.select_related("school").only("id", "name", "school_id").order_by("name")
    if name_query:
        students = students.filter(name__icontains=name_query)
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)
    paginator = Paginator(students, 20)
    page_number = request.GET.get("page", 1)
    students_page = paginator.get_page(page_number)

    context = {
        "selected_school_id": int(selected_school_id) if selected_school_id else None,
        "selected_student": selected_student,
        "student_form": student_form,
        "screening_forms": screening_forms,
        "schools": School.objects.only("id", "name"),
        "students_page": students_page,
        "name_query": name_query,
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
from django.http import JsonResponse
from .models import ScreeningCheck, Student
from django.http import JsonResponse
from core.models import ScreeningCheck, Student

def get_last_remarks(request):
    student_id = request.GET.get("student_id")
    remarks = None
    if student_id:
        try:
            s = Student.objects.get(id=student_id)
            last_check = (
                ScreeningCheck.objects.filter(screening__student=s)
                .order_by("-screening__screen_date")
                .first()
            )
            if last_check:
                remarks = last_check.E9_remarks
        except Student.DoesNotExist:
            pass
    return JsonResponse({"remarks": remarks})



@login_required
def get_previous_screenings(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string

    student_id = request.GET.get('student_id')
    html = ""

    if student_id:
        student = get_object_or_404(Student, id=student_id)

        screening = Screening.objects.filter(student=student, screen_date__isnull=False).order_by('-screen_date').first()

        if screening:
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

            screening.checklist_dict = get_checklist_for_screening(screening, checklist_groups)
            screening.muac_category = muac_category_for(screening, student)

            html = render_to_string("core/_screening_card.html", {
                "screening": screening,
                "student": student,
                "checklist_groups": checklist_groups,
            })

    return JsonResponse({"html": html})





@login_required
def get_student_growth_chart_partial(request):
    student_id = request.GET.get("student_id")
    student = get_object_or_404(Student, id=student_id)
    screenings = Screening.objects.filter(student=student).order_by("screen_date")

    chart_mode = "bmi" if any(s.age_in_month >= 60 for s in screenings) else "wfh"
    labels = [s.age_in_month for s in screenings if s.age_in_month is not None]
    values = [s.bmi if s.age_in_month >= 60 else s.weight for s in screenings]
    reference = [s.bmi_category if s.age_in_month >= 60 else s.weight_for_height for s in screenings]

    data = {
        "labels": labels,
        "values": values,
        "reference": reference,
        "chart_mode": chart_mode,
        "who_curves": {},  # optional WHO data
    }
    return JsonResponse(data)

@login_required(login_url='login')
def get_student_card(request):
    student_id = request.GET.get("student_id")
    student = get_object_or_404(Student, id=student_id)
    html = render_to_string("core/_student_card.html", {"student": student})
    return HttpResponse(html)

@login_required
def get_school_students(request):
    school_id = request.GET.get("school_id")

    if not school_id:
        return JsonResponse({"students": []})

    students = (
        Student.objects
        .filter(school_id=school_id)
        .only("id", "name", "date_of_birth", "gender")
        .order_by("name")
    )

    data = [
        {
            "id": s.id,
            "name": s.name,
            "dob": s.date_of_birth.strftime("%Y-%m-%d") if s.date_of_birth else "",
            "gender": (s.gender.lower() if s.gender else ""),
        }
        for s in students
    ]

    return JsonResponse({"students": data})

from django.shortcuts import render



@login_required
def add_screening(request):
    from core.utils.thresholds import vision_list, critical_vision_set

    # --- GET params ---
    selected_school_id = request.GET.get("school")
    student_name_query = request.GET.get("student_name", "")
    selected_student_id = (
    request.POST.get("selected_student")
    or request.GET.get("selected_student")
)


    try:
        selected_school_id = int(selected_school_id)
    except (TypeError, ValueError):
        selected_school_id = None

    # --- Students queryset ---
    students = Student.objects.all()
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)
    if student_name_query:
        students = students.filter(name__icontains=student_name_query)
    paginator = Paginator(students.order_by("name"), 20)
    page_number = request.GET.get("page")
    students_page = paginator.get_page(page_number)

    # --- Selected student ---
    student = None
    if selected_student_id:
        try:
            student = Student.objects.get(id=selected_student_id)
        except (Student.DoesNotExist, ValueError):
            student = None

    # --- Forms ---
    if request.method == "POST" and student:
        screening_form = ScreeningForm(request.POST)
        screening_check_form = ScreeningCheckForm(request.POST)

        if screening_form.is_valid() and screening_check_form.is_valid():
            screening = screening_form.save(commit=False)
            screening.student = student
            screening.save()

            checklist = screening_check_form.save(commit=False)
            checklist.screening = screening
            checklist.save()

            # reset forms after successful save
            screening_form = ScreeningForm()
            screening_check_form = ScreeningCheckForm()

    else:
        screening_form = ScreeningForm(
            initial={"school": student.school_id if student else None}
        )
        screening_check_form = ScreeningCheckForm()


    # --- Previous screenings ---
    previous_screenings = list(Screening.objects.filter(student=student).order_by("-screen_date")) if student else []

    # --- Growth chart ---
    from django.utils.safestring import mark_safe
    from core.utils.processor import calculate_age_in_months, calculate_bmi, bmi_category, muac_category, weight_height_category


    
    screenings_for_chart = previous_screenings.copy()
    if student and student.date_of_birth:
        for s in screenings_for_chart:
            s.age_in_months = calculate_age_in_months(student.date_of_birth, s.screen_date)
            s.bmi = calculate_bmi(s.weight, s.height)
            s.bmi_category = bmi_category(student.gender, s.age_in_months, s.bmi) if s.bmi else "N/A"
            s.muac_category = muac_category(s.muac, s.age_in_months) if hasattr(s, "muac") else "N/A"

            s.wfh_category = weight_height_category(
            s.weight,
            s.height,
            s.age_in_months,
            student.gender
        ) if s.weight and s.height else "N/A"

        bmi_labels, bmi_values, bmi_categories, wfh_labels, wfh_values, wfh_categories,  chart_who_bmi_curves,chart_who_wfh_curves = build_chart_data_for_student(screenings_for_chart, student)
    else:
        bmi_labels = bmi_values = bmi_categories = mark_safe("[]")
        wfh_labels = wfh_values = wfh_categories = mark_safe("[]")
        chart_who_bmi_curves = mark_safe("{}")
        chart_who_wfh_curves = mark_safe("{}")

    # --- Prepare checklist dict for previous screenings ---
    checklist_groups = {
        "Preventive Care": ["vaccination", "deworming"],
        "Nutritional / Medical": [
            "B1_severe_anemia", "B2_vitA_deficiency", "B3_vitD_deficiency",
            "B4_goitre", "B5_oedema"
        ],
        "Other Medical Conditions": [
            "C1_convulsive_dis", "C2_otitis_media", "C3_dental_condition",
            "C4_skin_condition", "C5_rheumatic_heart_disease",
            "C6_others_TB_asthma"
        ],
        "Development / Learning Difficulties": [
            "D1_difficulty_seeing", "D2_delay_in_walking", "D3_stiffness_floppiness",
            "D5_reading_writing_calculatory_difficulty", "D6_speaking_difficulty",
            "D7_hearing_problems", "D8_learning_difficulties", "D9_attention_difficulties"
        ],
        "Other Observations": [
            "E3_depression_sleep", "E4_menarke", "E5_regularity_period_difficulties",
            "E6_UTI_STI", "E7_discharge", "E8_menstrual_pain", "E9_remarks"
        ]
    }

    for screening in previous_screenings:
        checklist = getattr(screening, "checklist", None)
        if checklist:
            screening.checklist_dict = {
                field.name: getattr(checklist, field.name)
                for field in checklist._meta.get_fields()
                if not field.auto_created  # skip reverse relations
            }
        else:
            screening.checklist_dict = {}

    # --- Final render ---
    return render(request, "core/new_screening.html", {
    "checklist_groups": checklist_groups,
    "schools": School.objects.all(),
    "students_page": students_page,
    "selected_school_id": selected_school_id,
    "student_name_query": student_name_query,
    "selected_student_id": selected_student_id,
    "student": student,
    "screening_form": screening_form,
    "screening_check_form": screening_check_form,
    "previous_screenings": previous_screenings,
    "screenings": screenings_for_chart,
    "bmi_labels": bmi_labels,
    "bmi_values": bmi_values,
    "bmi_categories": bmi_categories,
    "wfh_labels": wfh_labels,
    "wfh_values": wfh_values,
    "wfh_categories": wfh_categories,
    "chart_who_bmi_curves": chart_who_bmi_curves,
    "chart_who_wfh_curves": chart_who_wfh_curves,

    "vision_list": vision_list,
    "critical_vision_set": list(critical_vision_set),  # convert to list so JS works
})



def ajax_student_search(request):
    q = request.GET.get('q', '').strip()
    school_id = request.GET.get("school_id")

    if not school_id:
        return JsonResponse({"results": []})

    qs = Student.objects.filter(school_id=school_id)

    # Apply search only if user typed something
    if q:
        qs = qs.filter(name__icontains=q)

    # Limit results for speed
    qs = qs.order_by("name")[:30]

    results = [
        {
            'id': s.id,
            'name': s.name,
            'class_section': s.class_section or '',
        }
        for s in qs
    ]

    return JsonResponse({'results': results})


def dashboard_view(request):
    return render(request, "core/dashboard.html")








