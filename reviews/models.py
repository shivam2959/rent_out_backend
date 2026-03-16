from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from properties.models import Building
from leases.models import LeaseAgreement

class BuildingReview(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='reviews')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='building_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('building', 'tenant')

    def __str__(self):
        return f"Review by {self.tenant.username} for {self.building.name}: {self.rating}/5"

class TenantReview(models.Model):
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tenant_reviews_received')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tenant_reviews_given')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='tenant_reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.owner.username} for tenant {self.tenant.username}: {self.rating}/5"
