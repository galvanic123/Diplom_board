from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserCreateView,
    MyTokenObtainPairView,
    PasswordResetView,
    PasswordResetConfirmView
)

app_name = "users"

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
