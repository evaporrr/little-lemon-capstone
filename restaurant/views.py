from django.shortcuts import render
from rest_framework import generics, permissions, viewsets

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


def index(request):
    """Serve the static HTML home page."""
    return render(request, "index.html")


class MenuItemsView(generics.ListCreateAPIView):
    """GET: list menu items (public). POST: add an item (login required)."""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET (public), PUT/PATCH/DELETE (login required) for one menu item."""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Table bookings: every method requires a valid token."""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
