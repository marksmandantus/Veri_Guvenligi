from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, UserLoginForm, FileUploadForm
from .models import UploadedFile, CustomUser, Directory
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'index.html')

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
            return redirect('user_profile')  # Kullanıcıyı profiline yönlendir
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_profile(request):
    user = request.user
    user_profile, created = CustomUser.objects.get_or_create(user=user)

    directories = Directory.objects.all()
    files_by_directory = {}

    for directory in directories:
        files_by_directory[directory] = UploadedFile.objects.filter(
            user_profile=user_profile,
            directory=directory
        )

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user_profile = user_profile

            # Dizin bilgisini formdan al veya varsayılan bir dizin belirle
            directory_id = form.cleaned_data.get('directory')
            if directory_id:
                directory = Directory.objects.get(id=directory_id)
            else:
            # Provide a default directory or handle this case based on your requirements
            # For example, create a default directory if it doesn't exist.
                directory, created = Directory.objects.get_or_create(name='Default')
            uploaded_file.directory = directory
            uploaded_file.save()
            return redirect('user_profile')
    else:
        form = FileUploadForm()

    user_files = UploadedFile.objects.filter(user_profile=user_profile)
    return render(request, 'user_profile.html', {'form': form, 'user_files': user_files, 'files_by_directory': files_by_directory})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

from django.http import JsonResponse

def delete_file(request, id):
    uploaded_file = get_object_or_404(UploadedFile, id=id)
    uploaded_file.file.delete()  # Dosyayı diskten sil
    uploaded_file.delete()  # Veritabanından dosyayı sil
    return JsonResponse({'status': 'success'})