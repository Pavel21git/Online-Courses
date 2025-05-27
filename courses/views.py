from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Course, Progress
from .forms import SignUpForm


@login_required
def complete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    progress, created = Progress.objects.get_or_create(user=request.user, course=course)
    progress.completed = True
    progress.save()
    return redirect("course_detail", pk=pk)


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("course_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lesson_set.all()
    return render(
        request, "courses/course_detail.html", {"course": course, "lessons": lessons}
    )


# Create your views here.
