from django.urls import path
from users.views import (
    SignUpCreateAPIView, CodeVerifiedAPIView,
    ResendVerifyCodeAPIView, UserListView,
    UserUpdateAPIView, ForgetPasswordView,
    LoginView, LogoutView, RefreshTokenView
)

app_name = 'users'

urlpatterns = [
    path('list/', UserListView.as_view(), name='list'),
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('lofresh/token/', RefreshTokenView.as_view(), name='refresh'),
    path('vegout/', LogoutView.as_view(), name='logout'),
    path('rerify/', CodeVerifiedAPIView.as_view(), name='verify'),
    path('resend/code/', ResendVerifyCodeAPIView.as_view(), name='verify-resend'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    path('password/forget/', ForgetPasswordView.as_view(), name='forget-password'),
]   