from django.db import models
class File(models.Model):
  file = models.FileField(blank=False, null=False)
  timestamp = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
  upc = models.CharField(max_length=20)
  ean = models.CharField(max_length=20)
  timestamp = models.DateTimeField(auto_now_add=True)


