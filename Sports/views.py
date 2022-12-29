from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta

from Slots.models import Location, Schedule, Slot
from Slots.forms import LocationForm

from Users.models import Notification

from .models import Inventory, Sport, Venue
from .forms import SportForm, VenueForm, InventoryForm

# Create your views here.


def index(request):
    # Home page
    return render(request, "Sports/index.html")


def view_sport(request, sport_id):
    # Individual page for each sport
    sport = Sport.objects.get(id=sport_id)
    venues = sport.venue_set.all()
    eqp = sport.inventory_set.all()
    context = {"sp": sport, "ven": venues, "eqp": eqp}

    return render(request, "Sports/sport.html", context=context)


def view_all_sports(request):
    # Link to all sports pages
    sport = Sport.objects.all()

    context = {"sp": sport}

    return render(request, "Sports/all_sports.html", context=context)


@login_required
def add_sport(request):
    # add sport form for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    if request.method != "POST":
        form = SportForm()

    else:
        form = SportForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:all_sports"))

    context = {"form": form}

    return render(request, "Sports/add_sport.html", context=context)


@login_required
def edit_sport(request, sport_id):
    # edit existing sport for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    sport = Sport.objects.get(id=sport_id)

    if request.method != "POST":
        form = SportForm(instance=sport)

    else:
        form = SportForm(instance=sport, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport", args=[sport_id]))

    context = {"form": form, "sp": sport}

    return render(request, "Sports/edit_sport.html", context=context)


@login_required
def add_venue(request, sport_id):
    # add new venue for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    sport = Sport.objects.get(id=sport_id)

    if request.method != "POST":
        form = VenueForm()

    else:
        form = VenueForm(data=request.POST)

        if form.is_valid():
            new_ven = form.save(commit=False)
            new_ven.sport = sport
            new_ven.save()

            return HttpResponseRedirect(reverse("Sports:sport", args=[sport_id]))

    context = {"form": form, "sp": sport}

    return render(request, "Sports/add_venue.html", context=context)


@login_required
def edit_venue(request, venue_id):
    # edit existing venue for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    venue = Venue.objects.get(id=venue_id)
    sport = venue.sport

    if request.method != "POST":
        form = VenueForm(instance=venue)

    else:
        form = VenueForm(instance=venue, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport", args=[sport.id]))

    context = {"form": form, "sp": sport, "ven": venue}

    return render(request, "Sports/edit_venue.html", context=context)


@login_required
def add_inventory(request, sport_id):
    # add new inventory for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    sport = Sport.objects.get(id=sport_id)

    if request.method != "POST":
        form = InventoryForm()

    else:
        form = InventoryForm(data=request.POST)

        if form.is_valid():
            new_inv = form.save(commit=False)
            new_inv.sport = sport
            new_inv.save()

            return HttpResponseRedirect(reverse("Sports:sport", args=[sport_id]))

    context = {"form": form, "sp": sport}

    return render(request, "Sports/add_inventory.html", context=context)


@login_required
def edit_inventory(request, inv_id):
    # edit existing inventory for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    inv = Inventory.objects.get(id=inv_id)
    sport = inv.sport

    if request.method != "POST":
        form = InventoryForm(instance=inv)

    else:
        form = InventoryForm(instance=inv, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport", args=[sport.id]))

    context = {"form": form, "sp": sport, "inv": inv}

    return render(request, "Sports/edit_inventory.html", context=context)


@login_required
def available_slots(request, sport_id, ven_id):
    # view available slots at a given location

    sp = Sport.objects.get(id=sport_id)
    ven = Venue.objects.get(id=ven_id)
    location = get_object_or_404(Location, sport=sp, venue=ven)

    sdate = datetime.now()
    edate = sdate + timedelta(weeks=1)
    slots = Slot.objects.filter(date__gte=sdate, date__lte=edate, location=location)

    header = []
    for i in range(8):
        dt = datetime.now() + timedelta(days=i)
        header.append(dt.strftime("%d/%m/%Y"))

    slots_dict = {
        (str(i) + ":00", str((i + 1) % 24) + ":00"): [False for _ in range(len(header))]
        for i in range(7, 24)
    }
    # sch = Schedule.objects.filter(location=loc)
    for s in slots:
        i = int((s.date - date.today()).days)
        st = s.schedule.start_time
        et = s.schedule.end_time
        t = (
            "{:d}:{:02d}".format(st.hour, st.minute),
            "{:d}:{:02d}".format(et.hour, et.minute),
        )
        slots_dict[t][i] = s

    context = {"loc": location, "slots": slots_dict, "header": header, "today": sdate}

    return render(request, "Sports/available_slots.html", context=context)


@login_required
def book_slot(request, slot_id):
    # book a slot

    slot = get_object_or_404(Slot, id=slot_id)

    if slot.status == 2 or slot.courts_booked >= slot.location.venue.no_of_courts:
        slot.status = 2
        slot.save()
        messages.error(request, "Slot is booked")
        return HttpResponseRedirect(
            reverse(
                "Sports:available_slots",
                args=[slot.location.sport.id, slot.location.venue.id],
            )
        )

    # count number of slots booked by user
    cnt = Slot.objects.filter(booking=request.user, date=slot.date).count()
    if cnt >= 3:
        messages.error(request, "You have already booked 3 slots for this day")
        return HttpResponseRedirect(
            reverse(
                "Sports:available_slots",
                args=[slot.location.sport.id, slot.location.venue.id],
            )
        )

    slot.booking.add(request.user)
    slot.courts_booked = slot.courts_booked + 1
    print(slot.courts_booked)

    if slot.courts_booked >= slot.location.venue.no_of_courts:
        slot.status = 2
    slot.save()
    messages.success(request, "Slot booked successfully")
    return HttpResponseRedirect(
        reverse(
            "Sports:available_slots",
            args=[slot.location.sport.id, slot.location.venue.id],
        )
    )


@login_required
def cancel_slot(request, slot_id):
    # cancel booked slot for user

    slot = get_object_or_404(Slot, id=slot_id)

    if request.user not in slot.booking.all():
        print("Invalid request")
        return HttpResponseRedirect(reverse("Users:profile"))

    slot.booking.remove(request.user)
    slot.courts_booked = slot.courts_booked - 1

    if slot.courts_booked < slot.location.venue.no_of_courts:
        slot.status = 1

    slot.save()

    messages.success(request, "Slot Booking cancelled successfully")
    return HttpResponseRedirect(
        reverse(
            "Sports:available_slots",
            args=[slot.location.sport.id, slot.location.venue.id],
        )
    )


@login_required
def staff_dashboard(request):
    # link to staff dashboard

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    return render(request, "Sports/staff_dashboard.html")


@login_required
def add_location(request):
    # add new location for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    if request.method != "POST":
        form = LocationForm()

    else:
        form = LocationForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:staff_dashboard"))

    context = {"form": form}

    return render(request, "Sports/add_location.html", context=context)


@login_required
def all_locations(request):
    # view all locations for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    locs = Location.objects.all()

    context = {"locs": locs}
    return render(request, "Sports/all_locations.html", context=context)


@login_required
def modify_location(request, loc_id):
    # modify existing location for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    loc = Location.objects.get(id=loc_id)

    if request.method != "POST":
        form = LocationForm(instance=loc)

    else:
        form = LocationForm(data=request.POST, instance=loc)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:staff_dashboard"))

    context = {"form": form, "l": loc}

    return render(request, "Sports/modify_location.html", context=context)


@login_required
def delete_location(request, loc_id):
    # delete a given location for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    loc = Location.objects.get(id=loc_id)

    loc.delete()
    return HttpResponseRedirect(reverse("Sports:staff_dashboard"))


@login_required
def scheduler(request, loc_id):
    # view schedule of a given location for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    loc = Location.objects.get(id=loc_id)

    header = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    # times = {i:[str(i)+":00",str(i+1)+":00"] for i in range(7,24)}
    is_scheduled = {
        (str(i) + ":00", str((i + 1) % 24) + ":00"): [False for _ in range(len(header))]
        for i in range(7, 24)
    }
    sch = Schedule.objects.filter(location=loc)

    for s in sch:
        i = int(s.day)
        st = s.start_time
        et = s.end_time
        t = (
            "{:d}:{:02d}".format(st.hour, st.minute),
            "{:d}:{:02d}".format(et.hour, et.minute),
        )
        is_scheduled[t][i] = True

    context = {"loc": loc, "header": header, "sch": is_scheduled}

    return render(request, "Sports/scheduler.html", context=context)


@login_required
def add_schedule(request, loc_id, day, stime):
    # add schedule at given location, day and time

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    loc = Location.objects.get(id=loc_id)
    s_time = datetime.strptime(stime, "%H:%M")
    e_time = s_time + timedelta(hours=1)
    if not Schedule.objects.filter(
        location=loc, day=day, start_time=s_time, end_time=e_time
    ).exists():
        Schedule.objects.create(
            location=loc, day=day, start_time=s_time, end_time=e_time
        )

    return HttpResponseRedirect(reverse("Sports:scheduler", args=[loc_id]))


@login_required
def remove_schedule(request, loc_id, day, stime):
    # remove schedule at given location, day and time

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    loc = Location.objects.get(id=loc_id)
    s_time = datetime.strptime(stime, "%H:%M")
    e_time = s_time + timedelta(hours=1)
    try:
        sch = Schedule.objects.get(
            location=loc, day=day, start_time=s_time, end_time=e_time
        )
        sch.delete()
    except Schedule.DoesNotExist():
        pass

    return HttpResponseRedirect(reverse("Sports:scheduler", args=[loc_id]))


@login_required
def view_slots_staff(request, loc_id):
    # view all slots status overview for staff at given location

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    sdate = datetime.now()
    edate = sdate + timedelta(weeks=1)

    loc = Location.objects.get(id=loc_id)
    slots = Slot.objects.filter(date__gte=sdate, date__lte=edate, location=loc)

    header = []
    for i in range(8):
        dt = datetime.now() + timedelta(days=i)
        header.append(dt.strftime("%d/%m/%Y"))
    # print(header)

    slots_dict = {
        (str(i) + ":00", str((i + 1) % 24) + ":00"): [False for _ in range(len(header))]
        for i in range(7, 24)
    }
    # sch = Schedule.objects.filter(location=loc)
    for s in slots:
        i = int((s.date - date.today()).days)
        st = s.schedule.start_time
        et = s.schedule.end_time
        t = (
            "{:d}:{:02d}".format(st.hour, st.minute),
            "{:d}:{:02d}".format(et.hour, et.minute),
        )
        slots_dict[t][i] = s

    # print(slots_dict)
    context = {"slots": slots_dict, "loc": loc, "header": header}
    return render(request, "Sports/view_slots_staff.html", context=context)


@login_required
def manage_slot(request, slot_id):
    # manage a given slot for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    slot = Slot.objects.get(id=slot_id)
    td = datetime.now()

    context = {"slot": slot, "today": td}

    return render(request, "Sports/slot_actions.html", context=context)


@login_required
def cancel_slot_staff(request, slot_id, user_id):
    # cancel a user's slot booking for staff

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    usr = User.objects.get(id=user_id)
    slot = Slot.objects.get(id=slot_id)

    if usr not in slot.booking.all():
        return HttpResponseRedirect(reverse("Sports:index"))

    slot.booking.remove(usr)
    slot.courts_booked = slot.courts_booked - 1

    if slot.courts_booked < slot.location.venue.no_of_courts:
        slot.status = 1

    slot.save()

    # send notification to user
    dt = slot.date.strftime("%m/%d/%Y")
    CNC_TXT = f"We are sorry to inform you that your slot booking (Date:{dt} From:{slot.schedule.start_time} To:{slot.schedule.end_time}) for {slot.location.sport.name} at {slot.location.venue.name} has been cancelled due to unavoidable reasons.\nWe are extremely sorry for the inconvenience."
    _ = Notification.objects.create(user=usr, text=CNC_TXT)

    return HttpResponseRedirect(reverse("Sports:manage_slot", args=[slot_id]))


@login_required
def schedule_maintenance(request, slot_id):
    # schedule the slot for maintenance

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    slot = Slot.objects.get(id=slot_id)
    users = slot.booking.all()

    for usr in users:
        slot.booking.remove(usr)

    slot.courts_booked = 0
    slot.status = 3

    slot.save()
    dt = slot.date.strftime("%m/%d/%Y")
    # send notif to users
    MNT_TXT = f"We are sorry to inform you that your slot booking (Date:{dt} From:{slot.schedule.start_time} To:{slot.schedule.end_time}) for {slot.location.sport.name} at {slot.location.venue.name} is cancelled due to maintenance.\nWe are extremely sorry for the inconvenience."
    for usr in users:
        _ = Notification.objects.create(user=usr, text=MNT_TXT)

    return HttpResponseRedirect(reverse("Sports:manage_slot", args=[slot_id]))


@login_required
def cancel_maintenance(request, slot_id):
    # cancel scheduled maintenance for given slot

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    slot = Slot.objects.get(id=slot_id)
    slot.status = 1
    slot.save()

    return HttpResponseRedirect(reverse("Sports:manage_slot", args=[slot_id]))


@login_required
def holiday(request, slot_id):
    # cancel a slot due to holiday

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    slot = Slot.objects.get(id=slot_id)
    users = slot.booking.all()

    for usr in users:
        slot.booking.remove(usr)

    slot.courts_booked = 0
    slot.status = 4

    slot.save()

    # send notif to users
    dt = slot.date.strftime("%m/%d/%Y")
    HLD_TXT = f"We are sorry to inform you that your slot booking (Date:{dt} From:{slot.schedule.start_time} To:{slot.schedule.end_time}) for {slot.location.sport.name} at {slot.location.venue.name} is cancelled due to holiday."
    for usr in users:
        _ = Notification.objects.create(user=usr, text=HLD_TXT)

    return HttpResponseRedirect(reverse("Sports:manage_slot", args=[slot_id]))
