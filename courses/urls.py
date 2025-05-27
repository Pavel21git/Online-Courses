from django.urls import path
from . import views
from .views import signup_view
from .views import complete_course

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/complete/', complete_course, name='complete_course'),  # ← новинка
    path('signup/', views.signup_view, name='signup'),
]