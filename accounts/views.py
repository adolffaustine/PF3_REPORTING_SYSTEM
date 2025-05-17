from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.views import View
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from accounts.forms import CreateUserForm, LoginForm
from accounts.forms import CustomUserCreationForm, UserLoginForm, ProfileForm, CustomUserChangeForm
from accounts.models import Profile
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

# class UserLoginView(SuccessMessageMixin, LoginView):
#     form_class = UserLoginForm
#     template_name = 'accounts/login.html'
#     success_message = "Login Successfull"
#     success_url = reverse_lazy("core:index")
#     def form_invalid(self, form):
#         messages.error(self.request, "Error in Login")
#         return super().form_invalid(form)
    
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('core:index')
#         return super(UserLoginView,self).dispatch(request, *args, **kwargs)



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
