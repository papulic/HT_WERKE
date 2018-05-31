# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Radnik, Vozilo, Poslovi, Prihodi, Rashodi, Zanimanja, Dan, Akontacije


#class RadniciInline(admin.TabularInline):
 #   model = RadniciZanimanja
  #  extra = 1

class ZanimanjaModelAdmin(admin.ModelAdmin):
    #inlines = (RadniciInline,)
    list_display = ["zanimanje"]

class DanModelAdmin(admin.ModelAdmin):
    list_display = ["radnik", "datum"]
    list_filter = ["datum"]

class RadnikModelAdmin(admin.ModelAdmin):
    #inlines = (RadniciInline,)
    list_display = ["ime", "poceo_raditi", "ugovor_vazi_do", "satnica", "zaduzena_oprema", "dostupan"]
    list_filter = ["u_radnom_odnosu"]

class VoziloModelAdmin(admin.ModelAdmin):
    list_display = ["marka", "predjeni_kilometri", "registracija_istice", "sledeci_servis", "potrosnja_goriva", "opis", "trenutno_duzi"]
    list_filter = ['marka', 'registracija_istice']

class PosloviModelAdmin(admin.ModelAdmin):
    list_display = ["ime", "opis", "dogovoreni_radni_sati"]
    list_filter = ["ime"]

class PrihodiModelAdmin(admin.ModelAdmin):
    list_display = ["vrsta", "kolicina", "posao"]
    list_filter = ["vrsta", "posao"]

class RashodiModelAdmin(admin.ModelAdmin):
    list_display = ["vrsta", "kolicina", "posao"]
    list_filter = ["vrsta", "posao"]

class AkontacijeModelAdmin(admin.ModelAdmin):
    list_display = ["godina", "mesec", "kolicina"]
    list_filter = ["godina", "mesec"]




admin.site.register(Radnik, RadnikModelAdmin)
admin.site.register(Vozilo, VoziloModelAdmin)
admin.site.register(Poslovi, PosloviModelAdmin)
admin.site.register(Prihodi, PrihodiModelAdmin)
admin.site.register(Rashodi, RashodiModelAdmin)
admin.site.register(Zanimanja, ZanimanjaModelAdmin)
admin.site.register(Dan, DanModelAdmin)
admin.site.register(Akontacije, AkontacijeModelAdmin)
