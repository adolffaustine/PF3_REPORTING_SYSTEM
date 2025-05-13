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
]