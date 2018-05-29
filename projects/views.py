# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm, PosloviForm, RadnikForm, PrihodiForm, RashodiForm, DatumForm, DanForm, ZanimanjeForm, VoziloForm
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
                posao_ime = data['posao']
                if posao_ime == None:
                    posao_id = 0
                else:
                    posao = Poslovi.objects.get(ime=posao_ime)
                    posao_id = posao.id
                return HttpResponseRedirect(reverse('projects:monthview-workers', args=(mesec, godina, posao_id)))
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


def mesecni_izvod_radnika(request, mesec, godina, posao_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        if posao_id == '0':
            radnici = Radnik.objects.filter(u_radnom_odnosu=True)
        else:
            posao = Poslovi.objects.get(id=posao_id)
            radnici = Radnik.objects.filter(u_radnom_odnosu=True, posao=posao)
        Dani = Dan.objects.filter(datum__year=godina,
              datum__month=mesec)
        ukupno = {}
        dana_bolovanja = {}
        radnih_sati = {}
        slobodnih_dana = {}
        for radnik in radnici:
            ukupno[radnik.id] = 0
            dana_bolovanja[radnik.id] = 0
            radnih_sati[radnik.id] = 0
            slobodnih_dana[radnik.id] = 0
        for dan in Dani:
            ukupno[dan.radnik.id] += dan.radio_sati * dan.radnik.satnica
            radnih_sati[dan.radnik.id] += dan.radio_sati
            if dan.bolovanje:
                dana_bolovanja[dan.radnik.id] += 1
            if dan.dozvoljeno_odsustvo:
                slobodnih_dana[dan.radnik.id] += 1

        svi = sum(ukupno.values())
        return render(request, 'projects/mesecni_izvod.html', {
            'radnici': radnici,
            'mesec': mesec,
            'godina': godina,
            'Dani': Dani,
            'ukupno': ukupno,
            'svi': svi,
            'dana_bolovanja': dana_bolovanja,
            'radnih_sati': radnih_sati,
            'slobodnih_dana': slobodnih_dana
        })


def vozila(request):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        current_date = datetime.date.today()
        vozila = Vozilo.objects.all()
        istek_registracije = {}
        for vozilo in vozila:
            preostalo_dana = vozilo.registracija_istice - current_date
            istek_registracije[vozilo.id] = preostalo_dana.days

        return render(request, 'projects/vozila.html', {
            'vozila': vozila,
            'istek_registracije': istek_registracije
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


def create_vozilo(request):
    form = VoziloForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            vozilo = form.save(commit=False)
            vozilo.save()
            messages.success(request, "Vozilo '{vozilo}' je dodato!".format(vozilo=vozilo.marka))
            return HttpResponseRedirect(reverse('projects:vozila'))
    context = {
        "form": form,
    }
    return render(request, 'projects/dodavanje_vozila.html', context)


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


def vozilo_detail(request, vozilo_id):
    if not request.user.is_authenticated():
        return render(request, 'projects/login.html')
    else:
        vozilo = get_object_or_404(Vozilo, pk=vozilo_id)
        current_date = datetime.date.today()
        preostalo_dana = (vozilo.registracija_istice - current_date).days
        return render(request, 'projects/vozilo_detalji.html', {
            'vozilo': vozilo,
            'vozilo_id': vozilo_id,
            'preostalo_dana': preostalo_dana
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


def vozilo_update(request, vozilo_id):
    instance = Vozilo.objects.get(pk=vozilo_id)
    form = VoziloForm(request.POST or None, instance=instance)
    if form.is_valid():
        vozilo = form.save(commit=False)
        vozilo.save()
        messages.success(request, "Podaci su ažurirani!")
        return HttpResponseRedirect(reverse('projects:vozilo-detail', args=(vozilo_id)))
    context = {
        "form": form,
        'vozilo_id': vozilo_id,
    }
    return render(request, 'projects/vozilo_update.html', context)


def dan_update(request, dan_id):
    instance = Dan.objects.get(pk=dan_id)
    old_radio_sati = instance.radio_sati
    old_posao = instance.posao
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
                if old_radio_sati != 0.0 and rashod.kolicina != dan.radio_sati * dan.radnik.satnica and old_posao != None:
                    rashod.kolicina -= old_radio_sati * dan.radnik.satnica
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
                if old_radio_sati != 0.0 and prihod.kolicina != dan.posao.dogovoreni_radni_sati * dan.radio_sati and old_posao != None:
                    prihod.kolicina -= old_radio_sati * dan.posao.dogovoreni_radni_sati
                prihod.save()
        return HttpResponseRedirect(reverse('projects:monthview-workers', args=(dan.datum.month, dan.datum.year, dan.radnik.posao.id)))
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


def delete_posao_and_create_log(request, posao):
    pass


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
