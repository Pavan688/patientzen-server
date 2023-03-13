from django.db import models

class Insurance(models.Model):
    name = models.CharField(max_length=55)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    policy_number = models.CharField(max_length=12)
    start_date = models.CharField(max_length=25)
    end_date = models.CharField(max_length=25)