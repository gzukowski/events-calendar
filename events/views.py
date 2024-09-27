from django.shortcuts import render
from .utils import fetch_events, fetch_event_details
from datetime import datetime

def home(request):
    events = fetch_events()
    return render(request, 'home.html', {'events' : events})

def show_event(request, event_id):
    event = fetch_event_details(event_id)
    return render(request, 'event_page.html', {'event' : event})