from django.urls import path
from api.v1.contributor_api import views

app_name = 'contributor_api'

urlpatterns = [
    path('contributors/', views.contributors, name='contributors'),
    path('contributor/create/', views.create_contributor, name='create_contributor'),
    path("contributor/view/<uuid:pk>/", views.contributor, name="contributor"),
    path('contributor/edit/<uuid:pk>/', views.edit_contributor, name='edit_contributor'),
    path("contributor/delete/<uuid:pk>/", views.delete_contributor, name="delete_contributor"),
    
    path('tasks/', views.tasks, name='tasks'),
    path('task/create/', views.create_task, name='create_task'),
    path("task/view/<uuid:pk>/", views.task, name="task"),
    path('task/edit/<uuid:pk>/', views.edit_task, name='edit_task'),
    path("task/delete<uuid:pk>/", views.delete_task, name="delete_task"),
    
    path('contributor-tasks/', views.contributor_tasks, name='contributor_tasks'),
    path('contributor-task/create/', views.create_contributor_task, name='create_contributor_task'),
    path("contributor-task/view/<uuid:pk>/", views.contributor_task, name="contributor_task"),
    path('contributor-task/edit/<uuid:pk>/', views.edit_contributor_task, name='edit_contributor_task'),
    path("contributor-task/delete/<uuid:pk>/", views.delete_contributor_task, name="delete_contributor_task"),
    path("status-choices/", views.get_status_choices, name="status_choices"),
    path("unit-choices/", views.get_unit_choices, name="unit_choices")
]