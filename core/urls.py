from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ Import this
urlpatterns = [
   path('get_school_students/', views.get_school_students, name='get_school_students'),
    path('get_student_card/', views.get_student_card, name='get_student_card'),
    # urls.py
 path('get_student_growth_chart_partial/', views.get_student_growth_chart_partial, name='get_student_growth_chart_partial'),





    path('get_previous_screenings/', views.get_previous_screenings, name='get_previous_screenings'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    # Students
    path('students/', views.screened_students, name='screened_students'),
    path('students/add/', views.student_create, name='student_create'),
  
  

    

    # Screenings
    # Only one path for screenings/
    path('screenings/', views.add_screening, name='new_screening'),
    path('students/add/', views.student_create, name='student_create'),
    path("growth-reference/", views.growth_reference_api, name="growth_reference_api"),
    path('students/ajax-search/', views.ajax_student_search, name='ajax_student_search'),


    # Reports
   
  path('schools/add/', views.school_create, name='school_create'),

    path("screening-summary/", views.screening_summary, name="screening_summary"),


    path('students/', views.screened_students, name='screened_students'),
    path("get_last_remarks/", views.get_last_remarks, name="get_last_remarks"),
    

]
