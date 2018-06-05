# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Poslovi, Vozilo, Radnik, Prihodi, Rashodi, Zanimanja, Dan, Akontacije, Komentar
from django.test import TestCase
import datetime

class DanTestCase(TestCase):
    def napravi_1000_dana(self):
        current_date = datetime.date.today()
        radnik = Radnik.objects.create(oib=32, ime="dhaskdgbkjas", poceo_raditi=current_date, ugovor_vazi_do=current_date, satnica=30)
        for i in range(0, 1000):
            Dan.objects.create(datum=current_date, radnik=radnik)
        dani = Dan.objects.all()
        for dan in dani:
            print dan.pk
