from django.db import models
from main.models import BaseModel
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ProjectSeller(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country = models.ForeignKey("main.Country", on_delete=models.CASCADE)
    state = models.ForeignKey("main.State", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/seller/', blank=True, null=True)
    bio = models.TextField(_("Bio/Introduction"), blank=True, null=True)
    phone = models.CharField(_("Phone Number with country code"), max_length=126, blank=True, null=True)
    git_hub = models.URLField(_("GitHub Profile Url"), max_length=255, blank=True, null=True)
    linked_in = models.URLField(_("LinkedIn Profile Url"), max_length=255, blank=True, null=True)
    skills = models.TextField(_("Skills"), blank=True, null=True)
    is_deleted = models.BooleanField(_("Is this seller deleted?"), default=False)
    is_blocked = models.BooleanField(_("Is this seller blocked?"), default=False)

    class Meta:
        db_table = 'project_seller'
        verbose_name = _('project seller')
        verbose_name_plural = _('project sellers')

    def __str__(self):
        return f'{self.user.email}'


class MarketplaceProject(BaseModel):
    seller = models.ForeignKey("ProjectSeller", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    tech_stack = models.CharField(max_length=255)
    demo_link = models.URLField(blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'marketplace_project'
        verbose_name = _('marketplace project')
        verbose_name_plural = _('marketplace projects')

    def __str__(self):
        return self.title


class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(MarketplaceProject, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'marketplace_order'
        verbose_name = _('marketplace order')
        verbose_name_plural = _('marketplace orders')

    def __str__(self):
        return f"Order {self.id} - {self.project.title}"
