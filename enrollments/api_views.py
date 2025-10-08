# enrollments/api_views.py
from rest_framework import viewsets, permissions, decorators, response, status
from django.shortcuts import get_object_or_404
from .models import Enrollment
from .serializers import EnrollmentSerializer
from courses.models import Course

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.AllowAny]  # позже поставим IsAuthenticated

    @decorators.action(detail=False, methods=["post"], url_path="enroll/(?P<course_id>[^/.]+)")
    def enroll(self, request, course_id: int):
        # временно требуем авторизацию — потом подключим JWT
        if not request.user or not request.user.is_authenticated:
            return response.Response({"detail": "Auth required"}, status=status.HTTP_401_UNAUTHORIZED)
        course = get_object_or_404(Course, pk=course_id)
        obj, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        ser = self.get_serializer(obj)
        return response.Response(ser.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        if not request.user or not request.user.is_authenticated:
            return response.Response({"detail": "Auth required"}, status=status.HTTP_401_UNAUTHORIZED)
        qs = Enrollment.objects.filter(user=request.user)
        return response.Response(self.get_serializer(qs, many=True).data)
