import os,errno
from urllib.parse import urljoin
from django.conf import settings
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_304_NOT_MODIFIED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_406_NOT_ACCEPTABLE,
                                   )

IMAGES_DIR_PATH = settings.IMAGES_DIR_PATH



"""It removes the given file name from the path,
    NOTE: it takes complete path of the file"""

def silentremove(filename):
    content = None
    status = HTTP_404_NOT_FOUND
    try:
        os.remove(filename)
        content = 'deleted successfully'
        status = HTTP_204_NO_CONTENT
    except OSError as e:
        if e.errno == errno.ENOENT: #No such file exception
            content = 'no such file'
        elif e.errno == errno.EACCES: #Permission denaied exception
            content = 'Internal error, not able to delete the file'
            status = HTTP_304_NOT_MODIFIED
    return (content,status)


"""It checks given file name is of type image or not"""
def is_image(image_name):

    ret = False

    image_extensions = [
        'png','jpeg','jpg','gif','tif'
    ]

    if image_name:
       image_ext =  str(image_name).split('.')
       if len(image_ext) >= 2:
            if image_ext[-1] in image_extensions:
                ret = True
    return ret


"""It stores the given image by taking image file object,
   auth token. It stores the image in a directory created
   with the name same as user token.If update is false
   and file aleardy exists it won't store the new file,
   otherwise it will override the existing file"""

def handle_image_storage(image,token,update = False):

    res = 'Bad request'
    status = HTTP_400_BAD_REQUEST

    if image and token:
        img_name = image._get_name()
        dir_path = os.path.join(IMAGES_DIR_PATH, str(token))
        file_path = os.path.join(dir_path, img_name)

        if not update:
            if os.path.exists(file_path):
                res = 'Image with the given name already exists'
                status = HTTP_406_NOT_ACCEPTABLE
                return (res,status)

        fl = open(file_path, 'wb')
        fl.write(image.read())
        fl.close()
        res = {'url':generate_url_for_image(img_name)}
        if update:
            status = HTTP_200_OK
        else:
            status = HTTP_201_CREATED

    return (res,status)



def generate_url_for_image(image_name):

   return urljoin(settings.BASE_URL, 'api/images/{}'.format(image_name))

