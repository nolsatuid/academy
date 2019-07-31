from rest_framework import serializers

from academy.apps.surveys.model import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        exclude = ["id", "user"]
