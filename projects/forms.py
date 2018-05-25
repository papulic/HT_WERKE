from django import forms
from django.contrib.auth.models import User
from .models import Poslovi, Vozilo, Radnik, Prihodi, Rashodi, Dan, Zanimanja

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class ZanimanjeForm(forms.ModelForm):
    class Meta:
        model = Zanimanja
        fields = ['zanimanje']

class PosloviForm(forms.ModelForm):
    class Meta:
        model = Poslovi
        fields = ['ime', 'opis', 'dogovoreni_radni_sati']

class RadnikForm(forms.ModelForm):
    poceo_raditi = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': "datum"}), input_formats=('%d.%m.%Y', '%d/%m/%Y', '%d.%m.%y', '%d/%m/%y'))
    ugovor_vazi_do = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': "datum"}), input_formats=('%d.%m.%Y', '%d/%m/%Y', '%d.%m.%y', '%d/%m/%y'))
    class Meta:
        model = Radnik
        fields = ['ime', 'oib', 'poceo_raditi', 'ugovor_vazi_do', 'satnica', 'broj_telefona', 'broj_odela', 'broj_cipela', 'zaduzena_oprema', 'posao', 'zanimanja', 'u_radnom_odnosu', 'komentar']
        widgets = {
            'zanimanja': forms.CheckboxSelectMultiple,
            'komentar': forms.Textarea
        }

class RadnikForm__old(forms.ModelForm):
    class Meta:
        model = Radnik
        fields = ['ime', 'oib', 'poceo_raditi', 'ugovor_vazi_do', 'satnica', 'broj_telefona', 'broj_odela', 'broj_cipela', 'zaduzena_oprema', 'posao', 'zanimanja']
        widgets = {
            'poceo_raditi': DateInput(),
            'ugovor_vazi_do': DateInput(),
            'zanimanja': forms.CheckboxSelectMultiple
        }

class PrihodiForm(forms.ModelForm):
    class Meta:
        model = Prihodi
        fields = ['vrsta', 'opis', 'kolicina']

class RashodiForm(forms.ModelForm):
    class Meta:
        model = Rashodi
        fields = ['vrsta', 'opis', 'kolicina']

class DatumForm(forms.Form):
    mesec = forms.IntegerField(max_value=12, min_value=1)
    godina = forms.IntegerField(label="godina")

class DanForm(forms.ModelForm):
    class Meta:
        model = Dan
        fields = ['posao', 'radio_sati', 'bolovanje', 'dozvoljeno_odsustvo', 'nedozvoljeno_odsustvo']
