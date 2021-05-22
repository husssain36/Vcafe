from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

	def clean_email(self):
		username = self.cleaned_data['username']
		if not username.endswith('@vit.edu.in'):
			raise ValidationError('Please enter a VIT email')
		return username