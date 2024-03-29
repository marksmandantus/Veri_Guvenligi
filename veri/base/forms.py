from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedFile
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-callback': 'onCaptchaSuccess'}))
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class FileUploadForm(forms.ModelForm):
    encryption_algorithm = forms.ChoiceField(choices=[('none', 'None'), ('des', 'DES'), ('aes', 'AES'), ('blowfish', 'Blowfish')], required=False)
    encryption_key = forms.CharField(max_length=256, required=False, widget=forms.PasswordInput)
    class Meta:
        model = UploadedFile
        fields = ['file', 'encryption_algorithm', 'encryption_key']
