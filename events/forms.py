from django import forms
from django.contrib.auth.models import User
from .models import *

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm (forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','location','datetime','seats',]
        widgets={
        'datetime': forms.DateTimeInput(format='%Y-%m-%d %H:%M'),
        }

class ParticipantForm (forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['seats_to_book']
