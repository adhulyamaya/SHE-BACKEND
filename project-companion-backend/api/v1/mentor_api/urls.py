from django.urls import path
from api.v1.mentor_api import views

app_name = 'mentor_api'

urlpatterns = [

    path('mentors/', views.mentors, name='mentors'),
    path('mentor/create/', views.create_mentor, name='create_mentor'),
    path('mentor/view/', views.mentor, name='mentor'),
    path('mentor/edit/', views.edit_mentor, name='edit_mentor'),
    path('mentor/delete/<uuid:pk>/', views.delete_mentor, name='delete_mentor'),
    path('mentor/send_request/', views.send_mentorship_request, name='request_mentorship'),
    path('mentor/requests/', views.get_mentorship_requests, name='get_mentorship_requests'),
    path('mentor/requests/check/', views.check_request_exists, name='check_request_exists'),
    path('mentor/handle_request/<uuid:pk>/', views.handle_mentorship_request, name='handle_mentorship_request'),

]