"""View module for handling requests for Patients data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Patient


class PatientView(ViewSet):
    """Honey Rae API patients view"""

    def list(self, request):
        """Handle GET requests to get all patients
        Returns:
            Response -- JSON serialized list of patients
        """

        patients = Patient.objects.all()
        serialized = PatientSerializer(patients, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single patient
        Returns:
            Response -- JSON serialized patient record
        """

        patient = Patient.objects.get(pk=pk)
        serialized = PatientSerializer(patient, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class PatientSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""
    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'DOB', 'phone_number', 'street_name', 'city', 'state', 'zip_code')