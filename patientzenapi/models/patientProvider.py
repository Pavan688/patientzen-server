from django.db import models

class PatientProvider(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)