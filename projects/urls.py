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
    url(r'^mesecni_izvod_radnika/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)/(?P<posao_id>[0-9]+)$', views.mesecni_izvod_radnika, name='monthview-workers'),
    url(r'^posao/(?P<project_id>[0-9]+)/$', views.detail, name='posao'),
    url(r'^radnik/(?P<radnik_id>[0-9]+)/$', views.radnik_detail, name='radnik-detail'),
    url(r'^vozilo/(?P<vozilo_id>[0-9]+)/$', views.vozilo_detail, name='vozilo-detail'),
    url(r'^azuriranje_posla/(?P<project_id>[0-9]+)/$', views.posao_update, name='posao-update'),
    url(r'^azuriranje_radnika/(?P<radnik_id>[0-9]+)/$', views.radnik_update, name='radnik-update'),
    url(r'^azuriranje_dana/(?P<dan_id>[0-9]+)/$', views.dan_update, name='dan-update'),
    url(r'^azuriranje_vozila/(?P<vozilo_id>[0-9]+)/$', views.vozilo_update, name='vozilo-update'),
    url(r'^novi_prihod/(?P<project_id>[0-9]+)/$', views.create_prihod, name='prihod-add'),
    url(r'^novi_rashod/(?P<project_id>[0-9]+)/$', views.create_rashod, name='rashod-add'),
    url(r'^novo_zanimanje/$', views.create_zanimanje, name='zanimanje-add'),
    url(r'^novi_radnik/$', views.create_radnik, name='radnik-add'),
    url(r'^novo_vozilo/$', views.create_vozilo, name='vozilo-add'),
    url(r'^posao/(?P<project_id>[0-9]+)/obrisi_prihod/(?P<prihod_id>[0-9]+)/$', views.prihod_delete, name='prihod-delete'),
    url(r'^(?P<project_id>[0-9]+)/obrisi_rashod/(?P<rashod_id>[0-9]+)/$', views.rashod_delete, name='rashod-delete'),
    url(r'^biranje_meseca/$', views.biranje_meseca, name='biranje_meseca'),
    url(r'^dodaj_dane/(?P<mesec>[0-9]+)/(?P<godina>[0-9]+)$', views.dodaj_dane, name='dodaj_dane')
]
