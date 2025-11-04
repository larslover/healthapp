from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ Import this
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    # Students
    path('students/', views.screened_students, name='screened_students'),
    path('students/add/', views.student_create, name='student_create'),
  
  

    

    # Screenings
    # Only one path for screenings/
    path('screenings/', views.add_screening, name='screening_list'),
    path('students/add/', views.student_create, name='student_create'),
    path("growth-reference/", views.growth_reference_api, name="growth_reference_api"),
    path('students/ajax-search/', views.ajax_student_search, name='ajax_student_search'),


    # Reports
   
  
    path("screening-summary/", views.screening_summary, name="screening_summary"),


    path('students/', views.screened_students, name='screened_students'),
    path("get_last_remarks/", views.get_last_remarks, name="get_last_remarks"),
    

]
