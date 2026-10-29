from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"tables", views.BookingViewSet, basename="booking")

urlpatterns = [
    path("", views.index, name="home"),
    path("menu/", views.MenuItemsView.as_view(), name="menu-list"),
    path("menu/<int:pk>/", views.SingleMenuItemView.as_view(), name="menu-detail"),
    path("booking/", include(router.urls)),
]
