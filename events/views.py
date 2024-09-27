from django.shortcuts import render
from .utils import fetch_events_from_api
from datetime import datetime

def home(request):
    events = fetch_events_from_api()
    return render(request, 'home.html', {'events' : events})

def show_event(request, event_id):
    event = None
    return render(request, 'event.html', {'event' : event})