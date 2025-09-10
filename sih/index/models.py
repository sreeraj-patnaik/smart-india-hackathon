from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/photos/", null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=(
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
            ("prefer_not_say", "Prefer not to say"),
        ),
        blank=True,
    )

    college_name = models.CharField(max_length=255, blank=True)
    college_type = models.CharField(max_length=255, blank=True)
    college_pin = models.CharField(max_length=20, blank=True)

    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)

    health_conditions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

# Create your models here.
