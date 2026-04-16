from django.urls import path
from .views import TeacherGroupsView, TeacherStatsView, TeacherStudentsView, TeacherProfileView

urlpatterns = [
    path("teacher/students/", TeacherStudentsView.as_view()),
    path("teacher/stats/", TeacherStatsView.as_view()),
    path("teacher/profile/", TeacherProfileView.as_view()),
    path("teacher/groups/", TeacherGroupsView.as_view()),
]
