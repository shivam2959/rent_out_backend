from django.db import models
from users.models import CustomUser
from properties.models import Room


class VacancyListing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('filled', 'Filled'),
        ('expired', 'Expired'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='vacancy_listings')
    listed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vacancy_listings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    available_from = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} – Room {self.room.room_number} ({self.status})"


class VacancyApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('shortlisted', 'Shortlisted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    listing = models.ForeignKey(VacancyListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vacancy_applications')
    message = models.TextField(blank=True, help_text="Cover message from the applicant")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    owner_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('listing', 'applicant')

    def __str__(self):
        return f"Application by {self.applicant.username} for {self.listing.title} ({self.status})"
