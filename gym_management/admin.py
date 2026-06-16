from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Uzytkownik, Karnet, Zajecia, Zapisy, PlanTreningowy

class CustomUserAdmin(UserAdmin):
    model = Uzytkownik

    fieldsets = UserAdmin.fieldsets + (
        ('Informacje klubowe', {'fields': ('rola', 'zdjecie_identyfikacyjne')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dodatkowe informacje', {
            'fields': ('email', 'first_name', 'last_name', 'rola'),
        }),
    )
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'rola', 'is_staff']
    list_filter = ['rola', 'is_staff', 'is_active']

admin.site.register(Uzytkownik, CustomUserAdmin)
admin.site.register(Karnet)
admin.site.register(Zajecia)
admin.site.register(Zapisy)
admin.site.register(PlanTreningowy)