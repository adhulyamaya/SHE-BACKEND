from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mentor.models import Mentor, MentorshipRequest
from user.models import CustomUser
from companion.models import Companion
from project.models import Project
from django.shortcuts import get_object_or_404


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with the actual user model if it's not named CustomUser
        fields = ['first_name','last_name','email','roles']

class CompanionSerializer(ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Companion
        fields = '__all__'

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class MentorSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only = True)

    class Meta:
        model = Mentor
        exclude = ['creator', 'updator', 'is_deleted','is_blocked','rating','feedback']
        read_only_fields = ['user']

class MentorshipRequestSerializer(serializers.ModelSerializer):
    companion = serializers.UUIDField()  # Expecting UUID for companion
    project = serializers.UUIDField()  # Expecting UUID for project

    class Meta:
        model = MentorshipRequest
        fields = ['id', 'mentor', 'project', 'status', 'companion'] 
    
    def validate(self, data):
        # Custom validation logic if required
        if not data.get('mentor'):
            raise serializers.ValidationError("Mentor ID is required.")
        if not data.get('project'):
            raise serializers.ValidationError("Project ID is required.")
        if not data.get('companion'):
            raise serializers.ValidationError("Companion ID is required.")
        return data

    def create(self, validated_data):
        # Fetch the Companion and Project objects based on UUIDs
        companion_uuid = validated_data.pop('companion') 
        project_uuid = validated_data.pop('project')

        companion = get_object_or_404(Companion, id=companion_uuid)
        project = get_object_or_404(Project, id=project_uuid)

        # Create the MentorshipRequest object
        mentorship_request = MentorshipRequest.objects.create(
            companion=companion,
            project=project,
            **validated_data
        )

        return mentorship_request
