from django.urls import path
from user_auth.views.password_reset_views import ResetPasswordRequestView, ResetPasswordConfirmView
urlpatterns = [
    path('password-reset/request/', ResetPasswordRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', ResetPasswordConfirmView.as_view(), name='password-reset-confirm'),            
]