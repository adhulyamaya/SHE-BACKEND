
from datetime import date
from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError




class Project(BaseModel):
    name = models.CharField(_("Project Name"), max_length=255)
    description = models.TextField(_("Description "), blank=True, null=True)
    start_date = models.DateField(_('Start Date'),help_text='start date', default=date.today)
    end_date = models.DateField(_('End Date'),help_text='end date', blank=True, null=True)
    leader = models.CharField(_("Project Leader"),max_length=255, blank=True, null=True)
    team = models.ManyToManyField("companion.Companion", verbose_name=_("Team"), blank=True)
    mentor = models.ManyToManyField("mentor.Mentor", verbose_name=_("Mentor"), blank=True)    
    file = models.FileField(upload_to='files/projects/', blank=True, null=True)
    is_active = models.BooleanField(_("Is this project active ?"),default=True)
    is_deleted = models.BooleanField(_("Is this project deleted ?"),default=False)

    class Meta:
        db_table = 'project_project'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
    
    def __str__(self):
        return self.name


class ProjectComment(BaseModel):
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False})
    companion = models.ForeignKey("companion.Companion", on_delete=models.CASCADE, limit_choices_to={'is_deleted': False}, null=True, blank=True)
    comment = models.TextField(_("Comment "), blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to='images/projects/comments/', blank=True, null=True)
    file = models.FileField(upload_to='projects/comments/files/', blank=True, null=True)
    is_deleted = models.BooleanField(_("Is this project comment deleted ?"), default=False)

    class Meta:
        db_table = 'project_project_comment'
        verbose_name = _('Project Comment')
        verbose_name_plural = _('Project Comments')

    def __str__(self):
        return str(self.comment) if self.comment else 'No Comment'

    def clean(self):
        super().clean()
        # Ensure at least one of comment, image, or file is provided
        if not (self.comment or self.image or self.file):
            raise ValidationError(_("At least one of 'comment', 'image', or 'file' must be provided."))

    def save(self, *args, **kwargs):
        self.clean()  # Call clean method to validate before saving
        super().save(*args, **kwargs)
    

class ProjectRequest(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sender = models.ForeignKey("companion.Companion", related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey("companion.Companion", related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="pending")

    class Meta:
        db_table = 'project_request'
        verbose_name = _('Project Request')
        verbose_name_plural = _('Project Requests')

    def __str__(self):
        return f"Request from {self.sender} to {self.receiver} for project {self.project.name}"