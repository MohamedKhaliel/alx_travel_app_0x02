from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from django.urls import path, include
from listings import views


router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns = [
    path("api/payment/initiate/", views.initiate_payment, name="initiate_payment"),
    path("api/payment/verify/", views.verify_payment, name="verify_payment"),
]
