from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # ← добавили

    def __str__(self): return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)  # ← добавили

    class Meta: ordering = ["order"]
    def __str__(self): return self.title

class Document(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')

    def _str_(self):
        return self.title

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Progress'
        verbose_name_plural = 'Progress'

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def _str_(self):
        return self.question

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

# Create your models here.