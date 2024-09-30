import requests
import os
import logging
from celery import shared_task
from .models import Event, Tag
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('django')

@shared_task
def celery_fetch_events():
    api_url = "https://rekrutacja.teamwsuws.pl/events"
    logger.info("Fetching events started.")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API key not found.")
        return
    
    headers = {"api-key": api_key}

    try:
        response = requests.get(url=api_url, headers=headers)
        response.raise_for_status()

        events_data = response.json()

        for event_data in events_data:
            event, created = Event.objects.update_or_create(
                id=event_data['id'],
                defaults={
                    'name': event_data['name'],
                    'start_time': event_data['start_time'],
                    'duration': event_data['duration'],
                    'image_url': event_data['image_url'],
                    'short_description': event_data['short_description']
                }
            )

            # Clear existing tags and set new ones
            event.tags.clear()
            for tag_data in event_data['tags']:
                tag, tag_created = Tag.objects.get_or_create(
                    id=tag_data['id'],
                    defaults={'name': tag_data['name']}
                )
                event.tags.add(tag)
            
            logger.info(f"{'Created' if created else 'Updated'} event: {event.name}")

    except requests.HTTPError as e:
        logger.error(f"HTTP error fetching events: {e.response.status_code} - {e.response.text}")
    except requests.RequestException as e:
        logger.error(f"Network error fetching events: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
