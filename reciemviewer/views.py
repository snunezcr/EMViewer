# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>
from rest_framework import generics
from reciemviewer.models import Organization, Contact, Service
from reciemviewer.serializers import OrganizationSerializer, ContactSerializer, ServiceSerializer
from django.shortcuts import render
from django.views import generic
import owslib.wms


def index(request):
    num_organizations = Organization.objects.all().count()
    num_services = Service.objects.all().count()
    num_contacts = Contact.objects.all().count()

    # TODO: add code to count layers

    context = {
        'num_organizations' : num_organizations,
        'num_services' : num_services,
        'num_contacts' : num_contacts
    }

    return render(request, 'index.html', context=context)


class OrganizationView(generic.ListView):
    model = Organization


class OrganizationDetailView(generic.DetailView):
    model = Organization


class ServiceView(generic.ListView):
    model = Service
    template_name = 'reciemviewer/service_list.html'


class LayerView(generic.ListView):
    model = Service
    template_name = 'reciemviewer/layersall_list.html'


class ServiceDetailView(generic.DetailView):
    model = Service


class OrganizationListGenerate(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ContactListGenerate(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ServiceListGenerate(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class VisorView(generic.ListView):
    model = Service
    template_name = 'reciemviewer/visor.html'