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
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

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
