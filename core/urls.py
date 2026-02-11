from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Statistics
        path('statistics/', views.statistics, name='statistics'),  # <-- new
         path("ajax/get-classes/", views.get_classes_for_school, name="get_classes_for_school"),
         path("ajax/stat-students/", views.stat_students_ajax, name="stat_students_ajax"),


    # Students
    path('students/', views.screened_students, name='screened_students'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/ajax-search/', views.ajax_student_search, name='ajax_student_search'),
    path('schools/add/', views.school_create, name='school_create'),
    path("student/<int:pk>/delete/", views.delete_student, name="delete_student"),
    path("screening/<int:screening_id>/delete/", views.delete_screening,
    name="delete_screening"),


    # Screenings
    path('screenings/', views.add_screening, name='add_screening'),
    path('growth-reference/', views.growth_reference_api, name='growth_reference_api'),
    path('get_previous_screenings/', views.get_previous_screenings, name='get_previous_screenings'),
    path('get_school_students/', views.get_school_students, name='get_school_students'),
    path('get_student_card/', views.get_student_card, name='get_student_card'),
    path('get_student_growth_chart_partial/', views.get_student_growth_chart_partial, name='get_student_growth_chart_partial'),
    path('get_last_remarks/', views.get_last_remarks, name='get_last_remarks'),

    # Reports
    path('screening-summary/', views.screening_summary, name='screening_summary'),
]
