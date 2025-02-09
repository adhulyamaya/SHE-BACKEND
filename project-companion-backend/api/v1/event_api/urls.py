from django.urls import path
from api.v1.event_api import views

app_name = 'event_api'

urlpatterns = [
    path('events/', views.allEvents, name='events'),
    path('my-events/', views.myEvents, name='my-events'),
    path('event/create/', views.create_event, name='create_event'),
    path("event/view/<uuid:pk>/", views.event, name="event"),
    path('event/edit/<uuid:pk>/', views.edit_event, name='edit_event'),
    path("event/delete/<uuid:pk>/", views.delete_event, name="delete_event"),
    
    path('eventRegistrations/', views.event_registrations, name='event-registration'),
    path('eventRegistration/create/', views.create_event_registration, name='event-registration-create'),
    path("eventRegistration/view/<uuid:pk>/", views.event_registration, name="event-registration-view"),
    path("eventRegistration/cancel/<uuid:pk>/", views.cancel_event_registration, name="event-registration-cancel")
]