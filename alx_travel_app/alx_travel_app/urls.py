from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),  # Include your API routes
]



schema_view = get_schema_view(
   openapi.Info(
      title="Travel API",
      default_version='v1',
      description="API documentation for Listings and Bookings",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
