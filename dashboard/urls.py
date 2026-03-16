from django.urls import path
from .views import OwnerDashboardView, TenantDashboardView, AnalyticsDashboardView

urlpatterns = [
    path('owner/', OwnerDashboardView.as_view(), name='owner-dashboard'),
    path('tenant/', TenantDashboardView.as_view(), name='tenant-dashboard'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
]
