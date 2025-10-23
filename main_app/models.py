from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


def resume_upload_path(instance, filename):
    return f"career_casts/resumes/user_{instance.user.id}/{filename}"


def video_upload_path(instance, filename):
    return f"career_casts/videos/user_{instance.user.id}/{filename}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def get_profile_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        return self.username[0].upper()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )


class CareerCast(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teleprompter_text = models.TextField(null=True, blank=True)
    resume_file = models.FileField(upload_to=resume_upload_path, null=True, blank=True)
    video_file = models.FileField(upload_to=video_upload_path, null=True, blank=True)

    def __str__(self):
        return self.job_title

