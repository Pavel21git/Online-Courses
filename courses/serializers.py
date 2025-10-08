from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        # без order, если его нет в модели
        fields = ["id", "title", "content", "course"]

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # без price, если его нет в модели
        fields = ["id", "title", "description", "lessons"]
