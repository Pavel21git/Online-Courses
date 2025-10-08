from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    paid = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "course")
