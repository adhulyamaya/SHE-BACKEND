from django.urls import path
from api.v1.companion_api import views

app_name = 'companion_api'

urlpatterns = [
    path('companions/', views.companions, name='companions'),
    path('companion/create/', views.create_companion, name='create_companion'),
    path("companion/view/", views.companion, name="companion"),
    path('companion/edit/', views.edit_companion, name='edit_companion'),
    path("companion/delete/<uuid:pk>/", views.delete_companion, name="delete_companion"),
    path("domain-choices/", views.get_domain_choices, name="domain_choices"),
]