from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

proxy_service_name = 'user-management'

urlpatterns = [
    path(f'api/{proxy_service_name}/admin/', admin.site.urls),
    path(f'api/{proxy_service_name}/auth/', include('authentications.urls')),
    path(f'api/{proxy_service_name}/users/', include('users.urls')),
    path(f'api/{proxy_service_name}/activities/', include('activities.urls')),
    path(f'api/{proxy_service_name}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'api/{proxy_service_name}/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'api/{proxy_service_name}/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
