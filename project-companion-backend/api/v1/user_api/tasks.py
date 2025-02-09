from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives

logger = get_task_logger(__name__)

logger.info("Starting tasks.py...")

@shared_task(name='send_welcome_email_notification')
def send_welcome_email_notification(subject, plain_message, from_email, to_email, html_message):
    logger.info("Entered send_welcome_email_notification task.")
    logger.info(f"Parameters - subject: {subject}, from_email: {from_email}, to_email: {to_email}")
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        logger.info(f"Email object created: {email}")

        email.attach_alternative(html_message, "text/html")
        email.send()
        logger.info("Email sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}", exc_info=True)  # Log the stack trace
        return False
