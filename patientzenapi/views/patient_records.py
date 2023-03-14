"""View module for handling requests for records data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Record, Provider, Patient


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
        serialized = RecordSerializer(records, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single records
        Returns:
            Response -- JSON serialized record 
        """

        record = Record.objects.get(pk=pk)
        serialized = RecordSerializer(record, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle Post operations
            returns
                Response -- JSON serialized record instance with 
                status code 201"""
        
        patient = Patient.objects.get(id=request.data['patient'])
        provider = Provider.objects.get(id=request.data["provider"])

        record = Record.objects.create(
            patient=patient,
            provider=provider,
            visit_datetime=request.data["visit_datetime"],
            visit_summary=request.data["visit_datetime"],
            treatment=request.data["treatment"],
            diagnosis=request.data["diagnosis"],
            medication=request.data["medication"]
        )
        serializer = RecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a record
        Returns:
            Response -- Empty body with 204 status code
        """

        record = Record.objects.get(pk=pk)
        record.visit_datetime=request.data["visit_datetime"]
        record.visit_summary=request.data["visit_datetime"]
        record.treatment=request.data["treatment"]
        record.diagnosis=request.data["diagnosis"]
        record.medication=request.data["medication"]

        patient = Patient.objects.get(pk=request.data["patient"])
        provider = Provider.objects.get(pk=request.data["provider"])
        record.patient = patient
        record.provider = provider
        record.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class PatientSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""

    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'DOB', )

class ProviderSerializer(serializers.ModelSerializer):
    """JSON serializer for provider"""

    class Meta:
        model = Provider
        fields = ('id', 'full_name', )


class RecordSerializer(serializers.ModelSerializer):
    """JSON serializer for records"""
    provider = ProviderSerializer()
    patient = PatientSerializer()
    class Meta:
        model = Record
        fields = ('id', 'patient', 'provider', 'visit_datetime', 'visit_summary', 'diagnosis', 'treatment', 'medication')