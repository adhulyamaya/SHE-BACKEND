from django.core.management.base import BaseCommand
from user.models import Role
from rest_framework.permissions import BasePermission


class Command(BaseCommand):
    help = 'Create initial roles'

    def handle(self, *args, **kwargs):
        Role.objects.get_or_create(name='companion')
        Role.objects.get_or_create(name='mentor')
        Role.objects.get_or_create(name='hr')
        Role.objects.get_or_create(name='contributor')
        Role.objects.get_or_create(name='project_seller')
        # Role.objects.get_or_create(name='project_team_member')
        self.stdout.write(self.style.SUCCESS('Roles created successfully'))


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='mentor').exists()

class IsCompanion(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='companion').exists()

class IsHr(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='hr').exists()
    
class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='contributor').exists()
    
class IsProjectSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='project_seller').exists()
    
# class IsProjectTeamMember(BasePermission):
#     def has_permission(self, request, view):
#         # Checks if the user has a role 'project_team_member'
#         return request.user.roles.filter(name='project_team_member').exists()