from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('events/', views.home, name="home"),
    path('events/<int:event_id>/', views.show_event, name="show_event"),
    path('events/filter/', views.filtered_events, name="filtered_events")
]