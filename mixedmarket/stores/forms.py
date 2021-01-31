from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

class SearchForm(forms.Form):
    CHOICES = (('ae', 'American Eagle'),
               ('asos', 'ASOS'),
               ('hm', 'H&M'),)
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.SelectMultiple(), required=True)
    search = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Search...'}), required=True)
