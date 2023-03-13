from django.db import models

class Appointment(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    office = models.ForeignKey("Office", on_delete=models.CASCADE)
    visit_summary = models.CharField(max_length=500)
