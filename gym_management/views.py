from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db import models
from django.utils import timezone  

from .models import Zajecia, Zapisy, Karnet, PlanTreningowy, Uzytkownik
from .decorators import wymaga_roli
from .forms import RejestracjaForm


def index(request):
    return render(request, 'gym/index.html')


def publiczny_grafik(request):
    zajecia = Zajecia.objects.filter(data_czas__gte=timezone.now()).order_by('data_czas')

    zapisane_zajecia_ids = []
    if request.user.is_authenticated and request.user.rola == 'KLUBOWICZ':
        zapisane_zajecia_ids = Zapisy.objects.filter(uzytkownik=request.user).values_list('zajecia_id', flat=True)
        
    return render(request, 'gym/grafik.html', {
        'zajecia': zajecia,
        'zapisane_zajecia_ids': zapisane_zajecia_ids
    })


@login_required
@wymaga_roli('KLUBOWICZ')
def panel_klubowicza(request):
    karnety = Karnet.objects.filter(uzytkownik=request.user).order_by('-data_do')
    moje_zapisy = Zapisy.objects.filter(uzytkownik=request.user)
    plany = PlanTreningowy.objects.filter(podopieczny=request.user)
    
    return render(request, 'gym/panel_klubowicza.html', {
        'karnety': karnety,
        'moje_zapisy': moje_zapisy,
        'plany': plany
    })


@login_required
@wymaga_roli('KLUBOWICZ')
def zapisz_na_zajecia(request, zajecia_id):
    zajecia = get_object_or_404(Zajecia, id=zajecia_id)
    if zajecia.wolne_miejsca > 0:
        Zapisy.objects.get_or_create(uzytkownik=request.user, zajecia=zajecia)
        messages.success(request, f"Zapisano na zajęcia {zajecia.nazwa}!")
    else:
        messages.error(request, "Brak wolnych miejsc!")
    return redirect('publiczny_grafik')


@login_required
@wymaga_roli('KLUBOWICZ')
def wypisz_z_zajec(request, zajecia_id):
    zajecia = get_object_or_404(Zajecia, id=zajecia_id)
    zapis = Zapisy.objects.filter(uzytkownik=request.user, zajecia=zajecia).first()
    
    if zapis:
        zapis.delete()
        messages.success(request, f"Wypisano Cię z zajęć {zajecia.nazwa}.")
    else:
        messages.error(request, "Nie byłeś zapisany na te zajęcia.")
        
    return redirect('publiczny_grafik')


from .forms import PlanTreningowyForm

@login_required
@wymaga_roli('TRENER')
def panel_trenera(request):
    podopieczni = Uzytkownik.objects.filter(plany_treningowe__trener=request.user).distinct()
    
    if request.method == 'POST':
        form = PlanTreningowyForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trener = request.user
            plan.save()
            messages.success(request, f"Pomyślnie dodano nowy plan dla podopiecznego!")
            return redirect('panel_trenera')
    else:
        form = PlanTreningowyForm()

    return render(request, 'gym/panel_trenera.html', {
        'podopieczni': podopieczni,
        'form': form
    })

@login_required
@wymaga_roli('RECEPCJA', 'ADMIN')
def panel_recepcji(request):
    query = request.GET.get('q')
    szukany_uzytkownik = None
    aktualny_karnet = None

    if query:
        szukany_uzytkownik = Uzytkownik.objects.filter(
            models.Q(last_name__icontains=query) | models.Q(email__icontains=query)
        ).first()
        
        if szukany_uzytkownik:
            aktualny_karnet = Karnet.objects.filter(uzytkownik=szukany_uzytkownik).order_by('-data_do').first()

    return render(request, 'gym/panel_recepcji.html', {
        'szukany_uzytkownik': szukany_uzytkownik,
        'aktualny_karnet': aktualny_karnet,
        'query': query
    })


def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja pomyślna! Witamy w klubie.")
            return redirect('index')
    else:
        form = RejestracjaForm()
    return render(request, 'gym/rejestracja.html', {'form': form})