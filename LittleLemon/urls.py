from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Home page and menu/booking API
    path("", include("restaurant.urls")),
    # User registration (POST /auth/users/) and token login (POST /auth/token/login/)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
