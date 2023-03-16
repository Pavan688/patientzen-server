"""View module for handling requests for office data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Office


class OfficeView(ViewSet):
    """PatientZen API offices view"""

    def list(self, request):
        """Handle GET requests to get all offices
        Returns:
            Response -- JSON serialized list of offices
        """

        offices = Office.objects.all()
        serialized = OfficeSerializer(offices, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single office
        Returns:
            Response -- JSON serialized office record
        """

        office = Office.objects.get(pk=pk)
        serialized = OfficeSerializer(office, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class OfficeSerializer(serializers.ModelSerializer):
    """JSON serializer for office"""
    class Meta:
        model = Office
        fields = ('id', 'address',)