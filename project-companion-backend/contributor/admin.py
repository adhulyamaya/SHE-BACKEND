from django.contrib import admin
from contributor.models import Contributor, ContributorTask, Task
# Register your models here.

admin.site.register(Contributor)
admin.site.register(Task)
admin.site.register(ContributorTask)