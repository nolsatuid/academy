from rest_framework import serializers

from academy.apps.offices.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('title', 'link', 'image')
