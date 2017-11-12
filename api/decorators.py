from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.status import  HTTP_401_UNAUTHORIZED


"""A decorator to validate the provided token in the request
    header"""

def token_required(func):

    def wrapper(request,*args,**kwargs):

        token = None
        token_exist = False

        token_header = request.META.get('HTTP_AUTHORIZATION')

        if token_header:
            token = token_header.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=str(token))
                if token_obj:
                    token_exist = True
            except:
                token_exist = False

        if token_exist:
            return func(request,*args,**kwargs)
        else:
            return JsonResponse(data={'detail': "Authentication credentials were not provided."},status=HTTP_401_UNAUTHORIZED)

    return wrapper