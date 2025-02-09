from rest_framework.serializers import ModelSerializer
from hr.models import Hr, JobPost, JobPostApplication
from rest_framework import serializers
from user.models import CustomUser
from companion.models import Companion


class HrSerializer(ModelSerializer):
    class Meta:
        model = Hr
        exclude = ['creator', 'updator', 'is_deleted','is_blocked']
        extra_kwargs = {
            'photo': {'required': False},
            'linked_in': {'required': False},
            'rating': {'required': False},
            'user': {'required': False},  # Ensure user is not required here
        }

        
class HrJobPostSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'description', 'salary_from', 'salary_to', 'experience', 'skills', 'company', 'location']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with the actual user model if it's not named CustomUser
        fields = ['email', 'first_name', 'last_name']

class CompanionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Companion
        fields = ['user', 'resume']

class JobApplicationSerializer(serializers.ModelSerializer):
    companion = CompanionSerializer()
    job = HrJobPostSerializer()

    class Meta:
        model = JobPostApplication
        fields = ['id', 'job', 'companion', 'status', 'applied_at']
