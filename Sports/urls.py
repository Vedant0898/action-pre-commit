from django.urls import path

from . import views

app_name = "Sports"

urlpatterns = [
    # Home Page
    path("",views.index,name='index'),

    # Sports page
    path("sport/<int:sport_id>",views.view_sport,name="sport"),
    path("sports",views.view_all_sports,name="all_sports"),

    # Staff pages
    path("sports/add",views.add_sport,name="add_sport"),
    path("sport/<int:sport_id>/edit",views.edit_sport,name="edit_sport"),
    path("venues/add/<int:sport_id>",views.add_venue,name="add_venue"),
    path("venues/<int:venue_id>/edit",views.edit_venue,name="edit_venue"),
    path("inventory/add/<int:sport_id>",views.add_inventory,name="add_inventory"),
    path("inventory/<int:inv_id>/edit",views.edit_inventory,name="edit_inventory"),

    # Slot pages
    path("slot/<int:sport_id>/<int:ven_id>",views.available_slots,name="available_slots"),
    path("slot/<int:slot_id>/book",views.book_slot,name="book_slot"),
    path("slot/<int:slot_id>/cancel",views.cancel_slot,name = "cancel_slot"),

]