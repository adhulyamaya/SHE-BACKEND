from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import BaseModel
from user.models import CustomUser




class Event(BaseModel):
    title = models.CharField(_("Event Title"), max_length=255)
    description = models.TextField(_("Event Description"), blank=True, null=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizer')
    event_date = models.DateField(_("Event Date"))
    event_time = models.TimeField(_("Event Time"))
    duration = models.DurationField(_("Event Duration"), blank=True, null=True)
    venue = models.CharField(_("Event Venue"), max_length=255, blank=True, null=True)
    is_online = models.BooleanField(_("Is Online Event?"), default=False)
    url = models.URLField(_("Event URL"), max_length=255, blank=True, null=True)
    is_completed = models.BooleanField(_("Is Event Completed?"), default=False)
    is_deleted = models.BooleanField(_("Is Event want to Deleted?"), default=False)
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    
    class Meta:
        db_table = 'event_event'
        verbose_name = _('event event')
        verbose_name_plural = _('event events')
    
    def __str__(self):
        return self.title
    

class EventRegistration(BaseModel):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name='event_registrations')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_registrations')
    registration_date = models.DateTimeField(_("Registration Date"), auto_now_add=True)
    is_attended = models.BooleanField(_("Did User Attend?"), default=False)
    is_cancel = models.BooleanField(_("Are you to cancel?"), default=False)
    
    class Meta:
        db_table = 'event_registration'
        verbose_name = _('event registration')
        verbose_name_plural = _('event registrations')
    
    def __str__(self):
        return f'{self.user.email} - {self.event.title}'
