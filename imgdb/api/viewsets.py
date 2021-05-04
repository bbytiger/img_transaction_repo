from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from imgdb.models import ImageData, ImageTransaction

from .serializers import ImageDataSerializer, ImageTransactionSerializer

class ImageDataViewset(viewsets.ModelViewSet):
  queryset = ImageData.objects.all()
  serializer_class = ImageDataSerializer
  
  @action(detail=True, methods=['get'])
  def user_images(self, request, *args, **kwargs):
    self.queryset = ImageData.objects.all()

  @action(detail=True, methods=['post'])
  def create_image(self, request, *args, **kwargs):
    pass
    #try:
    #
    #except:

  @action(detail=True, methods=['delete'])
  def delete_image(self, request, )

class ImageTransactionViewset(viewsets.ModelViewSet):
  pass