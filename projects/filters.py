import django_filters
from .models import Radnik, Zanimanja
from .forms import RadnikForm




class RadnikFilter(django_filters.FilterSet):
    ugovor_vazi_do = django_filters.NumberFilter(name='ugovor_vazi_do', lookup_expr='year', label="Ugovor vazi do godine:")
    class Meta:
        model = Radnik
        fields = ['dostupan', 'posao', 'zanimanja']

class ZanimanjeFilter(django_filters.FilterSet):
    class Meta:
        model = Radnik
        fields = ['zanimanja']
