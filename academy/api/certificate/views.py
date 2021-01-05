from rest_framework.generics import ListAPIView, RetrieveAPIView

from academy.api.authentications import UserAuthMixin
from academy.api.certificate.serializers import CertificateSerializer
from academy.apps.accounts.models import Certificate


class CertificateListView(UserAuthMixin, ListAPIView):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)


class CertificateDetailView(UserAuthMixin, RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)
