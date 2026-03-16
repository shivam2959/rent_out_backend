from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_OWNER = 'owner'
    ROLE_TENANT = 'tenant'
    ROLE_OPERATOR = 'operator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_OWNER, 'Owner'),
        (ROLE_TENANT, 'Tenant'),
        (ROLE_OPERATOR, 'Lease Operator'),
        (ROLE_ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_TENANT)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_owner(self):
        return self.role == self.ROLE_OWNER

    @property
    def is_tenant(self):
        return self.role == self.ROLE_TENANT

    @property
    def is_operator(self):
        return self.role == self.ROLE_OPERATOR


class OwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owner_profile')
    pan_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    pan_document = models.FileField(upload_to='kyc_documents/', null=True, blank=True)
    aadhar_document = models.FileField(upload_to='kyc_documents/', null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_ifsc_code = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    kyc_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Owner Profile: {self.user.email}"


class TenantProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tenant_profile')
    occupation = models.CharField(max_length=100, blank=True)
    employer_name = models.CharField(max_length=200, blank=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    id_proof_type = models.CharField(max_length=50, blank=True)
    id_proof_number = models.CharField(max_length=50, blank=True)
    id_proof_document = models.FileField(upload_to='id_documents/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tenant Profile: {self.user.email}"


class LeaseOperatorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='operator_profile')
    company_name = models.CharField(max_length=255, blank=True)
    company_registration_number = models.CharField(max_length=100, blank=True)
    gstin = models.CharField(max_length=20, blank=True)
    office_address = models.TextField(blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Operator Profile: {self.user.email}"
