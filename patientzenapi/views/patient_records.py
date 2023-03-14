"""View module for handling requests for records data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Record, Provider


class RecordView(ViewSet):
    """PatientZen API record view"""

    def list(self, request):
        """Handle GET requests to get all providers
        Returns:
            Response -- JSON serialized list of provider
        """
        
        if "patient" in request.query_params:
            records = Record.objects.filter(patient_id=request.query_params['patient'])

        else: 
            records = Record.objects.all()
        serialized = PatientSerializer(records, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single records
        Returns:
            Response -- JSON serialized record 
        """

        record = Record.objects.get(pk=pk)
        serialized = PatientSerializer(record, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class PatientSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""
    class Meta:
        model = Record
        fields = ('id', 'patient', 'provider', 'visit_datetime', 'visit_summary', 'diagnosis', 'treatment', 'medication')