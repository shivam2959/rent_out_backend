from rest_framework import serializers
from .models import VacancyListing, VacancyApplication


class VacancyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'created_at', 'updated_at']


class VacancyListingSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VacancyListing
        fields = '__all__'
        read_only_fields = ['listed_by', 'created_at', 'updated_at']

    def get_applications_count(self, obj):
        return obj.applications.count()
