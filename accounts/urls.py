from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, ProfileView, PasswordChangeView,
    PasswordResetView, AdminUserListView, AdminUserDetailView
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    
    # Profile endpoints
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Admin endpoints
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
] 