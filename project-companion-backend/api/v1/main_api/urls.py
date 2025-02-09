from django.urls import path
from api.v1.main_api import views

app_name = 'main_api'

urlpatterns = [
    path('dashboard/main', views.main_dashboard, name='main_dashboard'),
    path('countries', views.countries, name='countries'),
    path('states', views.states, name='states'),
    path('get_states/', views.get_states, name='get_states')
    
]