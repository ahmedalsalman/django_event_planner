from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Event(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField()
	location = models.CharField(max_length = 60)
	datetime = models.DateTimeField(default=datetime.today())
	seats = models.PositiveIntegerField()
	seats_remaining = models.PositiveIntegerField(null = True, blank = True,default=1)	
	owner = models.ForeignKey(User, default=1, on_delete= models.CASCADE, related_name='owner')
	def __str__(self):
		return self.title

class Participant(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='attendant')
	participant = models.ForeignKey(User, on_delete = models.CASCADE)
	seats_to_book = models.PositiveIntegerField()
	def __str__(self):
		return self.event.title
