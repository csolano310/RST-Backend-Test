from http import HTTPStatus
from django.http import HttpResponse, JsonResponse
from functools import wraps
from jose import jwt
from django.conf import settings
import time

def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            if not req.headers.get('Authorization') or req.headers.get('Authorization')==None:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
            header = req.headers.get('Authorization').split(" ")
            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms='HS512')
            except Exception as e:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
            
            if int(resuelto["exp"])>int(time.time()):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo