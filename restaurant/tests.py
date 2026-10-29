from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu
from .serializers import MenuSerializer


class ModelTests(TestCase):
    def test_menu_str(self):
        item = Menu.objects.create(title="IceCream", price=Decimal("80.00"), inventory=100)
        self.assertEqual(str(item), "IceCream : 80.00")

    def test_booking_str(self):
        booking = Booking.objects.create(
            name="Ana", no_of_guests=4,
            booking_date=datetime(2026, 11, 1, 19, 30, tzinfo=timezone.utc),
        )
        self.assertEqual(str(booking), "Ana (4) on 2026-11-01 19:30")


class MenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("chef", password="Lemon#2026pw")
        self.token = Token.objects.create(user=self.user)
        self.item = Menu.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=20)

    def test_list_is_public(self):
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [MenuSerializer(self.item).data])

    def test_retrieve_single_item(self):
        response = self.client.get(reverse("menu-detail", args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Greek Salad")

    def test_create_requires_authentication(self):
        payload = {"title": "Bruschetta", "price": "7.00", "inventory": 15}
        self.assertEqual(self.client.post(reverse("menu-list"), payload).status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(reverse("menu-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 2)

    def test_update_and_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("menu-detail", args=[self.item.pk])
        response = self.client.put(url, {"title": "Greek Salad", "price": "13.00", "inventory": 10})
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.price, Decimal("13.00"))
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Menu.objects.exists())


class BookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("guest", password="Lemon#2026pw")
        self.token = Token.objects.create(user=self.user)
        self.url = reverse("booking-list")
        self.payload = {
            "name": "Ben", "no_of_guests": 2, "booking_date": "2026-11-05T18:00:00Z",
        }

    def test_requires_token(self):
        self.assertEqual(self.client.get(self.url).status_code, 401)

    def test_create_list_update_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        created = self.client.post(self.url, self.payload)
        self.assertEqual(created.status_code, 201)
        detail = reverse("booking-detail", args=[created.data["id"]])

        self.assertEqual(len(self.client.get(self.url).data), 1)
        updated = self.client.patch(detail, {"no_of_guests": 6})
        self.assertEqual(updated.data["no_of_guests"], 6)
        self.assertEqual(self.client.delete(detail).status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

    def test_rejects_zero_guests(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(self.url, {**self.payload, "no_of_guests": 0})
        self.assertEqual(response.status_code, 400)


class AuthTests(TestCase):
    def test_register_then_login_for_token(self):
        client = APIClient()
        registered = client.post(
            "/auth/users/", {"username": "newuser", "password": "Lemon#2026pw"}
        )
        self.assertEqual(registered.status_code, 201)
        login = client.post(
            "/auth/token/login/", {"username": "newuser", "password": "Lemon#2026pw"}
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token", login.data)

    def test_login_with_wrong_password_fails(self):
        User.objects.create_user("someone", password="Lemon#2026pw")
        response = APIClient().post(
            "/auth/token/login/", {"username": "someone", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 400)


class HomePageTests(TestCase):
    def test_serves_static_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")
        self.assertTemplateUsed(response, "index.html")
