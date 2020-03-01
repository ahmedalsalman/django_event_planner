from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

from .forms import (
	UserSignup,
	UserLogin,
	EventForm,
	ParticipantForm
	)
from .models import Event , Participant

def home(request):
	return render(request, 'home.html')


class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				return redirect('dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")


def event_list(request):
	# Change variable name of all_events
	all_events = Event.objects.filter(datetime__gte = datetime.today()) #change it to timezone.now after you know what to import
	query = request.GET.get('q')
	if query:
		all_events = all_events.filter(
		Q(title__icontains=query)
		| Q(description__icontains=query)
		| Q(owner__first_name__icontains=query)
		| Q(owner__last_name__icontains=query)).distinct()

	context = {
	'all_events' : all_events,

	}
	return render(request , "eventlist.html" , context )


def dashboard(request):
	owned_events = request.user.events.all()
	events = request.user.participated.all()
	context = {
		'events' : events,
		'owned_events' : owned_events,

	}
	return render(request , "dashboard.html" , context )


def event_detail(request , event_id):
	event = Event.objects.get(id = event_id)
	participants = event.participants.all()
	context ={
	"event" : event,
	"participants": participants
	}
	return render(request , "eventdetail.html", context)

def event_update(request , event_id):
	event = Event.objects.get(id=event_id)
	form = EventForm(instance=event)
	if request.method == "POST":
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
		return redirect('dashboard')
		print (form.errors)
	context ={
	"event" : event,
	"form" : form
	}
	return render(request , "edit.html", context)

def event_create(request):
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			event = form.save(commit = False)
			event.owner = request.user
			event.seats_remaining = event.seats
			event.save()
			messages.success(request, "Successfully Added!")
			return redirect('dashboard')
	context = {
	"events" : Event.objects.all(),
	"form" : form
	}
	return render(request , 'create.html' , context)

def event_book(request, event_id):
	form = ParticipantForm()
	event = Event.objects.get(id = event_id)
	if request.method == "POST":
		form = ParticipantForm(request.POST)
		if form.is_valid():
			participant = form.save(commit = False)
			participant.event = event
			participant.participant = request.user
			if event.seats_remaining >= participant.seats_to_book:
				event.seats_remaining -= participant.seats_to_book
				participant.save()
				event.save()
				messages.success(request, "Successfully Added!")
				return redirect('dashboard')
			elif event.seats_remaining == 0:
				messages.error(request, "All seats have been booked!")
			else:
				messages.warning(request, "Try to book less seats")
				return redirect('event-detail', event_id)
	context = {
	"event" :event,
	"form" : form
	}
	return render(request , 'book.html' , context)

def event_delete(request , event_id ):
	Event.object.get(id = event_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect("event-list")
