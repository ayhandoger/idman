import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class Idea(models.Model):
	idea_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __str__(self): # __unicode__ on Python 2
		return self.idea_text
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class Innovator(models.Model):
	idea = models.ForeignKey(Idea)
	innovator_name = models.CharField(max_length=70)
	votes = models.IntegerField(default=0)
	def __str__(self): # __unicode__ on Python 2
			return self.innovator_name	
			
			
	


class Employee(models.Model):
	employee_name = models.CharField(max_length=70)
	employee_description = models.IntegerField(default=0)
	def __str__(self): # __unicode__ on Python 2
			return self.innovator_name		
			
class Employee(models.Model):
	employee_name = models.CharField(max_length=70)
	employee_description = models.IntegerField(default=0)
	def __str__(self): # __unicode__ on Python 2
			return self.innovator_name				