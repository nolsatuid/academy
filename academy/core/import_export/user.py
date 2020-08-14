import json

from rest_framework import serializers

from academy.apps.accounts.models import User, Profile, Certificate


class ProfileImportExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('id', 'user', 'avatar', 'curriculum_vitae')


class CertificateSerializer(serializers.Serializer):
    title = serializers.CharField()
    number = serializers.CharField()
    created_at = serializers.DateTimeField()
    is_graduate = serializers.BooleanField()

    def create(self, validated_data):
        cert = Certificate(
            title=validated_data['title'],
            number=validated_data['number'],
            created=validated_data['created_at'],
            user=validated_data['user']
        )
        cert.save()
        return cert


class UserImportExportSerializer(serializers.ModelSerializer):
    profile = ProfileImportExportSerializer(read_only=True)
    cert = CertificateSerializer(source="get_all_certificates", many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('id',)


class UserImportExport:

    def __init__(self, file_path):
        self.file_path = file_path

    def import_data(self):
        imported_count = 0
        invalid_count = 0
        with open(self.file_path, 'r') as inputfile:
            users_dict = json.loads(inputfile.read().replace('\n', ''))
            for user in users_dict:
                user_serializer = UserImportExportSerializer(data=user)
                profile_serializer = ProfileImportExportSerializer(data=user['profile'])
                cert_serializer = CertificateSerializer(data=user.get('cert', []), many=True)

                if user_serializer.is_valid() and profile_serializer.is_valid() and cert_serializer.is_valid():
                    new_user = user_serializer.save()
                    new_profile = profile_serializer.save(user=new_user)
                    new_cert = cert_serializer.save(user=new_user)
                    print(f"O {user['username']} Saved")
                    imported_count += 1
                else:
                    print(f"X {user['username']} INVALID")
                    invalid_count += 1
        print("=======================")
        print(f"{imported_count} Imported")
        print(f"{invalid_count} Invalid")
        print("=======================")

    def export_data(self, users):
        users_serializer = UserImportExportSerializer(users, many=True)
        with open(self.file_path, 'w') as outputfile:
            outputfile.write(json.dumps(users_serializer.data, indent=4))
