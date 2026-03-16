from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class BuildingReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='building_reviews')
    building = models.ForeignKey('properties.Building', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255, blank=True)
    review = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['reviewer', 'building']

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.building.name} - {self.rating}/5"


class TenantReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_reviews_given')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_reviews_received')
    lease = models.ForeignKey('leases.LeaseAgreement', on_delete=models.CASCADE, related_name='tenant_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255, blank=True)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['reviewer', 'lease']

    def __str__(self):
        return f"Review by {self.reviewer.email} for tenant {self.tenant.email} - {self.rating}/5"
