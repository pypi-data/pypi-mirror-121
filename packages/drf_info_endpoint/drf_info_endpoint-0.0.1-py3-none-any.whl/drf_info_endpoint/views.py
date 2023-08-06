from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import InfoSerializer


@extend_schema(request=None, responses=InfoSerializer())
@api_view(["get"])
@permission_classes([AllowAny])
def info(request: Request) -> Response:
    return Response(
        {
            "app": getattr(settings, "DRF_INFO_ENDPOINT_PROJECT_NAME", "Project"),
            "version": getattr(settings, "DRF_INFO_ENDPOINT_VERSION", "v0.0.0"),
        }
    )
