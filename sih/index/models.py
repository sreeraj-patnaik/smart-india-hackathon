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


class DoctorContact(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    organization = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class TestReport(models.Model):
    TEST_TYPES = (
        ("PHQ9", "PHQ-9"),
        ("GAD7", "GAD-7"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_reports")
    test_type = models.CharField(max_length=10, choices=TEST_TYPES)
    score = models.IntegerField()
    raw_answers = models.JSONField(default=dict, blank=True)
    is_anonymous = models.BooleanField(default=False)
    anon_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} {self.test_type} {self.score}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages")
    message = models.TextField()
    is_user = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    anon_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ChatMessage({self.user.username}, {'user' if self.is_user else 'ai'})"


class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    anon_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

# Create your models here.
