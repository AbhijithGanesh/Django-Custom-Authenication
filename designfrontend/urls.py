from django.urls import path
from .views import Landingpage, Second_Page, GuestLogin

urlpatterns = [
    path("", Landingpage),
    path("LoginPage", Second_Page ),
    path("Login/", GuestLogin.as_view())
]
