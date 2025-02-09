from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from contributor.models import Contributor,CustomUser, Task, ContributorTask


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','roles']


class ContributorSerializer(ModelSerializer):
    user = UserSerializer()  # Nest the UserSerializer to include first_name, last_name, email

    class Meta:
        model = Contributor
        exclude = ['creator', 'updator', 'is_deleted','is_blocked']
        read_only_fields = ['user']


class ContributorCreateSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'creator', 'updator']
        
class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','name', 'weightage', 'unit']

class ContributorTaskSerializer(ModelSerializer):
    contributor = ContributorSerializer()
    task = TaskSerializer()

    class Meta:
        model = ContributorTask
        fields = ['contributor', 'task', 'status', 'first_deadline', 'second_deadline', 'net_weightage', 'weightage_after_deadline']       

class StatusChoicesSerializer(Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()
    

class UnitChoicesSerializer(Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()