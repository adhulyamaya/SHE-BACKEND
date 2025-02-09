from django.db import models
from companion.models import DOMAIN_CHOICES
from main.models import BaseModel
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


CONTRIBUTOR_TASK_CHOICES = (
    ('completed', 'Completed'),
    ('missed_deadline', 'Missed Deadline'),
    ('not_started', 'Not Started'),
    ('not_completed', 'Not Completed')
)

UNIT_CHOICES = (
    ('percentage', '%'),
    ('rupees', 'Rupees')    
)

class Contributor(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country = models.ForeignKey("main.Country", on_delete=models.CASCADE,blank=True, null=True)
    state = models.ForeignKey("main.State", on_delete=models.CASCADE,blank=True, null=True)
    photo = models.ImageField(upload_to='photos/contributor/', blank=True, null=True)
    bio = models.TextField(_("Bio/Introduction"), blank=True, null=True)
    phone = models.CharField(_("Phone Number with country code"),max_length=126,blank=True, null=True)
    git_hub = models.URLField(_("GitHub Profile Url"),max_length=255, blank=True, null=True)    
    linked_in = models.URLField(_("Linked In Profile Url"),max_length=255, blank=True, null=True)
    experience = models.TextField(_("Experience in years"),blank=True, null=True)    
    domain = models.CharField(_('Domain'),choices=DOMAIN_CHOICES,max_length=125,null=True, blank=True)
    skills = models.TextField(_("Skills"),blank=True, null=True)
    qualification = models.CharField(_("Qualification"),max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)    
    is_deleted = models.BooleanField(_("Is this contributor deleted ?"),default=False)
    is_blocked = models.BooleanField(_("Is this contributor blocked ?"),default=False)

    class Meta:
        db_table = 'contributor_contributor'
        verbose_name = _('contributor')
        verbose_name_plural = _('contributors')    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Task(BaseModel):
    name = models.CharField(max_length=255)
    weightage = models.FloatField(default=3.0)
    unit = models.CharField(_('Unit'),choices=UNIT_CHOICES,default='percentage',max_length=125)
    is_deleted = models.BooleanField(_("Is this task deleted ?"),default=False)

    def __str__(self):
        return self.name

class ContributorTask(BaseModel):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)    
    status = models.CharField(_('Status'),choices=CONTRIBUTOR_TASK_CHOICES,default='not_started',max_length=125)
    weightage_after_deadline = models.FloatField(default=20.0)  # to calculate weightage after deadlines
    first_deadline = models.DateField()
    second_deadline = models.DateField(null=True, blank=True)  # Optional for future tasks
    net_weightage = models.FloatField(default=00.0)
    is_deleted = models.BooleanField(_("Is this contributor task deleted ?"),default=False)

    def __str__(self):
        return f"{self.contributor} - {self.task.name}"
    
