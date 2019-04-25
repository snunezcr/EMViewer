# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>

from django.urls import path
from . import views
from .views import emailView
from .views import successView

urlpatterns = [
    path('', views.index, name='index'),
    path('visor/', views.VisorView.as_view(), name='visor'),
    path('organizations/', views.OrganizationView.as_view(), name='organizations'),
    path('organization/<pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('services/', views.ServiceView.as_view(), name='services'),
    path('layersall/', views.LayerView.as_view(), name='layersall'),
    path('emailsend/', emailView, name='emailsend'),
    path('emailok/', successView, name='emailok'),
    path('service/<pk>', views.ServiceDetailView.as_view(), name='service-detail'),
    path('api/organizations/', views.OrganizationListGenerate.as_view()),
    path('api/contacts/', views.ContactListGenerate.as_view()),
    path('api/services/', views.ServiceListGenerate.as_view())
]
