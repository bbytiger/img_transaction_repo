from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.decorators import action, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from imgdb.models import ImageData, ImageTransaction
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import ImageDataSerializer, ImageTransactionSerializer

from datetime import datetime
import io

class UserSearchViewSet(viewsets.GenericViewSet):
  queryset = User.objects.all()
  @action(detail=False, methods=['post'])
  def shared_search(self, request, *args, **kwargs):
    # make sure that it is a user using it through the search function, i.e. disallow API keys
    pass

class ImageDataViewSet(viewsets.GenericViewSet):              
  queryset = ImageData.objects.all()
  serializer_class = ImageDataSerializer
  parser_classes = [JSONParser, MultiPartParser]
  
  @authentication_classes((TokenAuthentication,))
  @action(detail=False, methods=['get'])
  def user_images(self, request, *args, **kwargs):
    print(request.headers)
    if 'Authorization' not in request.headers:
      return Response({"detail":"Authorization credentials were not provided."}, status=401)
    
    self.queryset = ImageData.objects.all()
    serializer = ImageDataSerializer(self.queryset, many=True)
    return Response({"data": serializer.data})

  @authentication_classes((TokenAuthentication,))
  @action(detail=False, methods=['post'])
  def create_image(self, request, *args, **kwargs):
    print(request.headers)
    if 'Authorization' not in request.headers:
      # this will be a multipart-form-upload from in-app action
      name = str(request.data['img_name'])
      public = str(request.data['public'])
      img = request.data['img']
      print(request.FILES['img'])
      print(request.data)
      print(name)
      print(public)
      print(img)

      return Response({'not found': "not found"})
    else:
      return Response({'not found': "not found"})

  @action(detail=False, methods=['post'])
  def batch_create(self, request, *args, **kwargs):
    pass

  @action(detail=False, methods=['delete'])
  def delete_image(self, request, *args, **kwargs):
    pass

  @action(detail=False, methods=['delete'])
  def batch_delete(self, request, *args, **kwargs):
    pass

class ImageTransactionViewSet(viewsets.GenericViewSet):
  pass