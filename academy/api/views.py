from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):

    def get(self, request):
        content = {
            'data': 'home data',
        }
        return Response(content)
