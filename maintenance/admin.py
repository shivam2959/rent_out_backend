from django.contrib import admin
from .models import MaintenanceRequest, MaintenanceComment
admin.site.register(MaintenanceRequest)
admin.site.register(MaintenanceComment)
