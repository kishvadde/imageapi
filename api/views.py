import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   )

from .seriealizers import ImageSerializer

from .decorators import token_required
from .utils import (silentremove,
                    handle_image_storage,
                    generate_url_for_image)


IMAGES_DIR_PATH = settings.IMAGES_DIR_PATH



"""An API view to create Image through API. It uses token 
    authentication to authorize the requests """

class ImageCreate(generics.GenericAPIView):

    serializer_class = ImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):

        res = "Bad request"
        status = HTTP_400_BAD_REQUEST
        image = request.FILES.get('image')
        token_header = request.META.get('HTTP_AUTHORIZATION')

        if image and token_header:
            token = token_header.split(' ')[1]
            res,status = handle_image_storage(image=image,token=token)

        return Response({'content':res},status=status)



"""An API view to update image through API. It uses token 
    authentication to authorize the requests """

class ImageUpdate(generics.GenericAPIView):

    serializer_class = ImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):

        res = "Bad request"
        status = HTTP_400_BAD_REQUEST
        image = request.FILES.get('image')
        token_header = request.META.get('HTTP_AUTHORIZATION')

        if image and token_header:
            token = token_header.split(' ')[1]
            res,status = handle_image_storage(image=image,token=token,update=True)

        return Response({'content':res},status=status)


""" An API view to return the single image by its url.
    It returns image as an http response.
"""
@require_http_methods(['GET'])
@token_required
def get_image(request,image_name=None):

    res_content = "Image not found"
    status= HTTP_404_NOT_FOUND
    image_path = None
    extension = 'png'

    token_header = request.META.get('HTTP_AUTHORIZATION')
    token = token_header.split(' ')[1]

    if image_name:

        image_path = os.path.join(IMAGES_DIR_PATH,str(token),image_name)
        if os.path.exists(image_path):
            content = open(image_path,'rb')
            status = HTTP_200_OK
            extension = image_name.split('.')[-1]

    return HttpResponse(content.read(),status=status,content_type='image/{}'.format(extension))


"""A API view to return list of image urls associated with the 
    provided token """

@require_http_methods(['GET'])
@token_required
def get_images(request):

    res_content = {'res':"Images not found"}
    status = HTTP_404_NOT_FOUND
    image_path = None
    image_urls = []

    token_header = request.META.get('HTTP_AUTHORIZATION')
    token = token_header.split(' ')[1]
    image_dir_path = os.path.join(IMAGES_DIR_PATH,token)
    images = os.listdir(image_dir_path)

    if images:
        for img in images:
            img_url = generate_url_for_image(img)
            image_urls.append(img_url)

        res_content = {'content':image_urls}
        status = HTTP_200_OK

    return JsonResponse(res_content,status=status)


"""An API view to delete the image by its name,
    associated with the token"""

@require_http_methods(['POST'])
@csrf_exempt
@token_required
def delete_image(request):

    res_content = {}
    status = HTTP_400_BAD_REQUEST
    content = 'Bad request'

    image = request.POST.get('image')
    token_header = request.META.get('HTTP_AUTHORIZATION')
    token = token_header.split(' ')[1]

    if image:
        image_path = os.path.join(IMAGES_DIR_PATH,str(token),str(image))
        (content,status)= silentremove(image_path)

    if status == HTTP_204_NO_CONTENT:
       content = '{image},{content}'.format(image=image,content=content)

    res_content['content'] = content

    return JsonResponse(res_content,status=status)




"""A view to render the user API authentication token"""
@login_required
def get_api_key(request):

    token = None
    try:
        token_ob = Token.objects.get(user=request.user)
        token = token_ob.key
    except:
        token = "No Token"

    return render(request,'api/api_key.html',{'token':token})















    










