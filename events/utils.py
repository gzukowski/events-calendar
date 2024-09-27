import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_events_from_api():
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
