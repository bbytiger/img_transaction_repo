from rest_framework import serializers
from imgdb.models import *

class ImageDataSerializer(serializers.Serializer):
  class Meta:
    model = ImageData
    fields = '__all__'

class ImageTransactionSerializer(serializers.Serializer):
  class Meta:
    model = ImageTransaction
    fields = '__all__'