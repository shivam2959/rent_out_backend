from rest_framework import serializers
from .models import Building, BuildingPhoto, Room, RoomPhoto


class BuildingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPhoto
        fields = '__all__'
        read_only_fields = ['created_at']


class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = '__all__'
        read_only_fields = ['created_at']


class RoomSerializer(serializers.ModelSerializer):
    photos = RoomPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BuildingSerializer(serializers.ModelSerializer):
    photos = BuildingPhotoSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    total_rooms = serializers.SerializerMethodField()
    available_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_total_rooms(self, obj):
        return obj.rooms.count()

    def get_available_rooms(self, obj):
        return obj.rooms.filter(status='available').count()


class BuildingListSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    total_rooms = serializers.SerializerMethodField()
    available_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ['id', 'name', 'building_type', 'city', 'state', 'is_active',
                  'owner_email', 'total_rooms', 'available_rooms', 'created_at']

    def get_total_rooms(self, obj):
        return obj.rooms.count()

    def get_available_rooms(self, obj):
        return obj.rooms.filter(status='available').count()
