from django.urls import path
from .views import ParentCreateView

urlpatterns = [
    path('api/parent/create/', ParentCreateView.as_view()),
]