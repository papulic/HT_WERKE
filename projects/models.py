# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Poslovi(models.Model):
    ime = models.CharField(max_length=30)
    opis = models.CharField(max_length=100)
    dogovoreni_radni_sati = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.ime

    class Meta:
        verbose_name_plural = "Poslovi"

class Zanimanja(models.Model):
    zanimanje = models.CharField(max_length=30)

    def __unicode__(self):
        return self.zanimanje
    class Meta:
        verbose_name_plural = "Zanimanja"

class Radnik(models.Model):
    ime = models.CharField(max_length=50)
    oib = models.IntegerField()
    broj_telefona = models.CharField(max_length=30, blank=True)
    broj_odela = models.IntegerField(default=None, null=True, blank=True)
    broj_cipela = models.IntegerField(default=None, null=True, blank=True)
    poceo_raditi = models.DateField()
    ugovor_vazi_do = models.DateField()
    satnica = models.FloatField(max_length=10)
    zaduzena_oprema = models.CharField(max_length=100, blank=True)
    dostupan = models.BooleanField(default=True)
    posao = models.ForeignKey(Poslovi, null=True, blank=True)
    u_radnom_odnosu = models.BooleanField(default=True)
    zanimanja = models.ManyToManyField(Zanimanja)
    dana_do_isteka_ugovora = models.IntegerField(default=None, null=True, blank=True)
    komentar = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.ime

    class Meta:
        verbose_name_plural = "Radnici"




#class RadniciZanimanja(models.Model):
#    radnik = models.ForeignKey(Radnik, on_delete=models.CASCADE)
#    zanimanje = models.ForeignKey(Zanimanja, on_delete=models.CASCADE)

# created_at = models.DateTimeField(auto_now_add=True)
class Vozilo(models.Model):
    marka = models.CharField(max_length=30)
    predjeni_kilometri = models.IntegerField(default=None, null=True, blank=True)
    registracija_istice = models.DateField()
    sledeci_servis = models.DateField()
    potrosnja_goriva = models.FloatField(max_length=10)
    opis = models.CharField(max_length=100)
    trenutno_duzi = models.ForeignKey(Radnik, null=True, blank=True)


    def __unicode__(self):
        return self.marka

    class Meta:
        verbose_name_plural = "Vozila"

class Dan(models.Model):
    datum = models.DateField()
    radnik = models.ForeignKey(Radnik)
    posao = models.ForeignKey(Poslovi, null=True, blank=True)
    radio_sati = models.FloatField(max_length=10, default=0.0)
    bolovanje = models.BooleanField(default=False)
    dozvoljeno_odsustvo = models.BooleanField(default=False)
    nedozvoljeno_odsustvo = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.datum) + " - " + self.radnik.ime

    class Meta:
        verbose_name_plural = "Dani"

class Prihodi(models.Model):
    vrsta = models.CharField(max_length=50)
    opis = models.CharField(max_length=150, blank=True)
    kolicina = models.FloatField(max_length=10, default=0.0)
    posao = models.ForeignKey(Poslovi, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.vrsta

    class Meta:
        verbose_name_plural = "Prihodi"

class Rashodi(models.Model):
    vrsta = models.CharField(max_length=50)
    opis = models.CharField(max_length=150, blank=True)
    kolicina = models.FloatField(max_length=10, default=0.0)
    posao = models.ForeignKey(Poslovi, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.vrsta

    class Meta:
        verbose_name_plural = "Rashodi"

