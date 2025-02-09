from rest_framework import serializers
from project.models import Project, ProjectComment, ProjectRequest
from companion.models import Companion
from mentor.models import Mentor
from user.models import CustomUser

class ProjectSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(many=True, queryset=Companion.objects.all())  # Specify the queryset
    mentor = serializers.PrimaryKeyRelatedField(many=True, queryset=Mentor.objects.all())  

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'leader', 'team', 'mentor', 'file', 'is_active', 'is_deleted']
        

class ProjectListSerializer(serializers.ModelSerializer):
    is_team_member = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'is_active', 'is_team_member']  # Add other necessary fields here

    def get_is_team_member(self, obj):
        user = self.context.get('user')
        # Check if the user is in the project's team
        return user in obj.team.all() if user else False

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with the actual user model if it's not named CustomUser
        fields = ['email', 'first_name', 'last_name']

class CompanionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Companion
        fields = ['user']

class ProjectCommentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    
    class Meta:
        model = ProjectComment
        fields = ['id', 'project', 'comment', 'image', 'file']

class ProjectCommentListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    creator = CustomUserSerializer()

    class Meta:
        model = ProjectComment
        fields = ['id', 'project', 'comment', 'image', 'file', 'date_updated', 'creator']

class ProjectRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequest
        fields = '__all__'

class ProjectRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequest
        fields = ['project','receiver']