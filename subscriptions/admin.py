from django.contrib import admin
from .models import Subscription, SubscriptionInvoice

admin.site.register(Subscription)
admin.site.register(SubscriptionInvoice)
