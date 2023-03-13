from django.db import models

class Office(models.Model):
    address = models.CharField(max_length=50)