from rest_framework import serializers
from .models import Amenity, Building, BuildingPhoto, Floor, Room, RoomPhoto

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class BuildingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPhoto
        fields = '__all__'

class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    photos = RoomPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    photos = BuildingPhotoSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    floors = FloorSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Amenity.objects.all(), write_only=True, source='amenities', required=False
    )

    class Meta:
        model = Building
        fields = '__all__'
        read_only_fields = ['owner']
