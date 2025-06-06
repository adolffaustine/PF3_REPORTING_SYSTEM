from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic import CreateView, DetailView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm, CustomUserCreationForm, UserLoginForm, ProfileForm, CustomUserChangeForm, HospitalCreationForm, HospitalStaffCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Profile, Hospital, Role, User
# Create your views here.
# Create your views here.


class UserRegisterView(SuccessMessageMixin ,CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:index")
    success_message = "Account Successfully Created"
    
    def form_invalid(self, form):
        messages.error(self.request, "Error in Account Creation")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return super(UserRegisterView, self).dispatch(request, *args, **kwargs)
   
# User sign-in view
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('core:index')
        messages.error(request, 'Invalid username or password')
        return render(request, 'accounts/login.html', {'form': form})

# User registration view
def register(request):
    if request.method == 'GET':
        form = CreateUserForm()
        return render(request, 'accounts/register.html', {'form': form})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account successfully created')
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', {'form': form})

# User sign-out view
def sign_out(request):
    logout(request)
    return redirect('accounts:login')




class ProfileDetailAndUpdateView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        profile_form = ProfileForm(instance=profile)
        user_form = CustomUserChangeForm(instance=request.user)
        context = {
            "profile":profile,
            "profile_form":profile_form,
            "user_form":user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        profile = get_object_or_404(Profile, user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("accounts:profile")
        context = {
            "profile":profile,
            "profile_form":profile_form,
            "user_form":user_form,
        }
        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = "accounts/profile_view.html"
    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        profile = Profile.objects.get(user__username=username)
        context = {
            'profile':profile,
        }
        return render(request, self.template_name, context)


class PoliceRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.is_police

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to view this page.")
        return redirect('core:index')

class PoliceAdminRequiredMixin(UserPassesTestMixin): # Renamed to avoid conflict if core has one
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.is_staff and \
               hasattr(self.request.user, 'profile') and \
               self.request.user.profile.is_police

class HospitalListView(LoginRequiredMixin, PoliceRequiredMixin, ListView):
    model = Hospital
    template_name = 'accounts/hospital_list.html' # Create this template
    context_object_name = 'hospitals'

class HospitalCreateView(LoginRequiredMixin, PoliceRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'accounts/hospital_form.html' # Create this template
    form_class = HospitalCreationForm
    success_url = reverse_lazy('accounts:hospital_list')
    success_message = "Hospital and Admin User created successfully."

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        
        # Create Hospital Admin User
        admin_user = User.objects.create_user(
            username=cleaned_data['admin_username'],
            email=cleaned_data['admin_email'],
            password=cleaned_data['admin_password1']
        )
        
        # Create Profile for Admin User and assign "HospitalAdmin" role
        hospital_admin_role, created = Role.objects.get_or_create(role="HospitalAdmin")
        # Ensure profile is created for the new user
        # If you have a signal to create profile, this might be redundant or ensure it runs.
        # Otherwise, create it explicitly:
        profile, profile_created = Profile.objects.get_or_create(user=admin_user)
        profile.role.add(hospital_admin_role)
        profile.save()

        # Create Hospital
        hospital = Hospital.objects.create(
            name=cleaned_data['hospital_name'],
            address=cleaned_data['hospital_address'],
            admin_user=admin_user
        )
        # Link profile to hospital (optional for admin user, but good for consistency)
        # profile.hospital = hospital 
        # profile.save()
        return super().form_valid(form)
    

class HospitalAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if hasattr(self.request.user, 'profile') and self.request.user.profile.has_role("HospitalAdmin"):
            # Also check if this HospitalAdmin is associated with a hospital
            return hasattr(self.request.user, 'administered_hospital') and self.request.user.administered_hospital is not None
        return False

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to perform this action or not associated with a hospital.")
        return redirect('core:index')
    
class HospitalStaffListView(LoginRequiredMixin, HospitalAdminRequiredMixin, ListView):
    template_name = 'accounts/hospital_staff_list.html'
    context_object_name = 'staff_members'

    def get_queryset(self):
        # Get the hospital administered by the current user
        hospital_admin_user = self.request.user
        try:
            # The Hospital model has an 'admin_user' field linking to the User model
            # The Profile model has a 'hospital' field linking to the Hospital model
            admin_hospital = Hospital.objects.get(admin_user=hospital_admin_user)
            return Profile.objects.filter(hospital=admin_hospital).exclude(user=hospital_admin_user).select_related('user')
        except Hospital.DoesNotExist:
            return Profile.objects.none()

class HospitalStaffCreateView(LoginRequiredMixin, HospitalAdminRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'accounts/hospital_staff_form.html'
    form_class = HospitalStaffCreationForm
    success_message = "Staff member created successfully."

    def get_success_url(self):
        return reverse_lazy('accounts:hospital_staff_list')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        hospital_admin_user = self.request.user
        admin_hospital = hospital_admin_user.administered_hospital # Relies on related_name from Hospital.admin_user

        new_staff_user = User.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name']
        )

        staff_role = Role.objects.get(role=cleaned_data['role']) # Ensure 'Doctor' and 'Nurse' roles exist
        profile, created = Profile.objects.get_or_create(user=new_staff_user)
        profile.role.add(staff_role)
        profile.hospital = admin_hospital # Associate with the Hospital Admin's hospital
        profile.save()
        return super().form_valid(form)

class PoliceOfficerView(LoginRequiredMixin, PoliceAdminRequiredMixin, ListView):
    template_name = 'accounts/police_officer_list.html'
    context_object_name = 'officers'

    def get_queryset(self):
        police_role = Role.objects.filter(role__iexact="Police").first()
        return Profile.objects.filter(role=police_role).select_related('user') if police_role else Profile.objects.none()