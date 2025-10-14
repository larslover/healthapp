
from core.utils.bmi_processor import bmi_category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, School,LegacyStudent
from .forms import StudentForm, ScreeningForm, SchoolForm
from django.http import JsonResponse
from .processor import search_students, get_all_students  # we'll add get_all_students
from .processor import get_all_students, search_students
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


def add_screening(request):
    students = Student.objects.all().order_by('name')  # existing students
    screening_form = ScreeningForm()

    if request.method == "POST":
        selected_student_id = request.POST.get("student")
        if not selected_student_id:
            # No student selected
            return render(request, "core/screening_list.html", {
                "students": students,
                "screening_form": screening_form,
                "error": "Please select a student first."
            })

        # Fetch the student first
        student = get_object_or_404(Student, id=selected_student_id)

        # Bind the form
        screening_form = ScreeningForm(request.POST)
        if screening_form.is_valid():
            # Save without committing
            screening = screening_form.save(commit=False)
            screening.student = student  # assign student first

            # Calculate BMI and category
            screening.calculate_bmi()  # calculates BMI and sets bmi_category if student is present

            # Optional: override bmi_category explicitly using the utility function
            if screening.bmi and student.gender:
                screening.bmi_category = bmi_category(
                    gender=student.gender,
                    month=str(screening.age_in_month or ""),
                    bmi_value=screening.bmi
                )

            screening.save()  # now safe to save
            messages.success(request, f"Screening for {student.name} saved successfully!")
            return redirect('screening_list')

    return render(request, "core/screening_list.html", {
        "students": students,
        "screening_form": screening_form
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
