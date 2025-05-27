from django.contrib import admin
from .models import Course, Lesson, Progress, Document, Quiz

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Document)
admin.site.register(Quiz)


# Register your models here.
