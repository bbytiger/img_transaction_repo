import uuid
from django.db import models
from django.contrib.auth.models import User

class ImageData(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  owner = models.ForeignKey(User, related_name='user_images',on_delete=models.PROTECT, null=True, blank=True)
  public = models.BooleanField(null=True, default=False)
  forsale = models.BooleanField(null=True, default=False)
  viewers = models.ManyToManyField(User)
  path = models.FilePathField(max_length=512, null=True, blank=True)
  price = models.IntegerField(null=True, blank=True)
  discount_type = models.TextChoices('percent', 'cents')
  discount = models.IntegerField(null=True, blank=True)
  created = models.DateTimeField(null=True, blank=True)

class SearchMetaData(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  im = models.ForeignKey(ImageData, related_name="im_data", on_delete=models.PROTECT, null=True, blank=True)
  # to be expanded as we go to accomodate SEARCH

class ImageTransaction(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  complete = models.BooleanField(null=True, default=False)
  initiated = models.DateTimeField(null=True, blank=True)
  completed = models.DateTimeField(null=True, blank=True)
  confirmation_code = models.CharField(max_length=10, null=True, blank=True)
  amount = models.IntegerField(null=True, blank=True)
  img = models.ForeignKey(ImageData, on_delete=models.PROTECT, null=True, blank=True)
  seller = models.ForeignKey(User, related_name='sold', on_delete=models.PROTECT, null=True, blank=True)
  buyer = models.ForeignKey(User, related_name='bought', on_delete=models.PROTECT, null=True, blank=True)

  def save(self, *args, **kwargs):
    # method to ensure that the complete boolean is always consistent with the transaction date
    super().save(*args, **kwargs) 
    if self.completed:
      self.complete = True
    else:
      self.complete = False
    super().save()

  ## with transaction.atomic(): .select_for_updates() to lock the database before transaction
  