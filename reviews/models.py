from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class BuildingReview(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='building_reviews')
    building = models.ForeignKey('properties.Building', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_verified_tenant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'building')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.building.name} ({self.rating}/5)"


class TenantReview(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_tenant_reviews')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_tenant_reviews')
    building = models.ForeignKey('properties.Building', on_delete=models.CASCADE, related_name='tenant_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'tenant')
        ordering = ['-created_at']

    def __str__(self):
        return f"Tenant Review by {self.reviewer.email} for {self.tenant.email} ({self.rating}/5)"
