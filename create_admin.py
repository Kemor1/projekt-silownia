import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from gym_management.models import Uzytkownik

# Definiujemy dane Twojego admina
username = 'kemor'
email = 'kemorpoczta@gmail.com'
password = 'polop123'

if not Uzytkownik.objects.filter(username=username).exists():
    Uzytkownik.objects.create_superuser(username=username, email=email, password=password)
    print("Konto administratora zostalo utworzone!")
else:
    print("Admin juz istnieje.")