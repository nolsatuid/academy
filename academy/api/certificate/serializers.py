from rest_framework import serializers

from academy.apps.accounts.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('id', 'title', 'number', 'created', 'valid_until', 'certificate_file')
