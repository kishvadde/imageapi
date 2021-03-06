import os
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

images_dir_path = settings.IMAGES_DIR_PATH

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def generate_token(sender,instance=None,created=False,**kwargs):

    if created and isinstance(instance,User):
        token = Token.objects.create(user=instance)
        token.save()
        path = os.path.join(images_dir_path,str(token.key))
        if not os.path.exists(path):
            os.mkdir(path)












