from rest_framework import serializers
from .models import File,Product
class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'timestamp')
class ProductSerializer(serializers.ModelSerializer):
  class Meta():
    model = Product
    fields = ('upc','ean', 'timestamp')