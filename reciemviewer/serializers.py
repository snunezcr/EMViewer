# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2018
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>
from rest_framework import serializers
from reciemviewer.models import Organization
from reciemviewer.models import Contact
from reciemviewer.models import Service


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


