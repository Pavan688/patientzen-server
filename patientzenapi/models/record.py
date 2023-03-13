from django.db import models

class Record(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.DO_NOTHING)
    provider = models.ForeignKey("Provider", on_delete=models.DO_NOTHING)
    visit_datetime = models.CharField(max_length=20)
    visit_summary = models.CharField(max_length=500)
    diagnosis = models.CharField(max_length=200)
    treatment = models.CharField(max_length=500)
    medication = models.CharField(max_length=500)