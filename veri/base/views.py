from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, UserLoginForm
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Kullanıcıyı giriş sayfasına yönlendir
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            #return redirect('user_profile')  # Kullanıcıyı profiline yönlendir
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def custom_404(request, exception):
    return render(request, '404.html', status=404)
