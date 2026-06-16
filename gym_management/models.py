from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Uzytkownik(AbstractUser):
    ROLES = (
        ('GOSC', 'Niezalogowany Gość'),
        ('KLUBOWICZ', 'Klubowicz'),
        ('TRENER', 'Trener Personalny'),
        ('RECEPCJA', 'Pracownik Recepcji'),
        ('ADMIN', 'Administrator'),
    )
    
    email = models.EmailField(unique=True)
    rola = models.CharField(max_length=20, choices=ROLES, default='GOSC')
    zdjecie_identyfikacyjne = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'rola']
    
    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rola_display()})"

class Karnet(models.Model):
    TYPES = (
        ('OPEN', 'Karnet Open'),
        ('STUDENT', 'Karnet Studencki'),
        ('RELAX', 'Karnet Weekendowy'),
    )
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, related_name='karnety')
    data_od = models.DateField()
    data_do = models.DateField()
    typ = models.CharField(max_length=30, choices=TYPES, default='OPEN')

    @property
    def czy_wazny(self):
        return self.data_do >= timezone.now().date() and self.data_od <= timezone.now().date()

    class Meta:
        verbose_name = "Karnet"
        verbose_name_plural = "Karnety"

    def __str__(self):
        status = "AKTYWNY" if self.czy_wazny else "NIEAKTYWNY"
        return f"Karnet {self.get_typ_display()} - {self.uzytkownik.last_name} ({status})"

class Zajecia(models.Model):
    trener = models.ForeignKey(Uzytkownik, on_delete=models.SET_NULL, null=True, limit_choices_to={'rola': 'TRENER'}, related_name='prowadzone_zajecia')
    nazwa = models.CharField(max_length=100)
    data_czas = models.DateTimeField()
    limit_miejsc = models.IntegerField()

    class Meta:
        verbose_name = "Zajęcia"
        verbose_name_plural = "Zajęcia"

    def __str__(self):
        return f"{self.nazwa} - {self.data_czas.strftime('%d-%m-%Y %H:%M')}"

    @property
    def wolne_miejsca(self):
        return self.limit_miejsc - self.zapisani_uzytkownicy.count()

    def czy_uzytkownik_zapisany(self, uzytkownik):
        if not uzytkownik.is_authenticated:
            return False
        return self.zapisani_uzytkownicy.filter(uzytkownik=uzytkownik).exists()

class Zapisy(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, limit_choices_to={'rola': 'KLUBOWICZ'}, related_name='moje_zapisy')
    zajecia = models.ForeignKey(Zajecia, on_delete=models.CASCADE, related_name='zapisani_uzytkownicy')
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uzytkownik', 'zajecia') # Blokada ponownego zapisu na te same zajęcia
        verbose_name = "Zapis na zajęcia"
        verbose_name_plural = "Zapisy na zajęcia"

    def __str__(self):
        return f"{self.uzytkownik.last_name} -> {self.zajecia.nazwa}"

class PlanTreningowy(models.Model):
    trener = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, limit_choices_to={'rola': 'TRENER'}, related_name='utworzone_plany')
    podopieczny = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE, limit_choices_to={'rola': 'KLUBOWICZ'}, related_name='plany_treningowe')
    opis_treningu = models.TextField()
    data_utworzenia = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan treningowy"
        verbose_name_plural = "Plany treningowe"

    def __str__(self):
        return f"Plan dla {self.podopieczny.last_name} od trenera {self.trener.last_name}"