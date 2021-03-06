import os
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework import viewsets, mixins
from rest_framework.decorators import action, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from imgdb.models import ImageData, ImageTransaction
from imgdb.api.serializers import ImageDataSerializer, ImageTransactionSerializer

def process_img(blob, user_model_obj, bool_public, img_name):
  user_folder = "user_"+str(user_model_obj.id)+'/'
  user_path = 'userdata/tmp/'+user_folder
  save_path = 'tmp/'+user_folder

  # force the directory to exist
  if not os.path.exists(user_path):
    os.makedirs(user_path)

  list_of_user_images = user_model_obj.user_images
  file_number = list_of_user_images.count()

  try:
    # first save the file
    new_file_path = save_path+str(file_number)+".png"
    default_storage.save(new_file_path, ContentFile(blob.read()))
      
    # now create the model and save it
    image_entry = ImageData.objects.create(
      name = img_name[:500],
      owner = user_model_obj,
      public = bool_public,
      path = new_file_path,
      created = make_aware(datetime.now())
    )
    image_entry.save()
    return image_entry.id

  except:
    return False

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
    if 'Authorization' not in request.headers:
      return Response({"detail":"Authorization credentials were not provided."}, status=401)
    else:
      try:
        # parse Authorization header
        auth_token = str(request.headers['Authorization'].split(" ")[1])
        user_search = Token.objects.get(key=auth_token).user
        belong_to_user = user_search.user_images.all()
        serializer = ImageDataSerializer(belong_to_user, many=True)
        return Response({"data": serializer.data})
      except:
        return Response({"detail":"Authorization credentials were not provided."}, status=401)

  @authentication_classes((TokenAuthentication,))
  @action(detail=False, methods=['post'])
  def dl_image(self, request, *args, **kwargs):
    if 'Authorization' not in request.headers:
      return Response({"detail":"Authorization credentials were not provided."}, status=401)
    else:
      try:
        # parse Authorization header
        auth_token = str(request.headers['Authorization'].split(" ")[1])
        user_search = Token.objects.get(key=auth_token).user
        img_id = str(request.data['id'])
        belong_to_user = user_search.user_images.filter(id=img_id)[0]
        user_data = "userdata/"+belong_to_user.path
        f = open(user_data, 'rb').read()
        return HttpResponse(f, content_type='application/octet-stream')
      except:
        return Response({"detail":"Authorization credentials were not provided."}, status=401)

  @authentication_classes((TokenAuthentication,))
  @action(detail=False, methods=['post'])
  def create_image(self, request, *args, **kwargs):
    if 'Authorization' not in request.headers:
      user_list = User.objects.filter(username=request.user)
      name = str(request.data['img_name'])
      public = True if str(request.data['public']) == "true" else False
      img = request.data['img']
      if img is not None and name is not None and len(user_list) == 1:
        processed_img_bool = process_img(img, user_list[0], public, name)
        if processed_img_bool:
          return Response({'message': "successfully processed request"}, status=200)
        else:
          return Response({'message': "failed, please try again"}, status=400)
      else:
        return Response({'message': "failed, please try again"}, status=400)
    else:
      try:
        # parse Authorization header
        auth_token = str(request.headers['Authorization'].split(" ")[1])
        user_search = Token.objects.get(key=auth_token).user
        name = str(request.data['img_name'])
        public = True if 'public' in request.data and str(request.data['public']) == "True" else False
        img = request.data['img']
        if img is not None and name is not None:
          processed_img_bool = process_img(img, user_search, public, name)
          if processed_img_bool:
            return Response({'message': "successfully processed request", 'id': processed_img_bool}, status=200)
          else:
            return Response({'message': "failed, please try again"}, status=400)
        else:
          return Response({'message': "failed, please try again"}, status=400)
      except:
        return Response({"detail":"Authorization credentials failed."}, status=401)

  @action(detail=False, methods=['post'])
  def batch_create(self, request, *args, **kwargs):
    return Response({'message': "endpoint not completed"})

  @action(detail=False, methods=['delete'])
  def delete_image(self, request, *args, **kwargs):
    return Response({'message': "endpoint not completed"})

  @action(detail=False, methods=['delete'])
  def batch_delete(self, request, *args, **kwargs):
    return Response({'message': "endpoint not completed"})