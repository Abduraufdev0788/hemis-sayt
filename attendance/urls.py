from django.urls import path
from .views import StudentNBView

urlpatterns = [
    path('student/nb/', StudentNBView.as_view()),
]