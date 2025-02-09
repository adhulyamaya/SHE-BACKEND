from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser

def send_otp_via_email(email):
    subject = "Your account verification email"
    otp = random.randint(100000, 999999)
    print(otp)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, email_from, [email], fail_silently=False)
        user_obj = CustomUser.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()
    except CustomUser.DoesNotExist:
        raise ValueError(f"No user found with email {email}")
    except Exception as e:
        raise RuntimeError(f"Error sending OTP email to {email}: {str(e)}")
    
def send_verification_email(user_email):
    subject = 'Account Verified Successfully'
    login_link = 'http://127.0.0.1:3000/#/login'  # Update this link as per your environment
    message = f'Your account at Project Companion has been verified successfully. You can now login with your credentials. Click the following link to login: {login_link}'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )


def send_reset_password_email(email, reset_url, redirect_url):
    subject = "Your password reset email"
    message = (
        "Click the following link to reset your password\n"
        + reset_url
        + "?redirect_url="
        + redirect_url
    )
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)
