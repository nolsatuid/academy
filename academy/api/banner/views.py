from rest_framework import generics

from academy.api.banner.serializers import BannerSerializer
from academy.apps.offices.models import Banner


class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.filter(show_app=True).all()
    serializer_class = BannerSerializer
