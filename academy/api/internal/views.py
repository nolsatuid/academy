from rest_framework.response import Response

from academy.api.authentications import InternalAPIView


class DemoView(InternalAPIView):
    def get(self, request):
        return Response(data={
            'message': 'Hellow from academy'
        })

    def post(self, request):
        user_id = request.data.get('user_id', None)
        other_info = request.data.get('other_info', None)
        return Response(data={
            'user_id': user_id,
            'other_info': other_info
        })
