from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('', views.index, name='index'),
]

urlpatterns += [path('<path:path>/', TemplateView.as_view(template_name='404.html'))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)