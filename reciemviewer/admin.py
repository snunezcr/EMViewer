# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>

from django.contrib import admin
from reciemviewer.models import Organization, Contact, Service


class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ('province', 'canton', 'district', 'type')
    inlines = Organization


class ContactAdmin(admin.ModelAdmin):
    list_filter = ('org', 'type')


class ServiceAdmin(admin.ModelAdmin):
    list_filter = ('org', 'type')


admin.site.register(Organization)
admin.site.register(Contact)
admin.site.register(Service)



