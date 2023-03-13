from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=15)


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'