from rest_framework import serializers

from academy.apps.accounts.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        exclude = ['user']
