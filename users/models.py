from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
        ('lease_operator', 'Lease Operator'),
        ('broker', 'Broker / Agent'),
        ('society_manager', 'Society Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class OwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owner_profile')
    kyc_document = models.FileField(upload_to='kyc/', blank=True, null=True)
    bank_account_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OwnerProfile: {self.user.username}"

class TenantProfile(models.Model):
    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tenant_profile')
    occupation = models.CharField(max_length=200, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # KYC
    government_id_type = models.CharField(
        max_length=50, blank=True,
        help_text="E.g. Aadhaar, PAN, Passport, Driving License"
    )
    government_id_number = models.CharField(max_length=100, blank=True)
    kyc_document = models.FileField(upload_to='kyc/tenants/', blank=True, null=True)
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS_CHOICES, default='pending')
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    # Legacy field kept for compatibility
    emergency_contact = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"TenantProfile: {self.user.username}"

class LeaseOperatorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='lease_operator_profile')
    company_name = models.CharField(max_length=200, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"LeaseOperatorProfile: {self.user.username}"


class BrokerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='broker_profile')
    agency_name = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"BrokerProfile: {self.user.username}"


class SocietyManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='society_manager_profile')
    society_name = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"SocietyManagerProfile: {self.user.username}"


class BrokerCommission(models.Model):
    """Tracks commission owed to a broker for onboarding a tenant via a lease."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    broker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='commissions_earned',
        limit_choices_to={'role': 'broker'},
    )
    # Deferred import via string reference to avoid circular imports
    lease = models.ForeignKey(
        'leases.LeaseAgreement', on_delete=models.CASCADE,
        related_name='broker_commissions',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission ₹{self.amount} for {self.broker.username} ({self.status})"
