from django.urls import path
from .views import DashboardSummaryView, RevenueReportView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('revenue/', RevenueReportView.as_view(), name='revenue-report'),
]
