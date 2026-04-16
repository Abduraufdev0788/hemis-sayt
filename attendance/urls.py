from django.urls import path
from .views import AttendanceView, StudentNBView, StudentRankingView, StudentTodayStatusView

urlpatterns = [
    path("attendance/", AttendanceView.as_view()),
    path("student/nb/", StudentNBView.as_view()),
    path("student/status/", StudentTodayStatusView.as_view()),
    path("student/ranking/", StudentRankingView.as_view()),
]