from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from companion.models import Companion,CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','roles']
        
class CompanionSerializer(ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Companion
        exclude = ['creator', 'updator', 'is_deleted','is_blocked']
        read_only_fields = ['user']


class DomainChoicesSerializer(Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()