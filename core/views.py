
from core.utils.processor import bmi_category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, School,LegacyStudent
from .forms import StudentForm, ScreeningForm, SchoolForm
from django.http import JsonResponse
from core.legacy_helpers import get_all_students, search_students
from core.utils.processor import calculate_bmi, bmi_category, muac_category, calculate_age_in_months

from django.contrib import messages

def legacy_students_view(request):
    students = LegacyStudent.objects.all()[:50]  # read only
    return render(request, 'core/legacy_students.html', {'students': students})

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # redirect back to the student list
    else:
        form = StudentForm()

    return render(request, 'core/student_create.html', {'form': form})

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

def add_screening(request):
    students = Student.objects.all().order_by('name')
    schools = School.objects.all()  # <-- add this

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
            from datetime import datetime
            screen_date = datetime.strptime(screen_date_str, "%Y-%m-%d").date()
            age_in_months = calculate_age_in_months(student.date_of_birth, screen_date)

    # Initialize forms
    if request.method == "POST":
        screening_form = ScreeningForm(request.POST, initial=initial_data)
        screening_check_form = ScreeningCheckForm(request.POST)
        if screening_form.is_valid() and screening_check_form.is_valid():
            screening = screening_form.save(commit=False)
            screening.student = student
            screening.calculate_metrics()
            screening.save()

            check = screening_check_form.save(commit=False)
            check.student = student
            check.screen_date = screening.screen_date
            check.save()

            messages.success(request, f"Screening for {student.name} saved successfully!")
            return redirect("screening_list")
    else:
        screening_form = ScreeningForm(initial=initial_data)
        screening_check_form = ScreeningCheckForm()

    return render(request, "core/screening_list.html", {
        "students": students,
        "schools": schools,  # <-- add this
        "screening_form": screening_form,
        "screening_check_form": screening_check_form,
        "age_in_months": age_in_months
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
    return render(request, 'core/student_list.html', {})


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
