from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from main.models import BaseModel

class Job(BaseModel):
    title = models.CharField(_("Job Title"),max_length=255)
    description = models.TextField(_("Job Description"), blank=True, null=True)
    salary_from = models.DecimalField(_("Salary Range From"),max_digits=10, decimal_places=2, blank=True, null=True)
    salary_to = models.DecimalField(_("Salary Range To"),max_digits=10, decimal_places=2, blank=True, null=True)
    experience = models.IntegerField(_("Experience Required in years"), blank=True, null=True)
    skills = models.CharField(_("Skills"),max_length=255)
    company = models.CharField(_("Hiring Company Name"),max_length=255)
    is_deleted = models.BooleanField(_("Is this Job deleted ?"),default=False)

    class Meta:
        db_table = 'job_job'
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        ordering = ['date_added']
    
    def __str__(self):
        return str(self.title)
    

class JobApplication(BaseModel):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('on_hold', 'On Hold'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(_("Application Status"), max_length=50, choices=STATUS_CHOICES, default='applied')
    is_deleted = models.BooleanField(_("Is this application deleted?"), default=False)

    class Meta:
        db_table = 'job_application'
        verbose_name = _('job application')
        verbose_name_plural = _('job applications')
    
    def __str__(self):
        return f"{self.applicant.email} - {self.job.title}"