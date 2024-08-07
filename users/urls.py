from django.urls import path
from users.views import (
    SignUpCreateAPIView, CodeVerifiedAPIView,
    ResendVerifyCodeAPIView, UserListView,
    UserUpdateAPIView, ForgetPasswordView,
    LoginView, LogoutView, RefreshTokenView, UserProfileView
)

app_name = 'users'

urlpatterns = [
    path('list/', UserListView.as_view(), name='list'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('lofresh/token/', RefreshTokenView.as_view(), name='refresh'),
    path('vegout/', LogoutView.as_view(), name='logout'),
    path('verify/', CodeVerifiedAPIView.as_view(), name='verify'),
    path('resend/code/', ResendVerifyCodeAPIView.as_view(), name='verify-resend'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    path('password/forget/', ForgetPasswordView.as_view(), name='forget-password'),
]   