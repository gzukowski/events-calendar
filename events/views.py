from django.http import JsonResponse
from django.shortcuts import redirect, render
from .utils import fetch_events, fetch_event_details, filter_events

def home(request):
    events, tags = fetch_events()
    return render(request, 'home.html', {'events' : events, 'tags': tags})

def show_event(request, event_id):
    event = fetch_event_details(event_id)
    if event:
        return render(request, 'event_page.html', {'event' : event})
    else:
        return redirect('home')

def filtered_events(request):
    tag = request.GET.get('tag', None)
    events = filter_events(tag)
    return JsonResponse(events, safe=False)