from django.urls import include,path,re_path
from rest_framework.routers import DefaultRouter
from api.v1.job_api import views

app_name = 'job_api'

urlpatterns = [
    path('jobs/', views.jobs, name='jobs'),
    path('job/create/', views.create_job, name='create_job'),
    path("job/view/<uuid:pk>/", views.job, name="job"),
    path('job/edit/<uuid:pk>/', views.edit_job, name='edit_job'),
    path("job/delete/<uuid:pk>/", views.delete_job, name="delete_job"),

    path('job/application/create/', views.apply_job, name='apply_for_job'),
    path('job/application/change-status/<uuid:pk>/', views.manage_application_status, name='manage_application_status'),
    path('job/<uuid:job_id>/applications/', views.list_applications_for_job, name='list_applications_for_job'),
    path('companion/<int:companion_id>/applications/', views.list_applications_by_companion, name='list_applications_by_companion'),
]