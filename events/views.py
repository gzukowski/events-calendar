from django.shortcuts import render

def home(request):
    events = None
    return render(request, 'home.html', {'events' : events})