from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import SolicitudSerializer
from .models import Solicitud

class userSolicitudCreateAPIView(CreateAPIView):
    """
    API endpoint for creating biodiversity data requests.
    
    This endpoint allows users to submit requests for biodiversity data
    from the Instituto Alexander von Humboldt database.
    """
    serializer_class = SolicitudSerializer
    queryset = Solicitud.objects.all()
    
    @swagger_auto_schema(
        operation_description="Create a new biodiversity data request",
        operation_summary="Submit Data Request",
        tags=['User Requests'],
        request_body=SolicitudSerializer,
        responses={
            201: openapi.Response(
                description="Request created successfully",
                schema=SolicitudSerializer
            ),
            400: openapi.Response(
                description="Invalid request data",
                examples={
                    "application/json": {
                        "error": "Invalid data provided",
                        "details": "Field validation errors"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new biodiversity data request.
        
        Submit a request for biodiversity data including contact information
        and specific observations or requirements.
        """
        return super().post(request, *args, **kwargs)  
