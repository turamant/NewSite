from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'age', 'phone_number',
                  'profile_picture', 'bio', 'location')

