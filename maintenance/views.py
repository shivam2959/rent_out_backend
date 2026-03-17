from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MaintenanceRequest, MaintenanceComment
from .serializers import MaintenanceRequestSerializer, MaintenanceCommentSerializer

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
        if new_status == 'completed':
            from django.utils import timezone
            req.resolved_at = timezone.now()
        req.save()
        return Response(MaintenanceRequestSerializer(req).data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        req = self.get_object()
        serializer = MaintenanceCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=req, commenter=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MaintenanceCommentViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('owner', 'admin'):
            return MaintenanceComment.objects.filter(request__room__building__owner=user)
        return MaintenanceComment.objects.filter(request__tenant=user)

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)
