from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class user_onboarding_form(forms.ModelForm):
    class Meta:
        model = UserProfile
        #todo:change some fields to disabled
        fields = ['branch','gender','mob','tags','profile_pic']
        widgets = {
        'branch': forms.TextInput(attrs={'readonly': 'true'}),
        'gender': forms.TextInput(attrs={'readonly': 'true'}),
    }
      
         
       
