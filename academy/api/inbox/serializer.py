from rest_framework import serializers

from academy.apps.accounts.models import Inbox


class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        exclude = ['user']


class BulkReadUnreadSerializer(serializers.Serializer):
    filter = serializers.ListField(
        child=serializers.IntegerField()
    )
    read_state = serializers.BooleanField()
