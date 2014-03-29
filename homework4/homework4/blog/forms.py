from django import forms
from django.contrib.auth.models import User
from models import *


class RegistrationForm(forms.Form):
	username = forms.CharField(label = 'Username')
	email = forms.EmailField(label = 'Email')
	first_name = forms.CharField(max_length = 20, label='First_name')
	last_name = forms.CharField(max_length=50, label ='Last_name')
	password = forms.CharField(max_length = 200, label = 'Password', widget = forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		

		return username

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['owner']
		widgets = {'picture' : forms.FileInput()}

	