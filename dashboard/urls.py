from django.urls import path
from .views import OwnerDashboardView, TenantDashboardView, AdminDashboardView

urlpatterns = [
    path('owner/', OwnerDashboardView.as_view(), name='owner-dashboard'),
    path('tenant/', TenantDashboardView.as_view(), name='tenant-dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
