from django.urls import path
from .views import ChildrenRegisterView, ParentCreateView

urlpatterns = [
    path('api/parent/create/', ParentCreateView.as_view()),
    path('api/child/register/', ChildrenRegisterView.as_view()),
]