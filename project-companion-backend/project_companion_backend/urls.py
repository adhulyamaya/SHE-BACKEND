from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/job/', include(('api.v1.job_api.urls'),namespace='job_api')),
    path('api/v1/user/', include(('api.v1.user_api.urls'),namespace='user_api')),
    path('api/v1/mentor/', include(('api.v1.mentor_api.urls'),namespace='mentor_api')),
    path('api/v1/companion/', include(('api.v1.companion_api.urls'),namespace='companion_api')),
    path('api/v1/contributor/', include(('api.v1.contributor_api.urls'),namespace='contributor_api')),
    path('api/v1/project/', include(('api.v1.project_api.urls'),namespace='project_api')),
    path('api/v1/main/', include(('api.v1.main_api.urls'),namespace='main_api')),
    path('api/v1/event/', include(('api.v1.event_api.urls'),namespace='event_api')),
    path('api/v1/hr/', include(('api.v1.hr_api.urls'),namespace='hr_api')),
    path('api/v1/market/', include(('api.v1.market_api.urls'),namespace='market_api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
