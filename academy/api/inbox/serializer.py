from rest_framework import serializers

from academy.apps.accounts.models import Inbox


class InboxListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        exclude = ['user', 'content']


class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        exclude = ['user']


class BulkReadUnreadSerializer(serializers.Serializer):
    filter = serializers.ListField(
        child=serializers.IntegerField()
    )
    read_state = serializers.BooleanField()


class BulkDeleteSerializer(serializers.Serializer):
    inbox_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
