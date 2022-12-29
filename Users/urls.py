from django.urls import path

from . import views

app_name = "Users"

urlpatterns = [
    # User auth
    path("register", views.register, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    # Profile
    path("profile", views.profile, name="profile"),
    path("slots/booked", views.view_booked_slots, name="view_booked_slots"),
    path("notifications", views.view_notification, name="view_notification"),
]
