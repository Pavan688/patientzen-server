"""View module for handling requests for insurance data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Insurance, Patient


class InsuranceView(ViewSet):
    """patientzen API insurance view"""

    def list(self, request):
        """Handle GET requests to get all insurances
        Returns:
            Response -- JSON serialized list of insurances
        """

        if "patientuser" in request.query_params:
            patient = Patient.objects.get(user=request.query_params['patientuser'])
            insurances = Insurance.objects.filter(patient_id=patient.id)

        else:
            insurances = Insurance.objects.all()
        serialized = InsuranceSerializer(insurances, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single insurance
        Returns:
            Response -- JSON serialized insurance record
        """

        insurance = Insurance.objects.get(pk=pk)
        serialized = InsuranceSerializer(insurance, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle Post operations
            returns
                Response -- JSON serialized insurance instance with 
                status code 201"""
        
        patient = Patient.objects.get(id=request.data["patient"])

        insurance = Insurance.objects.create(
            patient=patient,
            name=request.data["name"],
            phone_number=request.data["phone_number"],
            policy_number=request.data["policy_number"],
            start_date=request.data["start_date"],
            end_date=request.data['end_date']
        )
        serializer = InsuranceSerializer(insurance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        insurance = Insurance.objects.get(pk=pk)
        insurance.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class InsuranceSerializer(serializers.ModelSerializer):
    """JSON serializer for insurances"""
    class Meta:
        model = Insurance
        fields = ('id', 'name', 'patient', 'phone_number', 'policy_number', 'start_date', 'end_date')