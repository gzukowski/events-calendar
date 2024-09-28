from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from ..utils import fetch_events, fetch_event_details, filter_events

class ViewsTests(TestCase):

    @patch('events.views.fetch_events')
    def test_home_view(self, mock_fetch_events):
        mock_fetch_events.return_value = (['event1', 'event2'], ['tag1', 'tag2'])

        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('events', response.context)
        self.assertIn('tags', response.context)
        self.assertEqual(len(response.context['events']), 2)
        self.assertEqual(len(response.context['tags']), 2)

    @patch('events.views.fetch_event_details')
    def test_show_event_view(self, mock_fetch_event_details):
        mock_fetch_event_details.return_value = {'id': 1, 'name': 'Event 1'}

        response = self.client.get(reverse('show_event', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_page.html')
        self.assertIn('event', response.context)
        self.assertEqual(response.context['event']['name'], 'Event 1')

    @patch('events.views.fetch_event_details')
    def test_show_event_view_redirects_on_no_event(self, mock_fetch_event_details):
        mock_fetch_event_details.return_value = None

        response = self.client.get(reverse('show_event', args=[1]))

        self.assertRedirects(response, reverse('home'))

    @patch('events.views.filter_events')
    def test_filtered_events_view(self, mock_filter_events):
        mock_filter_events.return_value = [{'id': 1, 'name': 'Event 1'}]

        response = self.client.get(reverse('filtered_events'), {'tag': 'tag1'})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [{'id': 1, 'name': 'Event 1'}])

