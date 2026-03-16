from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return MaintenanceRequest.objects.filter(room__building__owner=user)
        return MaintenanceRequest.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        req = self.get_object()
        new_status = request.data.get('status')
        valid = [s[0] for s in MaintenanceRequest.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        req.status = new_status
        req.save()
        return Response(MaintenanceRequestSerializer(req).data)
