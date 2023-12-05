from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedFile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class FileUploadForm(forms.ModelForm):
    encryption_algorithm = forms.ChoiceField(choices=[('none', 'None'), ('des', 'DES'), ('aes', 'AES'), ('blowfish', 'Blowfish')], required=True)
    encryption_key = forms.CharField(max_length=256, required=False, widget=forms.PasswordInput)
    class Meta:
        model = UploadedFile
        fields = ['file', 'encryption_algorithm', 'encryption_key']
