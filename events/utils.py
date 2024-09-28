import os
import requests
from dotenv import load_dotenv
import logging
logger = logging.getLogger('django')

load_dotenv()

def fetch_events(tag = None):
    logger.info("Fetching events started.")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API key not found.")
        return [], []
    
    headers = {"api-key": api_key}
    
    try:
        response = requests.get(url='https://rekrutacja.teamwsuws.pl/events/', headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch events: {e}")
        return [], []
    
    if response.status_code == 200:
        events = []
        all_tags = set()

        for event in response.json():
            event_tags = [tag["name"] for tag in event["tags"]]
            all_tags.update(event_tags)

            events.append({
                'id': event['id'],
                'title': event['name'],
                'start': event['start_time'],
            })

        unique_tags = list(all_tags)
        logger.info(f"Fetched {len(events)} events and {len(unique_tags)} unique tags.")
        return events, unique_tags
    else:
        logger.warning(f"Failed to fetch events, status code: {response.status_code}")
    
    return [], []

def fetch_event_details(event_id):
    logger.info(f"Fetching details for event {event_id}.")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API key not found.")
        return []
    
    headers = {"api-key": api_key}
    url = f"https://rekrutacja.teamwsuws.pl/events/{event_id}"
    
    try:
        response = requests.get(url=url, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch event details for event {event_id}: {e}")
        return []
    
    if response.status_code == 200:
        result = response.json()
        result['image_url'] = "https://rekrutacja.teamwsuws.pl" + result['image_url']
        logger.info(f"Successfully fetched details for event {event_id}.")
        return result
    else:
        logger.warning(f"Failed to fetch details for event {event_id}, status code: {response.status_code}")
    
    return []

def filter_events(tag):
    logger.info(f"Filtering events by tag: {tag}.")
    
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API key not found.")
        return []
    
    headers = {"api-key": api_key}
    url = "https://rekrutacja.teamwsuws.pl/events/filter/"
    
    if tag:
        url += f'?tag={tag}'
    else:
        url = "https://rekrutacja.teamwsuws.pl/events/"
    
    try:
        response = requests.get(url=url, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to filter events by tag {tag}: {e}")
        return []
    
    if response.status_code == 200:
        result = [{
            'id': event['id'],
            'title': event['name'],
            'start': event['start_time']
        } for event in response.json()]
        logger.info(f"Filtered {len(result)} events by tag: {tag}.")
        return result
    else:
        logger.warning(f"Failed to filter events by tag {tag}, status code: {response.status_code}")
    
    return []

