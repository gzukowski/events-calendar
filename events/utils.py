import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_events():
    api_key = os.getenv('API_KEY')
    headers = { "api-key": api_key }

    response = requests.get(url='https://rekrutacja.teamwsuws.pl/events/', headers=headers)
    
    if response.status_code == 200:
        result = [{
            'id': event['id'],
            'title': event['name'],
            'start': event['start_time']
        } for event in response.json()]
        return result

    return []

def fetch_event_details(event_id):
    api_key = os.getenv('API_KEY')
    headers = { "api-key": api_key }
    url = f"https://rekrutacja.teamwsuws.pl/events/{event_id}"
    response = requests.get(url=url, headers=headers)
    
    print(response.text)
    if response.status_code == 200:
        result = response.json()
        result['image_url'] = "https://rekrutacja.teamwsuws.pl" + result['image_url']
        return result

    return []

