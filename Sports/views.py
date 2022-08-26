from django.shortcuts import render

from .models import Sport
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