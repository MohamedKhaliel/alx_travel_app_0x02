from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

import os, requests, uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Payment


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer



CHAPA_SECRET_KEY = settings.CHAPA_SECRET_KEY
CHAPA_BASE_URL = settings.CHAPA_BASE_URL

headers = {
    "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
}

# Initiate payment
@api_view(["POST"])
def initiate_payment(request):
    booking_reference = request.data.get("booking_reference")
    amount = request.data.get("amount")

    tx_ref = str(uuid.uuid4())  # unique transaction id

    payload = {
        "amount": amount,
        "currency": "ETB",
        "email": "customer@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "tx_ref": tx_ref,
        "callback_url": "http://localhost:8000/api/payment/verify/",
        "return_url": "http://localhost:8000/payment/success/"
    }

    response = requests.post(
        f"{CHAPA_BASE_URL}/transaction/initialize",
        json=payload,
        headers=headers
    )
    data = response.json()

    if data.get("status") == "success":
        Payment.objects.create(
            booking_reference=booking_reference,
            transaction_id=tx_ref,
            amount=amount,
            status="Pending"
        )
        return Response({"checkout_url": data["data"]["checkout_url"], "tx_ref": tx_ref})
    else:
        return Response({"error": "Payment initiation failed"}, status=400)


# Verify payment
@api_view(["GET"])
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")

    response = requests.get(
        f"{CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
        headers=headers
    )
    data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    if data.get("status") == "success" and data["data"]["status"] == "success":
        payment.status = "Completed"
        payment.save()
        return Response({"message": "Payment successful", "status": "Completed"})
    else:
        payment.status = "Failed"
        payment.save()
        return Response({"message": "Payment failed", "status": "Failed"}, status=400)
