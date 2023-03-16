"""View module for handling requests for appointments data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from patientzenapi.models import Appointment, Provider, Patient, Office


class AppointmentView(ViewSet):
    """Honey Rae API appointments view"""

    def list(self, request):
        """Handle GET requests to get all appointments
        Returns:
            Response -- JSON serialized list of appointments
        """

        if "user" in request.query_params:
            provider = Provider.objects.get(user=request.query_params['user'])
            appointments = Appointment.objects.filter(provider_id=provider.id)

        elif "patientuser" in request.query_params:
            patient = Patient.objects.get(user=request.query_params['patientuser'])
            appointments = Appointment.objects.filter(patient_id=patient.id)

        else:
            appointments = Appointment.objects.all()
        serialized = AppointmentSerializer(appointments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single appointment
        Returns:
            Response -- JSON serialized appointment instance
        """

        appointment = Appointment.objects.get(pk=pk)
        serialized = AppointmentSerializer(appointment, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle Post operations
            returns
                Response -- JSON serialized appointment instance with 
                status code 201"""
        
        patient = Patient.objects.get(user=request.data["patient"])
        provider = Provider.objects.get(id=request.data["provider"])
        office = Office.objects.get(id=request.data["office"])

        appointment = Appointment.objects.create(
            patient=patient,
            provider=provider,
            date=request.data["date"],
            time=request.data["time"],
            office=office,
            visit_summary=request.data['visit_summary']
        )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a record
        Returns:
            Response -- Empty body with 204 status code
        """

        appointment = Appointment.objects.get(pk=pk)
        appointment.date=request.data["date"]
        appointment.visit_summary=request.data["visit_summary"]
        appointment.time=request.data["time"]

        patient = Patient.objects.get(user=request.data["patient"])
        provider = Provider.objects.get(pk=request.data["provider"])
        office = Office.objects.get(pk=request.data["office"])
        appointment.patient = patient
        appointment.provider = provider
        appointment.office = office
        appointment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        appointment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class PatientSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""

    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'DOB', )

class ProviderSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""

    class Meta:
        model = Provider
        fields = ('id', 'full_name', 'specialty', )

class OfficeSerializer(serializers.ModelSerializer):
    """JSON serializer for patients"""

    class Meta:
        model = Office
        fields = ('id', 'address', )


class AppointmentSerializer(serializers.ModelSerializer):
    """JSON serializer for appointments"""
    patient = PatientSerializer()
    office = OfficeSerializer()
    provider = ProviderSerializer()
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'provider', 'date', 'time', 'office', 'visit_summary')