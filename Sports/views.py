from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Slots.models import Location, Schedule, Slot

from .models import Inventory, Sport,Venue
from .forms import SportForm,VenueForm,InventoryForm
# Create your views here.

def index(request):
    return render(request,"Sports/index.html")

def view_sport(request,sport_id):
    sport = Sport.objects.get(id = sport_id)
    venues = sport.venue_set.all()
    eqp = sport.inventory_set.all()
    context = {"sp":sport,"ven":venues,"eqp":eqp}

    return render(request,"Sports/sport.html",context=context)

def view_all_sports(request):
    sport = Sport.objects.all()

    context = {"sp":sport}

    return render(request,"Sports/all_sports.html",context=context)

@login_required
def add_sport(request):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    if request.method != "POST":
        form = SportForm()
    
    else:
        form = SportForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:all_sports"))
    
    context = {"form":form}

    return render(request,"Sports/add_sport.html",context=context)

@login_required
def edit_sport(request,sport_id):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))

    sport = Sport.objects.get(id = sport_id)

    if request.method != "POST":
        form = SportForm(instance=sport)
    
    else:
        form = SportForm(instance=sport,data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport",args=[sport_id]))
    
    context = {"form":form,"sp":sport}

    return render(request,"Sports/edit_sport.html",context=context)

@login_required
def add_venue(request,sport_id):

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

            return HttpResponseRedirect(reverse("Sports:sport",args=[sport_id]))
    
    context = {"form":form,"sp":sport}

    return render(request,"Sports/add_venue.html",context=context)

@login_required
def edit_venue(request,venue_id):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))
    
    venue = Venue.objects.get(id = venue_id)
    sport = venue.sport

    if request.method != "POST":
        form = VenueForm(instance=venue)
    
    else:
        form = VenueForm(instance=venue,data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport",args=[sport.id]))
    
    context = {"form":form,"sp":sport,"ven":venue}

    return render(request,"Sports/edit_venue.html",context=context)

@login_required
def add_inventory(request,sport_id):

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

            return HttpResponseRedirect(reverse("Sports:sport",args=[sport_id]))
    
    context = {"form":form,"sp":sport}

    return render(request,"Sports/add_inventory.html",context=context)

@login_required
def edit_inventory(request,inv_id):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse("Sports:index"))
    
    inv = Inventory.objects.get(id = inv_id)
    sport = inv.sport

    if request.method != "POST":
        form = InventoryForm(instance=inv)
    
    else:
        form = InventoryForm(instance=inv,data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("Sports:sport",args=[sport.id]))
    
    context = {"form":form,"sp":sport,"inv":inv}

    return render(request,"Sports/edit_inventory.html",context=context)

@login_required
def available_slots(request,sport_id,ven_id):
    sp = Sport.objects.get(id = sport_id)
    ven = Venue.objects.get(id= ven_id)
    location = get_object_or_404(Location,sport = sp,venue = ven)
    courts_available = ven.no_of_courts
    slots = Slot.objects.filter(location=location,status = 1,courts_booked__lt = courts_available).exclude(booking=request.user)

    context = {"loc":location,"slots":slots}

    return render(request,"Sports/available_slots.html",context=context)

@login_required
def book_slot(request,slot_id):

    slot = get_object_or_404(Slot,id = slot_id)

    if slot.status==2 or slot.courts_booked>=slot.location.venue.no_of_courts:
        slot.status=2
        slot.save()
        messages.error(request,"Slot is booked")
        return HttpResponseRedirect(reverse("Sports:available_slots",args=[slot.location.sport.id,slot.location.venue.id]))
    
    # count number of slots booked by user


    slot.booking.add(request.user)
    slot.courts_booked = slot.courts_booked+1
    print(slot.courts_booked)

    if slot.courts_booked>=slot.location.venue.no_of_courts:
        slot.status=2
    slot.save()
    messages.success(request,"Slot booked successfully")
    return HttpResponseRedirect(reverse("Sports:available_slots",args=[slot.location.sport.id,slot.location.venue.id]))

@login_required
def cancel_slot(request,slot_id):

    slot = get_object_or_404(Slot,id = slot_id)

    if request.user not in slot.booking.all():
        print("Invalid request")
        return HttpResponseRedirect(reverse("Users:profile"))
    
    slot.booking.remove(request.user)
    slot.courts_booked = slot.courts_booked-1
    
    if slot.courts_booked<slot.location.venue.no_of_courts:
        slot.status = 1
    
    slot.save()

    messages.success(request,'Slot Booking cancelled successfully')
    return HttpResponseRedirect(reverse("Users:profile"))