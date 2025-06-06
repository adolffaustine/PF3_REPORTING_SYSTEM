from django.urls import path

from django.contrib.auth.views import LogoutView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.sign_in, name='login'),
    path('logout', views.sign_out, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileDetailAndUpdateView.as_view(), name="profile"),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name="profile_view"),

    # Hospital Management URLs for Police
    path('hospitals/', views.HospitalListView.as_view(), name='hospital_list'),
    path('hospitals/create/', views.HospitalCreateView.as_view(), name='hospital_create'),

     # Hospital Admin - Staff Management URLs
    path('hospital/staff/', views.HospitalStaffListView.as_view(), name='hospital_staff_list'),
    path('hospital/staff/create/', views.HospitalStaffCreateView.as_view(), name='hospital_staff_create'),

    # Police Admin - Officer Management
    path('officers/', views.PoliceOfficerView.as_view(), name='police_officer_list'),
]