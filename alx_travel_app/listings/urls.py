from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
