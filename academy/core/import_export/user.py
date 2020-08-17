import json
import os
from zipfile import ZipFile
from datetime import datetime

from django.conf import settings
from rest_framework import serializers

from academy.apps.accounts.models import User, Profile, Certificate


class ProfileImportExportSerializer(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField(required=False)
    cv_path = serializers.SerializerMethodField(required=False)

    def get_avatar_path(self, obj):
        if obj.avatar:
            return obj.avatar.path
        return None

    def get_cv_path(self, obj):
        if obj.curriculum_vitae:
            return obj.curriculum_vitae.path
        return None

    class Meta:
        model = Profile
        exclude = ('id', 'user', 'avatar', 'curriculum_vitae',)


class CertificateSerializer(serializers.Serializer):
    title = serializers.CharField()
    number = serializers.CharField()
    created_at = serializers.DateTimeField()
    cert_file = serializers.CharField()

    def create(self, validated_data):
        cert = Certificate(
            title=validated_data['title'],
            number=validated_data['number'],
            created=validated_data['created_at'],
            user=validated_data['user'],
            certificate_file=validated_data['cert_file']
        )
        cert.save()
        return cert


class UserImportExportSerializer(serializers.ModelSerializer):
    profile = ProfileImportExportSerializer(read_only=True)
    cert = CertificateSerializer(source="get_all_certificates", many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('id',)


class UserExport:
    users_json_name = "users.json"

    def __init__(self, file_path):
        self.file_path = file_path

    def _write_media_to_zip(self, zip_file, filepath, prefix):
        media_dir = os.path.dirname(filepath.replace(settings.MEDIA_ROOT, ""))
        old_name = os.path.basename(filepath)
        old_extension = ".".join(old_name.split(".")[1:])
        new_filename = prefix + datetime.now().strftime("%d%m%Y-%H%M%S%f") + "." + old_extension
        new_filepath = os.path.join(media_dir, new_filename)[1:]

        zip_file.write(filepath, new_filepath)

        return new_filepath

    def _write_profile_file_to_zip(self, zip_file, user_data, profile_attr):
        if user_data['profile'].get(profile_attr, None):
            new_path = self._write_media_to_zip(zip_file, user_data['profile'][profile_attr], user_data['username'])
            user_data['profile'][profile_attr] = new_path

        return user_data

    def _write_certificate_to_zip(self, zip_file, user_data):
        def map_cert_file(cert):
            cert['cert_file'] = self._write_media_to_zip(zip_file, cert['cert_file'], user_data['username'])
            return cert

        user_data['cert'] = list(map(map_cert_file, user_data['cert']))
        return user_data

    def export_data(self, users):
        zip_file = ZipFile(self.file_path, "w")
        users_serializer = UserImportExportSerializer(users, many=True)
        final_data = []
        for user_data in users_serializer.data:
            user_data = self._write_profile_file_to_zip(zip_file, user_data, 'cv_path')
            user_data = self._write_profile_file_to_zip(zip_file, user_data, 'avatar_path')
            user_data = self._write_certificate_to_zip(zip_file, user_data)
            final_data.append(user_data)

        zip_file.writestr(self.users_json_name, json.dumps(final_data, indent=4))
        zip_file.close()


class UserImport:
    users_json_name = "users.json"

    def __init__(self, file_path):
        self.file_path = file_path

    def _extract_profile_file_to_media(self, zip_file, user_data, profile_attr):
        path = user_data['profile'].get(profile_attr, None)
        if path:
            zip_file.extract(path, settings.MEDIA_ROOT)
        return path

    def _extract_certificates_to_media(self, zip_file, certificates):
        for cert in certificates:
            zip_file.extract(cert['cert_file'], settings.MEDIA_ROOT)

    def import_data(self):
        imported_count = 0
        invalid_count = 0
        zip_file = ZipFile(self.file_path, "r")
        users_dict = json.loads(zip_file.read(self.users_json_name))
        for user in users_dict:
            user_serializer = UserImportExportSerializer(data=user)
            profile_serializer = ProfileImportExportSerializer(data=user['profile'])
            cert_serializer = CertificateSerializer(data=user.get('cert', None), many=True)

            if user_serializer.is_valid():
                new_user = user_serializer.save()
                saved_data = "User"

                if profile_serializer.is_valid():
                    cv_path = self._extract_profile_file_to_media(zip_file, user, 'cv_path')
                    avatar_path = self._extract_profile_file_to_media(zip_file, user, 'avatar_path')
                    new_profile = profile_serializer.save(user=new_user, avatar=avatar_path, curriculum_vitae=cv_path)
                    saved_data += ", Profile"

                if cert_serializer.is_valid():
                    self._extract_certificates_to_media(zip_file, cert_serializer.validated_data)
                    new_cert = cert_serializer.save(user=new_user)
                    saved_data += ", Certificate"

                print(f"O {user['username']} Saved - {saved_data}")
                imported_count += 1
            else:
                print(f"X {user['username']} INVALID")
                invalid_count += 1

        print("=======================")
        print(f"{imported_count} Imported")
        print(f"{invalid_count} Invalid")
        print("=======================")

        zip_file.close()
