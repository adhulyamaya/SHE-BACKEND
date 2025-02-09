from decimal import Decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey("user.CustomUser",blank=True,related_name="creator_%(class)s_objects",on_delete=models.CASCADE)
    updator = models.ForeignKey("user.CustomUser",blank=True,related_name="updator_%(class)s_objects",on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)    
    date_updated = models.DateTimeField(auto_now_add=True) 

    class Meta:
        abstract = True
        

class Country(models.Model):
    name = models.CharField(max_length=128)
    iso3 = models.CharField(max_length=128)
    iso2 = models.CharField(max_length=128)
    numeric_code = models.CharField(max_length=128)
    phone_code = models.CharField(max_length=128)
    capital = models.CharField(max_length=128)
    currency = models.CharField(max_length=128)
    currency_symbol = models.CharField(max_length=128)
    tld = models.CharField(max_length=128)
    native = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    subregion = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'countries'
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self): 
        return "%s" %(self.name)


class State(models.Model):
    country = models.ForeignKey('main.Country',on_delete=models.CASCADE,)
    name = models.CharField(max_length=128)
    country_code = models.CharField(max_length=128)
    state_code = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'states'
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __str__(self): 
        return "%s" %(self.name)

