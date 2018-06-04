from django.conf.urls import url
from . import views


app_name = 'projects'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^radnici/$', views.ljudi, name='ljudi'),
    url(r'^vozila/$', views.vozila, name='vozila'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^novi_projekat/$', views.create_project, name='project-add'),
    url(r'^mesecni_pregled_radnika/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)/(?P<posao_id>[a-zA-Z0-9_.-]+)$', views.mesecni_izvod_radnika, name='monthview-workers'),  # samo string (?P<posao>[\w\-]+)
    url(r'^mesecni_pregled_poslova/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)$', views.mesecni_izvod_poslova, name='monthview-projects'),
    url(r'^posao/(?P<project_id>[0-9]+)/$', views.detail, name='posao'),
    url(r'^radnik/(?P<radnik_id>[0-9]+)/$', views.radnik_detail, name='radnik-detail'),
    url(r'^vozilo/(?P<vozilo_id>[0-9]+)/$', views.vozilo_detail, name='vozilo-detail'),
    url(r'^komentar/(?P<komentar_id>[0-9]+)/$', views.komentar_detail, name='komentar-detail'),
    url(r'^azuriranje_posla/(?P<project_id>[0-9]+)/$', views.posao_update, name='posao-update'),
    url(r'^azuriranje_radnika/(?P<radnik_id>[0-9]+)/$', views.radnik_update, name='radnik-update'),
    url(r'^azuriranje_dana/(?P<dan_id>[0-9]+)/(?P<posao_id>[a-zA-Z0-9_.-]+)$', views.dan_update, name='dan-update'),
    url(r'^azuriranje_akontacije/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)/(?P<posao_id>[a-zA-Z0-9_.-]+)/(?P<akontacija_id>[0-9]+)$', views.akontacija_update, name='akontacija-update'),
    url(r'^azuriranje_vozila/(?P<vozilo_id>[0-9]+)/$', views.vozilo_update, name='vozilo-update'),
    url(r'^izmena_komentara/(?P<komentar_id>[0-9]+)/$', views.komentar_update, name='komentar-update'),
    url(r'^novi_prihod/(?P<project_id>[0-9]+)/$', views.create_prihod, name='prihod-add'),
    url(r'^novi_rashod/(?P<project_id>[0-9]+)/$', views.create_rashod, name='rashod-add'),
    url(r'^novi_kvadrati/(?P<project_id>[0-9]+)/$', views.create_kvadrat, name='kvadrat-add'),
    url(r'^novi_komentar/(?P<project_id>[0-9]+)/$', views.create_komentar, name='komentar-add'),
    url(r'^novo_zanimanje/$', views.create_zanimanje, name='zanimanje-add'),
    url(r'^novi_radnik/$', views.create_radnik, name='radnik-add'),
    url(r'^novo_vozilo/$', views.create_vozilo, name='vozilo-add'),
    url(r'^posao/(?P<project_id>[0-9]+)/obrisi_prihod/(?P<prihod_id>[0-9]+)/$', views.prihod_delete, name='prihod-delete'),
    url(r'^(?P<project_id>[0-9]+)/obrisi_rashod/(?P<rashod_id>[0-9]+)/$', views.rashod_delete, name='rashod-delete'),
    url(r'^(?P<project_id>[0-9]+)/obrisi_komentar/(?P<komentar_id>[0-9]+)/$', views.komentar_delete, name='komentar-delete'),
    url(r'^obrisi_posao/(?P<posao_id>[0-9]+)/$', views.posao_delete, name='posao-delete'),
    url(r'^biranje_meseca/$', views.biranje_meseca, name='biranje_meseca'),
    url(r'^biranje_meseca_finansije/$', views.biranje_meseca_za_finansije, name='biranje_meseca_finansije'),
    url(r'^dodaj_dane/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)/(?P<posao_id>[a-zA-Z0-9_.-]+)$', views.dodaj_dane, name='dodaj_dane'),
    url(r'^pdf/(?P<posao_id>[0-9]+)$', views.pdf_posao, name='pdf_posao')
]
