from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Students
    path('students/', views.screened_students, name='screened_students'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    

    # Screenings
    # Only one path for screenings/
    path('screenings/', views.add_screening, name='screening_list'),
    path('students/add/', views.student_create, name='student_create'),

    path('students/ajax-search/', views.ajax_student_search, name='ajax_student_search'),



  



  
   
    # Schools
    path('schools/', views.school_list, name='school_list'),
    path('schools/add/', views.school_create, name='school_create'),

    # Reports
    path('reports/', views.report_summary, name='report_summary'),
    path('report-summary/', views.report_summary, name='report_summary'),
    path("screening-summary/", views.screening_summary, name="screening_summary"),



    # Statistics
    path('statistics/', views.statistics, name='statistics'),
]
