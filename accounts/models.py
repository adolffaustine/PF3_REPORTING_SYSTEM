from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.username

class GENDER_CHOICES(models.TextChoices):
    MALE = "M",'Male'
    FEMALE = "F",'Female'
    OTHER = "O",'Others'


class Role(models.Model):
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.role


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="user/profile", default="profile/avatar.jpeg")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES.choices, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_leader = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True, region="KE") # Assuming Kenya region for example
    role = models.ManyToManyField(Role, blank=True, related_name='profiles')

    def __str__(self):
        return f"{self.user.username.title()}'s Profile"
    
    def get_absolute_url(self):
        return reverse("accounts:profile_view", args=[self.user.username])
    
    def has_role(self, role_name):
        """Checks if the user has a specific role."""
        return self.role.filter(role__iexact=role_name).exists()

    @property
    def is_police(self):
        """Checks if the user is police (either by role or is_staff)."""
        return self.user.is_staff or self.has_role("Police")

    @property
    def is_doctor(self):
        """Checks if the user has the Doctor role."""
        return self.has_role("Doctor")

    @property
    def is_nurse(self):
        """Checks if the user has the Nurse role."""
        return self.has_role("Nurse")


