from django.urls import path
from api.v1.hr_api import views

app_name = 'hr_api'

urlpatterns = [
    path('hrs/', views.hrs, name='hrs'),
    path('hr/create/', views.create_hr, name='create_hr'),
    path("hr/view/", views.hr, name="hr"),
    path('hr/edit/', views.edit_hr, name='edit_hr'),
    path("hr/delete/<uuid:pk>/", views.delete_hr, name="delete_hr"),
    
    path('all-job-posts/', views.all_job_posts, name='all_job_posts'),
    path('job-posts/', views.job_posts, name='job_posts'),
    path('job-post/create/', views.create_job_post, name='create_job_post'),
    path("job-post/view/<uuid:pk>/", views.job_post, name="job_post"),
    path('job-post/edit/<uuid:pk>/', views.edit_job_post, name='edit_job_post'),
    path("job-post/delete/<uuid:pk>/", views.delete_job_post, name="delete_job_post"),
    # path('job-post/block-job/<uuid:pk>/', views.toggle_block_job, name='block_job'),
    
    path('job-apply/', views.apply_for_job, name='apply_for_job'),
    path('jobs-applicants/<uuid:pk>/', views.job_applicants_list, name='job-applicants'),
    path('my-applications/', views.user_job_applications_list, name='user-job-applications'),

]