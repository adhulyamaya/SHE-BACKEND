from django.urls import include,path,re_path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user_api'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),

    path("forgot-password/", views.reset_password_view, name='forgot-password'),
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset, name='password-reset-confirm'),
    path("set-password/", views.set_new_password_api, name='set-password'),

    path('users/', views.get_all_users, name='get_all_users'),
    path('user-requests/', views.get_user_requests, name='user_requests'),
    path('block-user/<int:user_id>/', views.toggle_block_user, name='block_user'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('add-role/', views.add_role, name='add-role'),
    path('check-profile-completion/', views.check_profile_completion, name='check-profile-completion'),


]