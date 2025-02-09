from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import BaseModel
from user.models import CustomUser
from companion.models import Companion
from mentor.models import Mentor


class Hr(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(_("Company Name"), max_length=255)
    country = models.ForeignKey("main.Country", on_delete=models.CASCADE)
    state = models.ForeignKey("main.State", on_delete=models.CASCADE)
    phone = models.CharField(_("Phone Number with country code"), max_length=126, blank=True, null=True)
    linked_in = models.URLField(_("Linked In Profile Url"), max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/hr/', blank=True, null=True)
    rating = models.FloatField(_("Rating"), default=0.0, blank=True, null=True)
    is_deleted = models.BooleanField(_("Is this HR deleted?"), default=False)
    is_blocked = models.BooleanField(_("Is this HR blocked?"), default=False)

    class Meta:
        db_table = 'hr_hr'
        verbose_name = _('HR')
        verbose_name_plural = _('HRs')

    def __str__(self):
        return f'{self.user.email}'
    

class JobPost(BaseModel):
    hr = models.ForeignKey(Hr, on_delete=models.CASCADE)
    title = models.CharField(_("Job Title"), max_length=255)
    description = models.TextField(_("Job Description"), blank=True, null=True)
    salary_from = models.DecimalField(_("Salary Range From"), max_digits=10, decimal_places=2, blank=True, null=True)
    salary_to = models.DecimalField(_("Salary Range To"), max_digits=10, decimal_places=2, blank=True, null=True)
    experience = models.IntegerField(_("Experience Required in years"), blank=True, null=True)
    skills = models.CharField(_("Skills"), max_length=255)
    company = models.CharField(_("Hiring Company Name"), max_length=255)
    location = models.CharField(_("Job Location"), max_length=255, default='Remote')
    is_deleted = models.BooleanField(_("Is this Job deleted?"), default=False)
    # is_blocked = models.BooleanField(_("Is this Job blocked?"), default=False)

    class Meta:
        db_table = 'hr_job_post'
        verbose_name = _('job_post')
        verbose_name_plural = _('job_posts')

    def __str__(self):
        return str(self.title)
    

class JobOffer(BaseModel):
    hr = models.ForeignKey(Hr, on_delete=models.CASCADE)
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE, blank=True, null=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=True, null=True)
    salary_offer = models.DecimalField(_("Salary Offered"), max_digits=10, decimal_places=2, blank=True, null=True)
    offer_date = models.DateField(_("Offer Date"), auto_now_add=True)
    is_accepted = models.BooleanField(_("Is Offer Accepted?"), default=False)
    is_rejected = models.BooleanField(_("Is Offer Rejected?"), default=False)

    class Meta:
        db_table = 'hr_job_offer'
        verbose_name = _('job offer')
        verbose_name_plural = _('job offers')

    def __str__(self):
        return f'{self.job.title if self.job else "No Job"} - {self.hr.user.email}'
    
    
class JobPostApplication(BaseModel):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_jobapplication'
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f'{self.companion.user} applied for {self.job.title}'