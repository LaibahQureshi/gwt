from django import forms
from .models import ProgressUpdate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SubCategory
class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ProgressUpdate
        fields = ['category', 'entry',]

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ProgressUpdate
        fields = ['feedback']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['main_category', 'name']
