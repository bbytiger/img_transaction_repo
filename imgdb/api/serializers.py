from rest_framework import serializers
from imgdb.models import ImageData, ImageTransaction

class ImageDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = ImageData
    fields = '__all__'

class ImageTransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ImageTransaction
    fields = '__all__'