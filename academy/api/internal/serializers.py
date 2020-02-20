from rest_framework import serializers

from academy.apps.accounts.models import User, Profile, Inbox, Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='avatar_with_host')
    curriculum_vitae = serializers.CharField(source='curriculum_vitae_with_host')

    class Meta:
        model = Profile
        exclude = ["id", 'user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = ["password"]


class AddInboxSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        if not attrs.get('raw_content', None):
            attrs['raw_content'] = attrs['content']
        return attrs

    class Meta:
        model = Inbox
        fields = ('user', 'subject', 'content', 'raw_content')
