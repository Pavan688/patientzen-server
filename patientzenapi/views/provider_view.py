"""View module for handling requests for Providers data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Provider


class ProviderView(ViewSet):
    """PatientZen API providers view"""

    def list(self, request):
        """Handle GET requests to get all providers
        Returns:
            Response -- JSON serialized list of provider
        """

        providers = Provider.objects.all()
        serialized = PatientSerializer(providers, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single provider
        Returns:
            Response -- JSON serialized provider record
        """

        provider = Provider.objects.get(user=pk)
        serialized = PatientSerializer(provider, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class PatientSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""
    class Meta:
        model = Provider
        fields = ('id','user', 'full_name', 'specialty', 'phone_number')