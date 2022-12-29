from django.urls import path

from . import views

app_name = "Sports"

urlpatterns = [
    # Home Page
    path("", views.index, name="index"),
    # Sports page
    path("sport/<int:sport_id>", views.view_sport, name="sport"),
    path("sports", views.view_all_sports, name="all_sports"),
    # Staff pages
    path("sports/add", views.add_sport, name="add_sport"),
    path("sport/<int:sport_id>/edit", views.edit_sport, name="edit_sport"),
    path("venues/add/<int:sport_id>", views.add_venue, name="add_venue"),
    path("venues/<int:venue_id>/edit", views.edit_venue, name="edit_venue"),
    path("inventory/add/<int:sport_id>", views.add_inventory, name="add_inventory"),
    path("inventory/<int:inv_id>/edit", views.edit_inventory, name="edit_inventory"),
    # staff dashboard pages
    path("staff", views.staff_dashboard, name="staff_dashboard"),
    path("staff/loc/add", views.add_location, name="add_location"),
    path("staff/loc/all", views.all_locations, name="all_locations"),
    path(
        "staff/loc/modify/<int:loc_id>", views.modify_location, name="modify_location"
    ),
    path(
        "staff/loc/delete/<int:loc_id>", views.delete_location, name="delete_location"
    ),
    path("staff/scheduler/<int:loc_id>", views.scheduler, name="scheduler"),
    path(
        "staff/scheduler/add/<int:loc_id>-<int:day>-<str:stime>",
        views.add_schedule,
        name="add_schedule",
    ),
    path(
        "staff/scheduler/remove/<int:loc_id>-<int:day>-<str:stime>",
        views.remove_schedule,
        name="remove_schedule",
    ),
    path(
        "staff/slots/all/<int:loc_id>", views.view_slots_staff, name="view_slots_staff"
    ),
    path("staff/slots/manage/<int:slot_id>", views.manage_slot, name="manage_slot"),
    path(
        "staff/slots/cancel/<int:slot_id>/<int:user_id>",
        views.cancel_slot_staff,
        name="cancel_slot_staff",
    ),
    path(
        "staff/slots/sch_mntnce/<int:slot_id>",
        views.schedule_maintenance,
        name="schedule_maintenance",
    ),
    path(
        "staff/slots/cancel_mntnce/<int:slot_id>",
        views.cancel_maintenance,
        name="cancel_maintenance",
    ),
    path("staff/slots/holiday/<int:slot_id>", views.holiday, name="holiday"),
    # Slot pages
    path(
        "slot/<int:sport_id>/<int:ven_id>",
        views.available_slots,
        name="available_slots",
    ),
    path("slot/<int:slot_id>/book", views.book_slot, name="book_slot"),
    path("slot/<int:slot_id>/cancel", views.cancel_slot, name="cancel_slot"),
]
