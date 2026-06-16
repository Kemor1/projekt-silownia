from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Uzytkownik, PlanTreningowy

class RejestracjaForm(UserCreationForm):
    first_name = forms.CharField(label="Imię", required=True)
    last_name = forms.CharField(label="Nazwisko", required=True)
    email = forms.EmailField(label="Adres e-mail", required=True)
    
    class Meta(UserCreationForm.Meta):
        model = Uzytkownik
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'rola', 'zdjecie_identyfikacyjne')
        labels = {
            'rola': 'Kim jesteś w systemie?',
            'zdjecie_identyfikacyjne': 'Zdjęcie tożsamości (wymagane dla Klubowiczów do weryfikacji na recepcji)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rola'].choices = [
            ('KLUBOWICZ', 'Klubowicz'),
            ('TRENER', 'Trener Personalny'),
        ]

    from .models import PlanTreningowy

class PlanTreningowyForm(forms.ModelForm):
    class Meta:
        model = PlanTreningowy
        fields = ['podopieczny', 'opis_treningu']
        labels = {
            'podopieczny': 'Wybierz klubowicza:',
            'opis_treningu': 'Rozpiska treningowa (ćwiczenia, serie, powtórzenia):',
        }
        widgets = {
            'podopieczny': forms.Select(attrs={'class': 'w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-green-500'}),
            'opis_treningu': forms.Textarea(attrs={'rows': 5, 'class': 'w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-green-500', 'placeholder': 'np.\nPoniedziałek: Klatka + Przód barku...\n- Wyciskanie sztangi 4x8\n...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['podopieczny'].queryset = Uzytkownik.objects.filter(rola='KLUBOWICZ')