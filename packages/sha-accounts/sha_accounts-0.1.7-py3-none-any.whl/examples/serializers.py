from rest_framework import serializers
from .models import ExampleProfile, ExampleRelProfile


class ExampleRelProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleRelProfile
        fields = ['id', 'age']


class ExampleProfileSerializer(serializers.ModelSerializer):
    relprofile = ExampleRelProfileSerializer(required=False, many=True)

    class Meta:
        model = ExampleProfile
        fields = ['id', 'first_name', 'last_name', 'relprofile']
