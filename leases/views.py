from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LeaseAgreement
from .serializers import LeaseAgreementSerializer

class LeaseAgreementViewSet(viewsets.ModelViewSet):
    serializer_class = LeaseAgreementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'tenant':
            return LeaseAgreement.objects.filter(tenant=user)
        if user.role == 'owner':
            return LeaseAgreement.objects.filter(owner=user)
        return LeaseAgreement.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        lease = self.get_object()
        new_status = request.data.get('status')
        valid = [s[0] for s in LeaseAgreement.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        lease.status = new_status
        lease.save()
        return Response(LeaseAgreementSerializer(lease).data)
