from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TenantOnboardingRequest(models.Model):
    STATUS_CHOICES = [
        ('step1', 'Step 1 - Basic Info'),
        ('step2', 'Step 2 - Identity Verification'),
        ('step3', 'Step 3 - Employment Details'),
        ('step4', 'Step 4 - Emergency Contact'),
        ('step5', 'Step 5 - Previous Rental History'),
        ('step6', 'Step 6 - Document Upload'),
        ('step7', 'Step 7 - Agreement & Submission'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='onboarding_requests')
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, related_name='onboarding_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='step1')
    current_step = models.PositiveIntegerField(default=1)
    # Step 1: Basic Info
    move_in_date = models.DateField(null=True, blank=True)
    num_occupants = models.PositiveIntegerField(default=1)
    purpose = models.CharField(max_length=100, blank=True)
    # Step 2: Identity
    id_type = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    id_document = models.FileField(upload_to='onboarding_docs/', null=True, blank=True)
    # Step 3: Employment
    employment_type = models.CharField(max_length=50, blank=True)
    employer = models.CharField(max_length=200, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    income_proof = models.FileField(upload_to='onboarding_docs/', null=True, blank=True)
    # Step 4: Emergency Contact
    emergency_name = models.CharField(max_length=200, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    emergency_relation = models.CharField(max_length=50, blank=True)
    # Step 5: Previous Rental
    previous_address = models.TextField(blank=True)
    previous_landlord = models.CharField(max_length=200, blank=True)
    previous_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason_for_leaving = models.CharField(max_length=255, blank=True)
    # Step 6: Documents
    additional_document = models.FileField(upload_to='onboarding_docs/', null=True, blank=True)
    # Step 7: Agreement
    terms_accepted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_onboardings'
    )
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Onboarding: {self.tenant.email} - Room {self.room.room_number}"
