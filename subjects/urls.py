# subjects/urls.py
from django.urls import path
from .views import TeacherRegisterView

urlpatterns = [
    path('teacher/register/', TeacherRegisterView.as_view()),
]