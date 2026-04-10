from django.urls import path
from .views import ChildrenRegisterView, ParentCreateView, ChildrenLoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('api/parent/create/', ParentCreateView.as_view()),
    path('api/child/register/', ChildrenRegisterView.as_view()),
    path('api/child/login/', ChildrenLoginView.as_view()),
    path('api/child/logout/', LogoutView.as_view()),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

