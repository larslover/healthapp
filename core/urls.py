from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Screenings
    # Only one path for screenings/
    path('screenings/', views.add_screening, name='screening_list'),

    path('students/ajax-search/', views.ajax_student_search, name='ajax_student_search'),



  



  
    path('screenings/<int:pk>/', views.screening_detail, name='screening_detail'),
    path('screenings/<int:pk>/edit/', views.screening_update, name='screening_update'),
    path('screenings/<int:pk>/delete/', views.screening_delete, name='screening_delete'),

    # Schools
    path('schools/', views.school_list, name='school_list'),
    path('schools/add/', views.school_create, name='school_create'),

    # Reports
    path('reports/', views.report_summary, name='report_summary'),

    # Statistics
    path('statistics/', views.statistics, name='statistics'),
]
