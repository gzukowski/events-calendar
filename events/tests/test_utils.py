import os
import json
from django.test import TestCase
from unittest.mock import patch, Mock
from ..utils import fetch_events, fetch_event_details, filter_events
import requests

class UtilsTests(TestCase):

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_events_success(self, mock_get):
        # Mock response for successful API call
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Event 1', 'start_time': '2023-01-01T10:00:00', 'tags': [{'name': 'tag1'}, {'name': 'tag2'}]},
            {'id': 2, 'name': 'Event 2', 'start_time': '2023-01-02T10:00:00', 'tags': [{'name': 'tag1'}]},
        ]
        mock_get.return_value = mock_response

        events, tags = fetch_events()

        self.assertEqual(len(events), 2)
        self.assertEqual(len(tags), 2)
        self.assertEqual(events[0]['title'], 'Event 1')
        self.assertEqual(sorted(tags), sorted(['tag1', 'tag2']))

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_events_api_key_not_found(self, mock_get):
        # Test when API_KEY is not set
        with patch.dict(os.environ, {'API_KEY': ''}):
            events, tags = fetch_events()
            self.assertEqual(events, [])
            self.assertEqual(tags, [])

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_events_failed_request(self, mock_get):
        # Mock response for failed request
        mock_get.side_effect = requests.RequestException("Network error")

        events, tags = fetch_events()

        self.assertEqual(events, [])
        self.assertEqual(tags, [])

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_event_details_success(self, mock_get):
        # Mock response for successful API call for event details
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Event 1', 'image_url': '/images/event1.jpg'}
        mock_get.return_value = mock_response

        event_details = fetch_event_details(1)

        self.assertEqual(event_details['name'], 'Event 1')
        self.assertEqual(event_details['image_url'], 'https://rekrutacja.teamwsuws.pl/images/event1.jpg')

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_event_details_api_key_not_found(self, mock_get):
        # Test when API_KEY is not set
        with patch.dict(os.environ, {'API_KEY': ''}):
            event_details = fetch_event_details(1)
            self.assertEqual(event_details, [])

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_fetch_event_details_failed_request(self, mock_get):
        # Mock response for failed request
        mock_get.side_effect = requests.RequestException("Network error")

        event_details = fetch_event_details(1)

        self.assertEqual(event_details, [])

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_filter_events_success(self, mock_get):
        # Mock response for successful API call to filter events
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Filtered Event 1', 'start_time': '2023-01-01T10:00:00'},
            {'id': 2, 'name': 'Filtered Event 2', 'start_time': '2023-01-02T10:00:00'},
        ]
        mock_get.return_value = mock_response

        events = filter_events('tag1')

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['title'], 'Filtered Event 1')

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_filter_events_failed_request(self, mock_get):
        # Mock response for failed request
        mock_get.side_effect = requests.RequestException("Network error")

        events = filter_events('tag1')

        self.assertEqual(events, [])

    @patch('events.utils.requests.get')
    @patch.dict(os.environ, {'API_KEY': 'fake_api_key'})
    def test_filter_events_api_key_not_found(self, mock_get):
        # Test when API_KEY is not set
        with patch.dict(os.environ, {'API_KEY': ''}):
            events = filter_events('tag1')
            self.assertEqual(events, [])
