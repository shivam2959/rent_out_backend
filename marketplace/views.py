from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import VacancyListing, VacancyApplication
from .serializers import VacancyListingSerializer, VacancyApplicationSerializer


class VacancyListingViewSet(viewsets.ModelViewSet):
    """
    Owners/lease-operators manage listings; tenants can browse active vacancies.
    Search by city, building type, room type, rent range.
    """
    serializer_class = VacancyListingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'title', 'description',
        'room__building__city', 'room__building__state',
        'room__room_type', 'room__building__building_type',
    ]
    ordering_fields = ['monthly_rent', 'available_from', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'tenant':
            return VacancyListing.objects.filter(status='active')
        if user.role in ('owner', 'lease_operator'):
            return VacancyListing.objects.filter(listed_by=user)
        return VacancyListing.objects.all()

    def perform_create(self, serializer):
        serializer.save(listed_by=self.request.user)

    @action(detail=True, methods=['post'])
    def fill(self, request, pk=None):
        """Mark listing as filled (vacancy taken)."""
        listing = self.get_object()
        listing.status = 'filled'
        listing.save()
        return Response(VacancyListingSerializer(listing).data)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        listing = self.get_object()
        listing.status = 'paused'
        listing.save()
        return Response(VacancyListingSerializer(listing).data)


class VacancyApplicationViewSet(viewsets.ModelViewSet):
    """Tenants apply for vacancies; owners/admins review applications."""
    serializer_class = VacancyApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'tenant':
            return VacancyApplication.objects.filter(applicant=user)
        if user.role in ('owner', 'lease_operator'):
            return VacancyApplication.objects.filter(listing__listed_by=user)
        return VacancyApplication.objects.all()

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        app = self.get_object()
        app.status = 'approved'
        app.save()
        return Response(VacancyApplicationSerializer(app).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        app = self.get_object()
        app.status = 'rejected'
        app.owner_notes = request.data.get('notes', '')
        app.save()
        return Response(VacancyApplicationSerializer(app).data)

    @action(detail=True, methods=['post'])
    def shortlist(self, request, pk=None):
        app = self.get_object()
        app.status = 'shortlisted'
        app.save()
        return Response(VacancyApplicationSerializer(app).data)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        app = self.get_object()
        app.status = 'withdrawn'
        app.save()
        return Response(VacancyApplicationSerializer(app).data)
