from django.urls import path
from .views import GroupStudentsView

urlpatterns = [
    path('group/<int:group_id>/', GroupStudentsView.as_view()),
]
