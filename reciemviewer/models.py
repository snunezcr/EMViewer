# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>

from django.db import models
from django.urls import reverse
from django.core.cache import cache, caches
from owslib.wms import WebMapService

class Organization(models.Model):
    short = models.CharField(max_length=10, help_text='Siglas')
    name = models.CharField(max_length=200, help_text='Nombre')
    address = models.TextField(max_length=500, help_text='Dirección física')
    province = models.CharField(max_length=20, help_text='Provincia', default="San José")
    canton = models.CharField(max_length=20, help_text='Cantón', default='San José')
    district = models.CharField(max_length=20, help_text='Distrito', default='El Carmen')
    phone = models.CharField(max_length=14, help_text='Número telefónico')
    url = models.URLField(max_length=300, help_text='Dirección web')

    OTYPE = (
        ('gov', 'Gubernamental'),
        ('soc', 'Sociedad civil'),
        ('edu', 'Educativa'),
        ('ong', 'Organización no gubernamental')
    )
    type = models.CharField(max_length=5, choices=OTYPE, default='soc', help_text='Tipo de organización')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-detail', args=[str(self.id)])


class Contact(models.Model):
    name = models.CharField(max_length=30, help_text="Nombre")
    flastn = models.CharField(max_length=30, help_text="Primer apellido")
    slastn = models.CharField(max_length=30, help_text="Segundo apellido")
    phone = models.CharField(max_length=14, help_text='Número telefónico')
    email = models.EmailField(max_length=200, help_text='Correo electrónico')
    org = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)

    CTYPE = (
        ('t', 'Técnico'),
        ('d', 'Toma de decisiones')
    )

    type = models.CharField(max_length=2, choices=CTYPE, default='t', help_text='Tipo de puesto')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contact-detail', args=[str(self.id)])


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    short = models.CharField(max_length=10, primary_key=False, help_text='Descriptor corto')
    name = models.CharField(max_length=200, help_text='Nombre de uso frecuente')
    url = models.URLField(max_length=300, help_text='URL')
    org = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, help_text='Organización')

    slist = []

    STYPE = (
        ('wms', 'Web Map Service'),
        ('wfs', 'Web Feature Service'),
    )

    type = models.CharField(max_length=5, choices=STYPE, default='wfs', help_text='Tipo de servicio')
    description = models.TextField(max_length=1000, help_text='Descripción de la capa')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-detail', args=[str(self.id)])

    def get_url(self):
        return self.url

    # We obtain the list of services as objects - uses cache
    def get_layer_list(self):
        slist = []

        if cache.get(self.url) is None:
            print('Obtaining data for the first time')
            if self.type == 'wms':
                try:
                    serwms = WebMapService(self.url)
                    # Only select those contents that are queriable
                    slist = list(filter(lambda x: x.queryable, list(serwms.contents.values())))
                    cache.set(self.url, slist)
                except Exception:
                    pass
            elif self.type == 'wfs':
                pass
            else:
                pass
        else:
            slist = cache.get(self.url)

        return slist

    # We obtain the list of services as objects - fills up cache
    def get_layer_list_cache(self):
        slist = []
        print(caches.all())
        if self.type == 'wms':
            try:
                serwms = WebMapService(self.url)
                # Only select those contents that are queriable
                slist = list(filter(lambda x: x.queryable, list(serwms.contents.values())))
                cache.set(self.url, slist)
            except Exception:
                pass
        elif self.type == 'wfs':
            pass
        else:
            pass

        return slist
