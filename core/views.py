
from core.utils.processor import bmi_category
from django.db.models import Prefetch
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Student, Screening, School
from .forms import ScreeningForm, ScreeningCheckForm
# core/views.py (snippet)
import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Student, Screening, ScreeningCheck, School
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from .models import School, Student, Screening
from .forms import ScreeningForm, ScreeningCheckForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import School, Student, Screening
from .forms import ScreeningForm, ScreeningCheckForm
from django.template.loader import render_to_string

import logging
from datetime import date
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from .models import School, Student, Screening, ScreeningCheck
from .utils.processor import muac_category, weight_height_category, bmi_category, calculate_age_in_months

from .forms import StudentForm
from django.db.models.functions import ExtractYear
from .models import Student, Screening, ScreeningCheck
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from .models import Screening, School,LegacyStudent
from django.http import JsonResponse
from core.legacy_helpers import get_all_students, search_students
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date
from .models import Student, School, Screening, ScreeningCheck
from .forms import ScreeningForm, ScreeningCheckForm
from .utils.processor import calculate_age_in_months
# views.py
from django.http import JsonResponse
from .models import Screening, Student
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
import time
from pathlib import Path
from django.http import JsonResponse
from datetime import date
from core.utils.processor import calculate_bmi, bmi_category, weight_height_category, calculate_age_in_months
from django.shortcuts import render, redirect
from .models import School
from .forms import SchoolForm  # You’ll create this form next

from django.http import HttpResponse
from django.templatetags.static import static
import os




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


def build_chart_data_for_student(screenings, student):
    if not screenings:
        empty = mark_safe("[]")
        return empty, empty, empty, empty, empty, empty, empty

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
            wfh_labels.append(s.height)
            wfh_values.append(plot_value)
            wfh_categories.append(category)

    # WHO curves (for both charts)
    gender = "male" if student.gender.lower().startswith("m") else "female"
    who_curves = get_who_reference_curves("bmi", gender)  # BMI curves
    # Optionally, WFH curves separately if needed

    return (
        mark_safe(json.dumps(bmi_labels)),
        mark_safe(json.dumps(bmi_values)),
        mark_safe(json.dumps(bmi_categories)),
        mark_safe(json.dumps(wfh_labels)),
        mark_safe(json.dumps(wfh_values)),
        mark_safe(json.dumps(wfh_categories)),
        mark_safe(json.dumps(who_curves)),
    )

# -------------------------
# The view
# -------------------------




@login_required(login_url='login')
def screening_summary(request):

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
    chart_who_curves = mark_safe("{}")

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
            s.muac_category = muac_category_for(s, student)

            if student.date_of_birth:
                indicator, cat, plot_val, age_m = determine_growth_for_screening(s, student)
            else:
                indicator, cat, plot_val, age_m = None, None, None, 0

            s.growth_indicator = indicator
            s.growth_category = cat
            s.age_in_months = age_m

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
                chart_who_curves
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
        "chart_who_curves": chart_who_curves,
    }

    return render(request, "core/screening_summary.html", context)

logger = logging.getLogger(__name__)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Student, Screening, ScreeningCheck, School
from .forms import StudentForm, ScreeningForm, ScreeningCheckForm
from django.contrib import messages

@login_required(login_url='login')
def screened_students(request):
    # --- Filters ---
    selected_school_id = request.GET.get("school")
    selected_student_id = request.GET.get("selected_student")
    name_query = request.GET.get("name", "").strip()

    # --- Selected student & forms ---
    student_form = screening_form = checklist_form = None
    selected_student = None

    if selected_student_id:
        selected_student = get_object_or_404(
            Student.objects.select_related("school"),
            pk=selected_student_id
        )

        # Get the last screening (you can change later to all screenings)
        screening = Screening.objects.filter(student=selected_student).last()
        if not screening:
            screening = Screening.objects.create(student=selected_student)

        checklist, _ = ScreeningCheck.objects.get_or_create(screening=screening)

        if request.method == "POST":
            student_form = StudentForm(request.POST, instance=selected_student)
            screening_form = ScreeningForm(request.POST, instance=screening)
            checklist_form = ScreeningCheckForm(request.POST, instance=checklist)

            if student_form.is_valid() and screening_form.is_valid() and checklist_form.is_valid():
                # Save student
                student = student_form.save(commit=False)
                school_id = request.POST.get("school")
                if school_id:
                    try:
                        student.school = School.objects.get(pk=int(school_id))
                    except School.DoesNotExist:
                        student.school = None
                student.save()

                # Save screening and checklist
                screening_form.save()
                checklist_form.save()

                # Optional: show success message
                messages.success(request, f"Student {student.name} updated successfully.")

                # Redirect to the same student edit view
                redirect_url = f"{reverse('screened_students')}?selected_student={student.id}"
                if selected_school_id:
                    redirect_url += f"&school={selected_school_id}"
                if name_query:
                    redirect_url += f"&name={name_query}"
                return redirect(redirect_url)
        else:
            student_form = StudentForm(instance=selected_student)
            screening_form = ScreeningForm(instance=screening)
            checklist_form = ScreeningCheckForm(instance=checklist)

    # --- Student filtering ---
    students = Student.objects.select_related("school").only("id", "name", "school_id").order_by("name")
    if name_query:
        students = students.filter(name__icontains=name_query)
    if selected_school_id:
        students = students.filter(school_id=selected_school_id)

    # --- Pagination ---
    paginator = Paginator(students, 20)  # 20 per page
    page_number = request.GET.get("page", 1)
    students_page = paginator.get_page(page_number)

    # --- Context ---
    context = {
        "selected_school_id": int(selected_school_id) if selected_school_id else None,
        "selected_student": selected_student,
        "student_form": student_form,
        "screening_form": screening_form,
        "checklist_form": checklist_form,
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





from django.http import JsonResponse
from .models import Screening
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
    from core.utils.processor import calculate_age_in_months, calculate_bmi, bmi_category, muac_category

    screenings_for_chart = previous_screenings.copy()
    if student and student.date_of_birth:
        for s in screenings_for_chart:
            s.age_in_months = calculate_age_in_months(student.date_of_birth, s.screen_date)
            s.bmi = calculate_bmi(s.weight, s.height)
            s.bmi_category = bmi_category(student.gender, s.age_in_months, s.bmi) if s.bmi else "N/A"
            s.muac_category = muac_category(s.muac, s.age_in_months) if hasattr(s, "muac") else "N/A"

        bmi_labels, bmi_values, bmi_categories, wfh_labels, wfh_values, wfh_categories, chart_who_curves = build_chart_data_for_student(
            screenings_for_chart, student
        )
    else:
        bmi_labels = bmi_values = bmi_categories = mark_safe("[]")
        wfh_labels = wfh_values = wfh_categories = mark_safe("[]")
        chart_who_curves = mark_safe("{}")
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
    "chart_who_curves": chart_who_curves,
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

from django.http import JsonResponse
from .models import Student

def dashboard_view(request):
    return render(request, "core/dashboard.html")








