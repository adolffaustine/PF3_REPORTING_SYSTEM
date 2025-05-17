# Error analysis:
# The new traceback indicates a TypeError: MultiWidget.__init__() missing 1 required positional argument: 'widgets'.
# This happens on the line where PhoneNumberPrefixWidget() is instantiated: "phone_number": PhoneNumberPrefixWidget().
# The PhoneNumberPrefixWidget, inheriting from MultiWidget, requires a list or tuple of sub-widgets to be passed during initialization.
# However, when using a ModelForm with a PhoneNumberField from django-phonenumber-field, Django automatically uses the correct default widget (PhoneNumberPrefixWidget) associated with that field type.
# Explicitly defining the widget in the `widgets` dictionary is usually unnecessary unless you need to customize its attributes (which wasn't the case here, and the previous attempt to pass 'initial' was incorrect).
# By trying to instantiate PhoneNumberPrefixWidget() directly without arguments, we violate its constructor's requirement for the 'widgets' argument.

# Correction:
# Remove the explicit widget definition for 'phone_number' from the `widgets` dictionary.
# The ModelForm will automatically use the default PhoneNumberPrefixWidget provided by the PhoneNumberField in the Profile model.

# Corrected code:
# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Profile, Role
from django.core.exceptions import ValidationError

from django import forms


from datetime import date

from accounts.models import Profile

# No need to import PhoneNumberPrefixWidget if we are not instantiating it directly here
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields =['username','email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username','password','remember_me']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class UserForm(forms.ModelForm):
    class Meta:
        model =  User
        fields = ['first_name','last_name','username','email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio','gender','date_of_birth','phone_number','role','is_leader']
        # Remove the widgets dictionary entirely if 'phone_number' was the only entry,
        # or just remove the 'phone_number' key-value pair if there were other widgets.
        # The ModelForm will automatically use the default widget for the PhoneNumberField.
        # widgets = {
        #     # "phone_number": PhoneNumberPrefixWidget(), # This line caused the TypeError
        # }

    def clean_date_of_birth(self, *args, **kwargs):
        dateOfBirth = self.cleaned_data.get("date_of_birth")
        if dateOfBirth is not None:
            # Use date.today() for comparison
            if dateOfBirth > date.today():
                raise ValidationError("Invalid Date of Birth")
        return dateOfBirth

class HospitalCreationForm(forms.Form):
    hospital_name = forms.CharField(max_length=255, label="Hospital Name")
    hospital_address = forms.CharField(widget=forms.Textarea, required=False, label="Hospital Address")
    
    admin_username = forms.CharField(max_length=150, label="Hospital Admin Username")
    admin_email = forms.EmailField(label="Hospital Admin Email")
    admin_password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    admin_password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def clean_admin_username(self):
        username = self.cleaned_data.get('admin_username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("admin_password1")
        password_2 = cleaned_data.get("admin_password2")
        if password_1 and password_2 and password_1 != password_2:
            self.add_error('admin_password2', "Passwords do not match.")
        return cleaned_data
    

class HospitalStaffCreationForm(forms.Form):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
    ]
    first_name = forms.CharField(max_length=150, label="First Name")
    last_name = forms.CharField(max_length=150, label="Last Name")
    username = forms.CharField(max_length=150, label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Assign Role")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data