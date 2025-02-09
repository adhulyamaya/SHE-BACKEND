from django.db import models
from main.models import BaseModel
from user.models import CustomUser
from project.models import Project
from companion.models import Companion
from django.utils.translation import gettext_lazy as _




PAYMENT_CHOICES = [
        ('paid', 'Paid'),
        ('free', 'Free'),
    ]


class Mentor(BaseModel):  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    country = models.ForeignKey("main.Country", on_delete=models.CASCADE)
    state = models.ForeignKey("main.State", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/mentor/', blank=True, null=True)
    bio = models.TextField(_("Bio/Introduction"), blank=True, null=True)
    phone = models.CharField(_("Phone Number with country code"),max_length=15)
    git_hub = models.URLField(_("GitHub Profile Url"), max_length=255, blank=True, null=True)
    linked_in = models.URLField(_("Linked In Profile Url"), max_length=255, blank=True, null=True)
    experience = models.IntegerField(_("Experience in years"), blank=True, null=True)
    domain = models.CharField(_("Domain"), max_length=255, blank=True, null=True)
    payment_method = models.CharField(_("Paid/Free Mentorship ?"), max_length=126, choices=PAYMENT_CHOICES, default='free')
    rating = models.FloatField(_("Rating"), default=0.0, blank=True, null=True)
    feedback = models.TextField(_("Feedback"), blank=True, null=True)
    is_deleted = models.BooleanField(_("Is this mentor deleted ?"), default=False)
    is_blocked = models.BooleanField(_("Is this mentor blocked ?"), default=False)

    class Meta:
        db_table = 'mentor_mentor'
        verbose_name = _('mentor')
        verbose_name_plural = _('mentors')    

    def __str__(self):
        return f"{self.user.email}"
    
class MentorshipRequest(BaseModel):
    companion = models.ForeignKey("companion.Companion", on_delete=models.CASCADE, related_name="mentorship_requests")
    mentor = models.ForeignKey("Mentor", on_delete=models.CASCADE, related_name="received_requests")
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, related_name="mentorship_requests")
    request_date = models.DateTimeField(_("Request Date"), auto_now_add=True)
    status = models.CharField(_("Request Status"), max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    message = models.TextField(_("Message to Mentor"), blank=True, null=True)

    class Meta:
        db_table = 'mentorship_request'
        verbose_name = _('mentorship request')
        verbose_name_plural = _('mentorship requests')

    def __str__(self):
        return f"Request from {self.companion.user.email} to {self.mentor.user.email} for {self.project.title}"