from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from gym_management import views

urlpatterns = [
    path('admin/', admin.site.core_urls if hasattr(admin.site, 'core_urls') else admin.site.urls),
    path('', views.index, name='index'),
    path('grafik/', views.publiczny_grafik, name='publiczny_grafik'),
    path('panel/', views.panel_klubowicza, name='panel_klubowicza'),
    path('zapisz/<int:zajecia_id>/', views.zapisz_na_zajecia, name='zapisz_na_zajecia'),
    path('wypisz/<int:zajecia_id>/', views.wypisz_z_zajec, name='wypisz_z_zajec'),
    path('trener/', views.panel_trenera, name='panel_trenera'),
    path('recepcja/', views.panel_recepcji, name='panel_recepcji'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('login/', auth_views.LoginView.as_view(template_name='gym/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)