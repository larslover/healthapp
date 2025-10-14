from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Screening, School,LegacyStudent
from .forms import StudentForm, ScreeningForm, SchoolForm
from django.http import JsonResponse
from .processor import search_students
from django.shortcuts import render, redirect
from .forms import StudentForm, ScreeningForm
from .models import School
from .processor import search_students, get_all_students  # we'll add get_all_students
from .models import LegacyStudent

def legacy_students_view(request):
    students = LegacyStudent.objects.all()[:50]  # read only
    return render(request, 'core/legacy_students.html', {'students': students})
from django.shortcuts import render, redirect
from .forms import StudentForm, ScreeningForm
from .models import School, LegacyStudent, Student, Screening
from .processor import get_all_students, search_students

from django.shortcuts import render, redirect
from .forms import StudentForm, ScreeningForm
from .models import School
from .processor import get_all_students, search_students

from django.shortcuts import render, redirect
from .models import LegacyStudent, Screening
from .forms import ScreeningForm

from django.shortcuts import render, redirect
from .models import LegacyStudent
from .forms import StudentForm, ScreeningForm
from django.shortcuts import render, redirect
from .models import LegacyStudent, Student, Screening, School
from .forms import StudentForm, ScreeningForm

def add_screening(request):
    students = LegacyStudent.objects.using('legacy').all()
    schools = LegacyStudent.objects.using('legacy') \
              .values_list('school_name', flat=True) \
              .distinct().order_by('school_name')

    student_form = StudentForm()
    screening_form = ScreeningForm()
    selected_student = None

    if request.method == "POST":
        selected_student_id = request.POST.get("student")

        if selected_student_id:
            # Existing student selected
            selected_student = students.filter(id=selected_student_id).first()
            if not selected_student:
                return render(request, "core/screening_list.html", {
                    'students': students,
                    'schools': schools,
                    'student_form': student_form,
                    'screening_form': screening_form,
                    'error': "Selected student not found."
                })
        else:
            # Save new student first
            student_form = StudentForm(request.POST)
            if student_form.is_valid():
                selected_student = student_form.save()
            else:
                return render(request, "core/screening_list.html", {
                    'students': students,
                    'schools': schools,
                    'student_form': student_form,
                    'screening_form': screening_form,
                    'error': "Please correct the errors in the student form."
                })

        # Only now allow screening to be saved
        screening_form = ScreeningForm(request.POST)
        if screening_form.is_valid():
            screening = screening_form.save(commit=False)
            screening.student = selected_student  # link student
            screening.save()
            return redirect('screening_list')
        else:
            return render(request, "core/screening_list.html", {
                'students': students,
                'schools': schools,
                'student_form': student_form,
                'screening_form': screening_form,
                'error': "Please correct the errors in the screening form."
            })

    return render(request, "core/screening_list.html", {
        'students': students,
        'schools': schools,
        'student_form': student_form,
        'screening_form': screening_form,
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

def student_create(request):
    return render(request, 'core/student_form.html', {})

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
