# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from django_theme.libs.code import success_dict

from .models import Theme


class SystemStyleView(APIView):
    def get(self, request):
        style = Theme.objects.first()
        theme_dict = style.to_dict()
        return Response(success_dict(msg="success", data=theme_dict))
