from rest_framework.views import APIView
from .decorators import logueado
from django.conf import settings
from jose import jwt
from http import HTTPStatus
from django.http import JsonResponse
from .models import *
from .serializers import *
import datetime



class Class_ListTask(APIView):
    
    @logueado()
    def get(self, request):
        
        try:
            header = request.headers.get('Authorization').split(" ")
            resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms='HS512')
            data = Task.objects.filter(user_id=User(resuelto['id'])).order_by('-id').all()
            datos_parseJson = TaskSerializers(data, many=True)
            return JsonResponse({"data": datos_parseJson.data}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
class Class_CreateTask(APIView):
    
    @logueado()
    def post(self, request):
        if request.data.get("title") == None or not(request.data.get("title")):
            return JsonResponse({"Status": "Error", "message": "title field is necesary, tasks without title not allowed"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("description") == None or not(request.data.get("description")):
            return JsonResponse({"Status": "Error", "message": "description field is necesary, empty tasks not allowed"}, status=HTTPStatus.BAD_REQUEST)
        header = request.headers.get('Authorization').split(" ")
        resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms='HS512')
        try:
            Task.objects.create(title=request.data['title'], description=request.data['description'], status='pendiente', user_id=User(resuelto['id']), created_at=datetime.datetime.now())
        except Exception as e:
            print(e)
            return JsonResponse({"status": "Error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return JsonResponse({"status": "OK", "message": "Created"}, status=HTTPStatus.CREATED)
    
class Class_EditTask(APIView):
    
    @logueado()
    def put(self, request, id_task):
        
        if request.data.get("title") == None or not(request.data.get("title")):
            return JsonResponse({"Status": "Error", "message": "title field is necesary, tasks without title not allowed"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("description") == None or not(request.data.get("description")):
            return JsonResponse({"Status": "Error", "message": "description field is necesary, empty tasks not allowed"}, status=HTTPStatus.BAD_REQUEST)
        try:
            data = Task.objects.filter(id=id_task).get()
        except Task.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Register not exist"}, status=HTTPStatus.NOT_FOUND)
        try:
            Task.objects.filter(id=id_task).update(title=request.data['title'], description=request.data['description'], status=request.data['status'])
        except Exception as e:
            print(e)
            return JsonResponse({"status": "Error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return JsonResponse({"status": "OK", "message": "Update register"}, status=HTTPStatus.OK)
    
    
class Class_DeleteTask(APIView):
    
    @logueado()
    def delete(self, request, id):
        
        try:
            data = Task.objects.filter(id=id).get()
        except Task.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Register not exist"}, status=HTTPStatus.NOT_FOUND)
        try:
            Task.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
            return JsonResponse({"status": "Error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return JsonResponse({"status": "OK", "message": "Task has been delete"}, status=HTTPStatus.OK)