from rest_framework import serializers
from user.models import CustomUser, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'is_superuser', 'date_joined', 'roles', 'is_active', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    roles = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'roles']

    def create(self, validated_data):
        password = validated_data.pop('password')
        roles_data = validated_data.pop('roles')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=password,
        )

        roles = Role.objects.filter(name__in=roles_data)
        user.roles.set(roles)
        user.save()
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the roles from a list of Role objects to a list of role names
        representation['roles'] = [role.name for role in instance.roles.all()]
        return representation

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "redirect_url"]

from rest_framework import serializers

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        uidb64 = attrs.get("uidb64")

        try:
            # Decode the user ID
            id = force_str(urlsafe_base64_decode(uidb64))
            print(f"Decoded ID: {id}")
            user = CustomUser.objects.get(id=id)
            print(f"Fetched User: {user.email}")
            user.set_password(password)
            user.save()

            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")
        except Exception as e:
            raise serializers.ValidationError(f"Error: {e}")



class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(_("Must include 'email', and 'password'."))

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_registered or not user.is_verified:
                raise serializers.ValidationError(_("Account is not registered or verified."))

            roles = [role.name for role in user.roles.all()]

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Construct and return response data
            data = {
                'refresh': str(refresh),
                'access': str(access),
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_superuser': user.is_superuser,
                    'date_joined': user.date_joined,
                    'roles': roles  # List of roles assigned to the user
                }
            }
            update_last_login(None, user)
            return data
            
        else:
            raise serializers.ValidationError(_("No active account found with the given credentials."))