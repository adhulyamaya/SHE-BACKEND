from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from user.models import CustomUser

logger = get_task_logger(__name__)

logger.info("Starting tasks.py...")

@shared_task(name='send_welcome_email_notification')
def send_welcome_email_notification(subject, plain_message, from_email, to_email, html_message):
    logger.info("Entered send_welcome_email_notification task.")
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        logger.info(f"Email object created with subject: {subject} and to_email: {to_email}")
        
        email.attach_alternative(html_message, "text/html")
        email.send()
        logger.info("Email sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False
    
    
@shared_task(name='send_bulk_comment_notification')
def send_bulk_comment_notification(recipients, subject, companion_username, project, comment, project_url, comment_added_by):
    logger.info("Entered send_bulk_comment_notification task.")
    try:
        for recipient in recipients:
            context = {
                'companion_username': companion_username,
                'project': project,
                'comment': comment,
                'project_url': project_url,
                'comment_added_by':comment_added_by
            }

            html_message = render_to_string('email_templates/comment_notification.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            logger.info(f"Notification sent to {recipient}.")
        return True
    except Exception as e:
        logger.error(f"Error sending bulk notifications: {e}")
        return False
