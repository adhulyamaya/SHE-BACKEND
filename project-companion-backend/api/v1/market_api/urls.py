from django.urls import path
from . import views

app_name = 'market_api'

urlpatterns = [
    path('projectsellers/', views.projectseller_list, name='projectsellers'),
    path('projectseller/create/', views.projectseller_create, name='create_projectseller'),
    path("projectseller/view/", views.projectseller_detail, name="projectseller"),
    path('projectseller/edit/', views.projectseller_update, name='edit_projectseller'),
    path("projectseller/delete/<uuid:pk>/", views.projectseller_delete, name="delete_projectseller"),

    path('marketplace-projects/', views.marketplace_projects, name='marketplace_projects'),
    path('marketplace-project/create/', views.create_marketplace_project, name='create_marketplace_project'),
    path('marketplace-project/view/<uuid:pk>/', views.view_marketplace_project, name='view_marketplace_project'),
    path('marketplace-project/edit/<uuid:pk>/', views.edit_marketplace_project, name='view_marketplace_project'),
    path('marketplace-project/delete/<uuid:pk>/', views.delete_marketplace_project, name='delete_marketplace_project'),
    path('seller/projects/', views.seller_marketplace_projects, name='seller_marketplace_projects'),
    path('marketplace-project/create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('marketplace-project/verify-payment/', views.VerifyPaymentView.as_view(), name='verify-payment'),
    path('marketplace-project/purchase-history/', views.PurchaseHistoryView.as_view(), name='purchase-history'),
]
