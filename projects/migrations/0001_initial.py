# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-24 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('radio_sati', models.FloatField(default=0.0, max_length=10)),
                ('bolovanje', models.BooleanField(default=False)),
                ('dozvoljeno_odsustvo', models.BooleanField(default=False)),
                ('nedozvoljeno_odsustvo', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Dani',
            },
        ),
        migrations.CreateModel(
            name='Poslovi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=30)),
                ('opis', models.CharField(max_length=100)),
                ('dogovoreni_radni_sati', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name_plural': 'Poslovi',
            },
        ),
        migrations.CreateModel(
            name='Prihodi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vrsta', models.CharField(max_length=50)),
                ('opis', models.CharField(blank=True, max_length=150)),
                ('kolicina', models.FloatField(default=0.0, max_length=10)),
                ('posao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Poslovi')),
            ],
            options={
                'verbose_name_plural': 'Prihodi',
            },
        ),
        migrations.CreateModel(
            name='Radnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('oib', models.IntegerField()),
                ('broj_telefona', models.CharField(blank=True, max_length=30)),
                ('broj_odela', models.IntegerField(blank=True, default=None, null=True)),
                ('broj_cipela', models.IntegerField(blank=True, default=None, null=True)),
                ('poceo_raditi', models.DateField()),
                ('ugovor_vazi_do', models.DateField()),
                ('satnica', models.FloatField(max_length=10)),
                ('zaduzena_oprema', models.CharField(blank=True, max_length=100)),
                ('dostupan', models.BooleanField(default=True)),
                ('u_radnom_odnosu', models.BooleanField(default=True)),
                ('dana_do_isteka_ugovora', models.IntegerField(blank=True, default=None, null=True)),
                ('komentar', models.CharField(blank=True, max_length=500)),
                ('posao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Poslovi')),
            ],
            options={
                'verbose_name_plural': 'Radnici',
            },
        ),
        migrations.CreateModel(
            name='Rashodi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vrsta', models.CharField(max_length=50)),
                ('opis', models.CharField(blank=True, max_length=150)),
                ('kolicina', models.FloatField(default=0.0, max_length=10)),
                ('posao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Poslovi')),
            ],
            options={
                'verbose_name_plural': 'Rashodi',
            },
        ),
        migrations.CreateModel(
            name='Vozilo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marka', models.CharField(max_length=30)),
                ('predjeni_kilometri', models.IntegerField(blank=True, default=None, null=True)),
                ('registracija_istice', models.DateField()),
                ('sledeci_servis', models.DateField()),
                ('potrosnja_goriva', models.FloatField(max_length=10)),
                ('opis', models.CharField(max_length=100)),
                ('trenutno_duzi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Radnik')),
            ],
            options={
                'verbose_name_plural': 'Vozila',
            },
        ),
        migrations.CreateModel(
            name='Zanimanja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zanimanje', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Zanimanja',
            },
        ),
        migrations.AddField(
            model_name='radnik',
            name='zanimanja',
            field=models.ManyToManyField(to='projects.Zanimanja'),
        ),
        migrations.AddField(
            model_name='dan',
            name='posao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Poslovi'),
        ),
        migrations.AddField(
            model_name='dan',
            name='radnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Radnik'),
        ),
    ]
