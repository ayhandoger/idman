from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Idea

class IdeaMethodTests(TestCase):
	def test_was_published_recently_with_future_idea(self):
		"""
		was_published_recently() should return False for idea whose
		pub_date is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_idea = Idea(pub_date=time)
		self.assertEqual(future_idea.was_published_recently(), False)

	def test_was_published_recently_with_old_idea(self):
		"""
		was_published_recently() should return False for ideas whose
		pub_date is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_idea = Idea(pub_date=time)
		self.assertEqual(old_idea.was_published_recently(), False)

	def test_was_published_recently_with_recent_idea(self):
		"""
		was_published_recently() should return True for ideas whose
		pub_date is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_idea = Idea(pub_date=time)
		self.assertEqual(recent_idea.was_published_recently(), True)

		
		
		
		
	def create_idea(idea_text, days):
		"""
		Creates a idea with the given `idea_text` published the given
		number of `days` offset to now (negative for ideas published
		in the past, positive for ideas that have yet to be published).
		"""
		time = timezone.now() + datetime.timedelta(days=days)
		return Idea.objects.create(idea_text=idea_text,
									pub_date=time)
									
	class IdeaViewTests(TestCase):
		def test_index_view_with_no_ideas(self):
			"""
			If no ideas exist, an appropriate message should be displayed.
			"""
			response = self.client.get(reverse('idman:index'))
			self.assertEqual(response.status_code, 200)
			self.assertContains(response, "No idman are available.")
			self.assertQuerysetEqual(response.context['latest_idea_list'], [])

		def test_index_view_with_a_past_idea(self):
			"""
			Ideas with a pub_date in the past should be displayed on the
			index page.
			"""
			create_idea(idea_text="Past idea.", days=-30)
			response = self.client.get(reverse('idman:index'))
			self.assertQuerysetEqual(
				response.context['latest_idea_list'],
				['<Idea: Past idea.>']
		)
		def test_index_view_with_a_future_idea(self):
			"""
			Ideas with a pub_date in the future should not be displayed on
			the index page.
			"""
			create_idea(idea_text="Future idea.", days=30)
			response = self.client.get(reverse('idman:index'))
			self.assertContains(response, "No idman are available.",
								status_code=200)
			self.assertQuerysetEqual(response.context['latest_idea_list'], [])

		def test_index_view_with_future_idea_and_past_idea(self):
		"""
		Even if both past and future ideas exist, only past ideas 
		should be displayed.
		"""
		create_idea(idea_text="Past idea.", days=-30)
		create_idea(idea_text="Future idea.", days=30)
		response = self.client.get(reverse('idman:index'))
		self.assertQuerysetEqual(
			response.context['latest_idea_list'],
			['<Idea: Past idea.>']
		)
		
		def test_index_view_with_two_past_ideas(self):
			"""
			The ideas index page may display multiple ideas.
			"""
			create_idea(idea_text="Past idea 1.", days=-30)
			create_idea(idea_text="Past idea 2.", days=-5)
			response = self.client.get(reverse('idman:index'))
			self.assertQuerysetEqual(
				response.context['latest_idea_list'],
				['<Idea: Past idea 2.>', '<Idea: Past idea 1.>']
			)

			
			
class IdeaIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_idea(self):
		"""
		The detail view of a idea with a pub_date in the future should
		return a 404 not found.
		"""
		future_idea = create_idea(idea_text='Future idea.',
											days=5)
		response = self.client.get(reverse('idman:detail',
									args=(future_idea.id,)))
		self.assertEqual(response.status_code, 404)
	
	def test_detail_view_with_a_past_idea(self):
		"""
		The detail view of a idea with a pub_date in the past should
		display the idea's text.
		"""
		past_idea = create_idea(idea_text='Past Idea.',
										days=-5)
		response = self.client.get(reverse('idman:detail',
									args=(past_idea.id,)))
		self.assertContains(response, past_idea.idea_text,
							status_code=200)