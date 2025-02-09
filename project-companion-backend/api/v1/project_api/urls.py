from django.urls import path
from rest_framework.routers import DefaultRouter
from api.v1.project_api import views
import uuid


app_name='project_api'

urlpatterns = [
    path('projects/',views.projects, name='projects'),
    path('my_projects/',views.my_projects, name='my_projects'),
    path('project/create/',views.create_project,name='create_project'),
    path('project/view/<uuid:pk>/',views.project,name='project'),
    path('project/edit/<uuid:pk>/',views.edit_project,name='edit_project'),
    path('project/delete/<uuid:pk>/',views.delete_project,name='deleteproject'),

    # Project Comment URLs
    path('<uuid:pk>/comments/', views.project_comments, name='project_comments'),  # Fetch comments for a specific project
    path('comment/create/', views.create_project_comment, name='create_project_comment'),
    path('comment/edit/<uuid:pk>/', views.edit_project_comment, name='edit_project_comment'),
    path('comment/delete/<uuid:pk>/', views.delete_project_comment, name='delete_project_comment'),
    path('comment/<uuid:pk>/', views.project_comment, name='project_comment'),

    # Project Request URLs
    path('project/requests/', views.list_project_requests, name='project_requests'),
    path('project/requests/<int:receiver_id>/', views.list_project_requests_for_receiver, name='list_project_requests_for_receiver'),
    path('project/request/create/', views.send_project_request, name='create_project_request'),
    path('project/request/accept/<uuid:pk>/', views.respond_to_project_request, name='accept_project_request'),
]