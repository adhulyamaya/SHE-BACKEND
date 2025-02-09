from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from user.tasks import send_welcome_email_notification
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    VerifyAccountSerializer,
    ForgotPasswordSerializer,
    SetNewPasswordSerializer
)
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect
from user.utils import send_otp_via_email, send_verification_email, send_reset_password_email
from user.models import CustomUser, Role
from companion.models import Companion
from mentor.models import Mentor
from hr.models import Hr
from market.models import ProjectSeller
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import *
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import smart_bytes
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.template.loader import render_to_string


@api_view(['POST'])
def register_user(request):
    print(request.data)
    if request.method == 'POST':
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            if not user.is_verified:
                # Resend OTP if user exists but is not verified
                try:
                    send_otp_via_email(user.email)
                    return Response(
                        {"message": "User already registered but not verified. OTP resent."},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        {"message": f"An error occurred while resending the OTP: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    {"message": "User already registered and verified."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Attempt to send verification email with OTP
            try:
                send_otp_via_email(user.email)
                return Response(
                    {"message": "Registration successful. Check your email for OTP."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"message": f"An error occurred while sending the OTP: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = CustomUser.objects.get(email=email)
            if user.otp != otp:
                return Response(
                    {"error": "Invalid OTP."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Activate user account
            user.is_registered = True
            user.save()

            return Response(
                {"message": "Account verified successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    print(request.data)
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if 'user' in data:
                return Response(data, status=status.HTTP_200_OK)
            elif 'available_roles' in data:
                return Response(data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get("email")
    user = get_object_or_404(CustomUser, email=email)

    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request=request).domain
        redirect_url = settings.REDIRECT_URL
        reset_url = f"http://{current_site}/api/v1/user/password-reset/{uidb64}/{token}/"
        send_reset_password_email(email=email, reset_url=reset_url, redirect_url=redirect_url)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def password_reset(request, uidb64, token):
    redirect_url = request.query_params.get("redirect_url", "")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        return HttpResponsePermanentRedirect(
            f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}"
        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def set_new_password_api(request):
    try:
        data = request.data
        uidb64 = data.get("uidb64")
        password = data.get("password")

        # Decode the user ID
        id = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)

        # Set the new password
        user.set_password(password)
        user.save()

        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )

    except CustomUser.DoesNotExist:
        return Response(
            {"success": False, "message": "Invalid user ID"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    

@api_view(["GET"])
def get_all_users(request):
    users = CustomUser.objects.filter(is_superuser=False, is_verified=True)
    serializer = UserSerializer(users, many=True)
    response_data = {
        "status_code": 200,
        "title": "User List",
        "data": serializer.data
    }
    return Response(response_data)

@api_view(["GET"])
def get_user_requests(request):
    users = CustomUser.objects.filter(is_superuser=False, is_verified=False)
    serializer = UserSerializer(users, many=True)
    print(users)
    response_data = {
        "status_code": 200,
        "title": "User List",
        "data": serializer.data
    }
    return Response(response_data)
    
@api_view(['PUT'])
def add_role(request):
    user = request.user
    role = request.data.get('role').lower()  # Convert role to lowercase for consistency
    user_roles = [r.name.lower() for r in user.roles.all()]  # Assuming you have a Role model with a 'name' field

    print("User roles:", user_roles)
    
    if not user or not role:
        return Response(
            {"error": "user_id and role are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if role not in user_roles:
            new_role = Role.objects.get(name__iexact=role)  # Assuming 'Role' is the model name
            user.roles.add(new_role)
            user.save()
            return Response(
                {"message": "Role added successfully."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Role already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Role.DoesNotExist:
        return Response(
            {"error": "Role does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
def check_profile_completion(request):
    user = request.user
    role = request.query_params.get('role')
    print(role)

    if role == 'hr':
        profile = Hr.objects.filter(user=user).first()
        print(profile)
    elif role == 'companion':
        profile = Companion.objects.filter(user=user).first()
    elif role == 'mentor':
        profile = Mentor.objects.filter(user=user).first()
    elif role == 'project_seller':
        profile = ProjectSeller.objects.filter(user=user).first()
    else:
        return Response({"error": "Invalid role."}, status=400)

    if profile:
        return Response({"profile_complete": True})
    else:
        return Response({"profile_complete": False})
    
@api_view(['PUT'])
def toggle_block_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = not user.is_active
        user.save()
        status = 'unblocked' if user.is_active else 'blocked'
        roles = user.roles.all()
        for role in roles:
            try:
                if role.name.lower() == 'companion':
                    companion = Companion.objects.get(user=user)
                    companion.is_blocked = not companion.is_blocked
                    companion.save()
                elif role.name.lower() == 'hr':
                    hr = Hr.objects.get(user=user)
                    hr.is_blocked = not hr.is_blocked
                    hr.save()
                elif role.name.lower() == 'mentor':
                    mentor = Mentor.objects.get(user=user)
                    mentor.is_blocked = not mentor.is_blocked
                    mentor.save()
            except ObjectDoesNotExist:
                # If the profile does not exist, skip to the next role
                continue
        return Response({'success': True, 'message': f'User has been {status} successfully.'})
    except Exception as e:
        print(e)
        return Response({'success': False, 'message': str(e)}, status=400)
    
@api_view(['PUT'])
def verify_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        print("user ",user)
        user.is_verified = True
        user.save()

        # Send verification email
        # send_verification_email(user.email)
        # Send welcome email notification to verified users
        subject = 'Welcome to Wompact! Login To Explore !!'
        html_message = render_to_string('email_templates/welcome_email_notification.html', {'user': user})
        plain_message = strip_tags(html_message)  
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        print("to email",to_email)
        print("from email ",from_email)
        # Enqueue the email sending task
        send_welcome_email_notification(subject, plain_message, from_email, to_email, html_message)   

        return Response({'success': True, 'message': 'User has been verified and notified successfully.'})
    except Exception as e:
        print("mail error ",e)
        return Response({'success': False, 'message': str(e)}, status=HTTP_400_BAD_REQUEST) # type: ignore