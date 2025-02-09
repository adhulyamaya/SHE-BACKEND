from django.db import models
from main.models import BaseModel
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


DOMAIN_CHOICES = (
    ('Python', "Python"),
    ('MERN',"MERN"),
    ('Java',"Java"),
    ('Other', "Other")    
)

class Companion(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country = models.ForeignKey("main.Country", on_delete=models.CASCADE)
    state = models.ForeignKey("main.State", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/companion/', blank=True, null=True)
    bio = models.TextField(_("Bio/Introduction"), blank=True, null=True)
    phone = models.CharField(_("Phone Number with country code"), max_length=126, blank=True, null=True)
    git_hub = models.URLField(_("GitHub Profile Url"),max_length=255, blank=True, null=True)    
    linked_in = models.URLField(_("Linked In Profile Url"),max_length=255, blank=True, null=True)
    experience = models.TextField(_("Experience in years"),blank=True, null=True)  
    domain = models.CharField(_('Domain'),choices=DOMAIN_CHOICES,max_length=125,null=True, blank=True)
    skills = models.TextField(_("Skills"),blank=True, null=True)
    qualification = models.CharField(_("Qualification"),max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)    
    is_deleted = models.BooleanField(_("Is this companion deleted ?"),default=False)
    is_blocked = models.BooleanField(_("Is this companion blocked ?"),default=False)

    class Meta:
        db_table = 'companion_companion'
        verbose_name = _('companion')
        verbose_name_plural = _('companions')    

    def __str__(self):
        return f'{self.user.email}'
    
