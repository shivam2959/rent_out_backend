from rest_framework import serializers
from .models import Building, Room, BuildingPhoto, RoomPhoto


class BuildingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPhoto
        fields = ('id', 'photo', 'caption', 'is_primary', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = ('id', 'photo', 'caption', 'is_primary', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class RoomSerializer(serializers.ModelSerializer):
    photos = RoomPhotoSerializer(many=True, read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'building', 'building_name', 'room_number', 'floor', 'room_type',
                  'capacity', 'rent_amount', 'security_deposit', 'is_available',
                  'description', 'amenities', 'photos', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class RoomListSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'building', 'building_name', 'room_number', 'floor', 'room_type',
                  'capacity', 'rent_amount', 'is_available')


class BuildingSerializer(serializers.ModelSerializer):
    photos = BuildingPhotoSerializer(many=True, read_only=True)
    total_rooms = serializers.ReadOnlyField()
    available_rooms = serializers.ReadOnlyField()
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'owner', 'owner_email', 'name', 'address', 'city', 'state', 'pincode',
                  'description', 'total_floors', 'amenities', 'is_active',
                  'total_rooms', 'available_rooms', 'photos', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')


class BuildingListSerializer(serializers.ModelSerializer):
    total_rooms = serializers.ReadOnlyField()
    available_rooms = serializers.ReadOnlyField()

    class Meta:
        model = Building
        fields = ('id', 'name', 'city', 'state', 'total_floors', 'is_active',
                  'total_rooms', 'available_rooms', 'created_at')
