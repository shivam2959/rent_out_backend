from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    OwnerProfileView, TenantProfileView, LeaseOperatorProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/owner/', OwnerProfileView.as_view(), name='owner-profile'),
    path('profile/tenant/', TenantProfileView.as_view(), name='tenant-profile'),
    path('profile/lease-operator/', LeaseOperatorProfileView.as_view(), name='lease-operator-profile'),
]
