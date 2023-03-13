from django.db import models
from django.contrib.auth.models import User


class Provider(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    patients = models.ManyToManyField("Patient", through="PatientProvider")

    property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'