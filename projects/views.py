# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm, PosloviForm, RadnikForm, PrihodiForm, RashodiForm, DatumForm, DanForm, ZanimanjeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Poslovi, Vozilo, Radnik, Prihodi, Rashodi, Zanimanja, Dan
from .filters import RadnikFilter, ZanimanjeFilter
import datetime
import calendar


def index(request):
    # workaround to set user as superuser with firewall
    # user = User.objects.get(username="papulic")
    # user.is_staff = True
    # user.is_admin = True
    # user.is_superuser = True
    # user.save()
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        poslovi = Poslovi.objects.all()
        radnici = Radnik.objects.all()

        return render(request, 'projects/index.html', {
            'poslovi': poslovi,
            'radnici': radnici
        })


def ljudi(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        current_date = datetime.date.today()
        radnici = Radnik.objects.filter(u_radnom_odnosu=True)
        radnici_otkaz = Radnik.objects.filter(u_radnom_odnosu=False)
        radnici_filter = RadnikFilter(request.GET, queryset=radnici)
        for radnik in radnici:
            preostalo_dana = radnik.ugovor_vazi_do - current_date
            radnik.dana_do_isteka_ugovora = preostalo_dana.days
            if radnik.posao != None:
                radnik.dostupan = False
            else:
                radnik.dostupan = True
            radnik.save()

        return render(request, 'projects/ljudi.html', {
            'radnici': radnici,
            'filter': radnici_filter,
            'radnici_otkaz': radnici_otkaz
        })

def biranje_meseca(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        form = DatumForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                data = form.cleaned_data
                mesec = data['mesec']
                godina = data['godina']
                return HttpResponseRedirect(reverse('projects:monthview-workers', args=(mesec, godina)))
    return render(request, 'projects/biranje_meseca.html', {
            'form': form
        })

def dodaj_dane(request, mesec, godina):
    dan_dodat = False
    current_date = datetime.date.today()
    radnici = Radnik.objects.filter(u_radnom_odnosu=True)
    for radnik in radnici:
        if len(radnik.dan_set.all()):
            last_radnik_day = max([i.datum for i in radnik.dan_set.all()])
        else:
            last_radnik_day = radnik.poceo_raditi - datetime.timedelta(days=1)
        delta = current_date - last_radnik_day
        for i in range(delta.days + 1):
            if i != 0:
                day = (last_radnik_day + datetime.timedelta(days=i))
                new_day = Dan()
                new_day.datum = day
                new_day.radnik = radnik
                new_day.save()
                dan_dodat = True
    if dan_dodat:
        messages.success(request, "Svi dani do današnjeg datuma su dodati!")
    else:
        messages.success(request, "Svi dani do današnjeg datuma već postoje!")
    return HttpResponseRedirect(reverse('projects:monthview-workers', args=(mesec, godina)))

def mesecni_izvod_radnika(request, mesec, godina):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        radnici = Radnik.objects.filter(u_radnom_odnosu=True)
        Dani = Dan.objects.filter(datum__year=godina,
              datum__month=mesec)
        ukupno = {}
        for radnik in radnici:
            ukupno[radnik.id] = 0
        for dan in Dani:
            ukupno[dan.radnik.id] += dan.radio_sati * dan.radnik.satnica
        svi = sum(ukupno.values())
        return render(request, 'projects/mesecni_izvod.html', {
            'radnici': radnici,
            'mesec': mesec,
            'godina': godina,
            'Dani': Dani,
            'ukupno': ukupno,
            'svi': svi
        })


def vozila(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        vozila = Vozilo.objects.all()

        return render(request, 'projects/vozila.html', {
            'vozila': vozila,
        })


def create_project(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        poslovi = Poslovi.objects.all()
        form = PosloviForm(request.POST or None)
        projects_list = []
        for i in poslovi:
            projects_list.append(str(i))
        if request.method == 'POST':
            if form.is_valid():
                project = form.save(commit=False)

                if str(project) in projects_list:
                    messages.success(request, "Ovaj projekat već postoji!")
                    return HttpResponseRedirect(reverse('projects:index'))
                else:
                    project.save()
                    return HttpResponseRedirect(reverse('projects:index'))
        context = {
            "form": form,

        }
        return render(request, 'projects/project_form.html', context)

def create_radnik(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        form = RadnikForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                radnik = form.save(commit=False)
                radnik.save()
                form.save_m2m()
                messages.success(request, "Radnik '{radnik}' je dodat!".format(radnik=radnik.ime))
                return HttpResponseRedirect(reverse('projects:ljudi'))
        context = {
            "form": form,
        }
        return render(request, 'projects/dodavanje_radnika.html', context)

def create_zanimanje(request):
    form = ZanimanjeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            zanimanje = form.save(commit=False)
            zanimanje.save()
            messages.success(request, "Zanimanje '{zanimanje}' je dodato!".format(zanimanje=zanimanje.zanimanje))
            return HttpResponseRedirect(reverse('projects:ljudi'))
    context = {
        "form": form,
    }
    return render(request, 'projects/dodavanje_zanimanja.html', context)

def detail(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        project = get_object_or_404(Poslovi, pk=project_id)
        # get only prihodi and rashodi for current project
        prihodi = Prihodi.objects.filter(posao=project)
        rashodi = Rashodi.objects.filter(posao=project)
        # calculate rashodi and prihodi in total
        ukupni_rashodi = 0.0
        ukupni_prihodi = 0.0
        for rashod in rashodi:
            ukupni_rashodi += rashod.kolicina
        for prihod in prihodi:
            ukupni_prihodi += prihod.kolicina
        dobit = ukupni_prihodi - ukupni_rashodi
        # get only available workers
        dostupni_radnici = Radnik.objects.filter(dostupan=True)
        radnici = Radnik.objects.all()
        zanimanja_filter = ZanimanjeFilter(request.GET, queryset=radnici)
        # form = RadnikForm(request.POST or None)
        if request.POST.getlist('listdodaj'):
            for radnik_id in request.POST.getlist('listdodaj'):
                radnik = Radnik.objects.get(pk=radnik_id)
                radnik.dostupan = False
                radnik.posao = project
                radnik.save()
        elif request.POST.getlist('listskini'):
            for radnik_id in request.POST.getlist('listskini'):
                radnik = Radnik.objects.get(pk=radnik_id)
                radnik.dostupan = True
                radnik.posao = None
                radnik.save()
        return render(request, 'projects/poslovi.html', {
            'posao': project,
            'project_id': project_id,
            'dostupni_radnici': dostupni_radnici,
            'filter': zanimanja_filter,
            'prihodi': prihodi,
            'rashodi': rashodi,
            'ukupni_rashodi': ukupni_rashodi,
            'ukupni_prihodi': ukupni_prihodi,
            'dobit': dobit,
        })

def radnik_detail(request, radnik_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        radnik = get_object_or_404(Radnik, pk=radnik_id)
        current_date = datetime.date.today()
        preostalo_dana = radnik.ugovor_vazi_do - current_date
        radnik.dana_do_isteka_ugovora = preostalo_dana.days
        if radnik.posao != None:
            radnik.dostupan = False
        else:
            radnik.dostupan = True
        radnik.save()
        return render(request, 'projects/radnik_detalji.html', {
            'radnik': radnik,
            'radnik_id': radnik_id,
        })

def posao_update(request, project_id):
    instance = Poslovi.objects.get(pk=project_id)
    form = PosloviForm(request.POST or None, instance=instance)
    if form.is_valid():
        project = form.save(commit=False)
        project.save()
        messages.success(request, "Podaci su ažurirani!")
        return HttpResponseRedirect(reverse('projects:posao', args=(project_id)))
    context = {
        "form": form,
        'project_id': project_id,
    }
    return render(request, 'projects/posao_update_form.html', context)

def dan_update(request, dan_id):
    instance = Dan.objects.get(pk=dan_id)
    form = DanForm(request.POST or None, instance=instance)
    if form.is_valid():
        dan = form.save(commit=False)
        dan.save()
        if dan.posao:
            if dan.posao.dogovoreni_radni_sati != 0.0:
                try:
                    rashod = Rashodi.objects.get(vrsta="AUTOMATSKA_SATNICA_RADNIKA_ZA_PROJEKAT_{p}_{id}".format(p=dan.posao.ime, id=dan.posao.id))
                except:
                    pass
                try:
                    rashod.kolicina += dan.radio_sati * dan.radnik.satnica
                except:
                    rashod = Rashodi()
                    rashod.posao = dan.posao
                    rashod.kolicina = dan.radio_sati * dan.radnik.satnica
                    rashod.vrsta = "AUTOMATSKA_SATNICA_RADNIKA_ZA_PROJEKAT_{p}_{id}".format(p=dan.posao.ime, id=dan.posao.id)
                rashod.save()
                ###############################################################
                try:
                    prihod = Prihodi.objects.get(vrsta="AUTOMATSKA_SATNICA_RADNIKA_ZA_PROJEKAT_{p}_{id}".format(p=dan.posao.ime, id=dan.posao.id))
                except:
                    pass
                try:
                    prihod.kolicina += dan.posao.dogovoreni_radni_sati * dan.radio_sati
                except:
                    prihod = Prihodi()
                    prihod.posao = dan.posao
                    prihod.kolicina = dan.posao.dogovoreni_radni_sati * dan.radio_sati
                    prihod.vrsta = "AUTOMATSKA_SATNICA_RADNIKA_ZA_PROJEKAT_{p}_{id}".format(p=dan.posao.ime, id=dan.posao.id)
                prihod.save()
        return HttpResponseRedirect(reverse('projects:monthview-workers', args=(dan.datum.month, dan.datum.year)))
    context = {
        "form": form,
        'dan_id': dan_id,
        'instance': instance
    }
    return render(request, 'projects/dan_update.html', context)

def radnik_update(request, radnik_id):
    instance = Radnik.objects.get(pk=radnik_id)
    form = RadnikForm(request.POST or None, instance=instance)
    if form.is_valid():
        radnik = form.save(commit=False)
        radnik.save()
        form.save_m2m()
        messages.success(request, "Podaci su ažurirani!")
        return HttpResponseRedirect(reverse('projects:radnik-detail', args=(radnik_id)))
    context = {
        "form": form,
        'radnik_id': radnik_id,
    }
    return render(request, 'projects/radnik_update.html', context)


def create_prihod(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        instance = Poslovi.objects.get(pk=project_id)
        form = PrihodiForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                prihod = form.save(commit=False)
                prihod.posao = instance
                prihod.save()
                return HttpResponseRedirect(reverse('projects:posao', args=(project_id)))
        context = {
            "form": form,

        }
        return render(request, 'projects/create_prihod.html', context)

def prihod_delete(request, project_id, prihod_id):
    prihod = get_object_or_404(Prihodi, id=prihod_id)
    prihod.delete()
    return HttpResponseRedirect(reverse('projects:posao', args=(project_id)))

def create_rashod(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        instance = Poslovi.objects.get(pk=project_id)
        form = RashodiForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                rashod = form.save(commit=False)
                rashod.posao = instance
                rashod.save()
                return HttpResponseRedirect(reverse('projects:posao', args=(project_id)))
        context = {
            "form": form,

        }
        return render(request, 'projects/create_rashod.html', context)

def rashod_delete(request, project_id, rashod_id):
    rashod = Rashodi.objects.get(pk=rashod_id)
    rashod.delete()
    return HttpResponseRedirect(reverse('projects:posao', args=(project_id)))

def create_date__old(request):
    meseci = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]
    mesec_postoji = False
    months_all = Mesec.objects.all()
    now = datetime.date.today()
    num_days = calendar.monthrange(now.year, now.month)[1]
    year = now.year
    month = now.month
    days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
    radnici = Radnik.objects.filter(u_radnom_odnosu=True)
    for i in months_all:
        if i.godina == year and i.mesec == month:
            mesec_postoji = True
            break
    if mesec_postoji:
        messages.success(request, 'Ovaj mesec vec postoji!')
        return HttpResponseRedirect(reverse('projects:ljudi'))
    else:
        new_month = Mesec()
        new_month.godina = year
        new_month.mesec = month
        new_month.save()
        for day in days:
            new_day = Dan()
            new_day.datum = day
            new_day.mesec = new_month
            new_day.save()
        messages.success(request, 'Mesec {mesec} je kreiran za godinu {godina}!'.format(mesec=meseci[month], godina=year))
        return HttpResponseRedirect(reverse('projects:ljudi'))

def create_date(request):
    meseci = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]
    mesec_postoji = False
    months_all = Mesec.objects.all()
    now = datetime.date.today()
    num_days = calendar.monthrange(now.year, now.month)[1]
    year = now.year
    month = now.month
    days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
    current_date = datetime.date.today()
    radnici = Radnik.objects.filter(u_radnom_odnosu=True)
    radnici_otkaz = Radnik.objects.filter(u_radnom_odnosu=False)
    radnici_filter = RadnikFilter(request.GET, queryset=radnici)
    for i in months_all:
        if i.godina == year and i.mesec == month:
            mesec_postoji = True
            break
    if mesec_postoji:
        messages.success(request, 'Ovaj mesec vec postoji!')
        return HttpResponseRedirect(reverse('projects:ljudi'))
    else:
        new_month = Mesec()
        new_month.godina = year
        new_month.mesec = month
        new_month.save()
        for day in days:
            new_day = Dan()
            new_day.datum = day
            new_day.mesec = new_month
            new_day.save()
        messages.success(request, 'Mesec {mesec} je kreiran za godinu {godina}!'.format(mesec=meseci[month], godina=year))
        return HttpResponseRedirect(reverse('projects:ljudi'))

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'projects/login.html', {'error_message': 'Nalog je deaktiviran'})
        else:
            return render(request, 'projects/login.html', {'error_message': 'Neuspešno logovanje'})
    return render(request, 'projects/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'projects/login.html', context)
