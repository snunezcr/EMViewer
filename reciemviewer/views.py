# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>
from rest_framework import generics
from reciemviewer.models import Organization, Contact, Service
from reciemviewer.serializers import OrganizationSerializer, ContactSerializer, ServiceSerializer
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import generic
from .forms import ContactForm


def index(request):
    num_organizations = Organization.objects.all().count()
    num_services = Service.objects.all().count()
    num_contacts = Contact.objects.all().count()

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

@method_decorator(cache_page(60 * 20), name='dispatch')
class LayerView(generic.ListView):
    model = Service
    template_name = 'reciemviewer/layersall_list.html'


class ServiceDetailView(generic.DetailView):
    model = Service


class OrganizationListGenerate(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by('short')
    serializer_class = OrganizationSerializer


class ContactListGenerate(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ServiceListGenerate(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('short')
    serializer_class = ServiceSerializer

@method_decorator(cache_page(60 * 20), name='dispatch')
class VisorView(generic.ListView):
    model = Service
    template_name = 'reciemviewer/visor.html'

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['snunezcr@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('emailok')
    return render(request, "emailsend.html", {'form': form})

def successView(request):
    return render(request, "emailok.html")