import phonenumbers, re
from phonenumbers import phonenumberutil
from id_phonenumbers import parse

from django.conf import settings
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext
from django.contrib.auth.password_validation import (MinimumLengthValidator as DjangoMinimumLengthValidator,
                                                     NumericPasswordValidator as DjangoNumericPasswordValidator)


def validate_email(email):
    return validate_email_address(email)


def validate_email_address(email):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError(f'{email} is not a valid email', code='invalid')

    if email.endswith('.'):
        raise ValidationError('Email cannot end with \'.\' (dot), please check again')
    else:
        return True

def validate_username(email):
    if not re.match(r'^[a-z0-9_.-]+$', email):
        raise ValidationError('Masukkan nama pengguna yang valid. Nilai ini hanya boleh mengandung karakter huruf kecil, angka, dan karakter ./-/_')
    else:
        return True

def validate_mobile_phone(phone_number):
    # Indonesia only accept mobile phone
    if settings.COUNTRY == 'ID':
        try:
            number = parse(phone_number)
        except phonenumberutil.NumberParseException:
            raise ValidationError('Please enter a valid mobile phone number.')

        if number.is_mobile:
            return True

        # International phone numbers are accepted
        if phone_number.startswith('+') and len(phone_number) > 8:
            return True
    else:
        try:
            phone = phonenumbers.parse(phone_number, settings.COUNTRY)
        except phonenumberutil.NumberParseException:
            raise ValidationError('Please enter a valid mobile phone number.')
        number_type = phonenumberutil.number_type(phone)

        accepted_mobile_type = [
            phonenumberutil.PhoneNumberType.MOBILE,
            phonenumberutil.PhoneNumberType.FIXED_LINE_OR_MOBILE,
        ]

        if number_type in accepted_mobile_type:
            return True

    raise ValidationError('Please enter a valid mobile phone number.')


class MinimumLengthValidator(DjangoMinimumLengthValidator):
    def get_help_text(self):
        return ugettext(
            "Password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )


class NumericPasswordValidator(DjangoNumericPasswordValidator):
    def get_help_text(self):
        return ugettext("Password can't be entirely numeric.")
