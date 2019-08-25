import json

from rest_framework import status
from rest_framework.response import Response


class ErrorResponse(Response):
    """
    API subclass from rest_framework response to easy extact error message Form
    """

    def __init__(self, form=None, error_message=None, **kwargs):
        super().__init__(status=status.HTTP_400_BAD_REQUEST)

        data = kwargs
        if not data.get('detail'):
            data['detail'] = "Your request cannot be completed"
            data["error_message"] = data['detail']
            data["error_code"] = "invalid_request"

        if error_message:
            data["error_message"] = error_message

        # only returns the first error
        if form and form.errors.items():
            data['errors'] = {}

            for field, errors in json.loads(form.errors.as_json()).items():
                key = field

                message = errors[0]['message']
                data['errors'][key] = message
                data["detail"] = '%s: %s' % (key, message)
                data["error_code"] = errors[0].get('code') if errors[0].get('code') else "invalid_data"
                data["error_message"] = message if key == "__all__" else data["detail"]

                break
        self.data = data
