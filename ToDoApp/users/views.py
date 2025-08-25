from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus
from .models import User
from django.http import Http404
from utilidades import utilidades
import datetime
import time
import uuid
import os
from dotenv import dotenv_values
from django.contrib.auth.hashers import make_password, check_password
from jose import jwt
from django.conf import settings
# Create your views here.

class Class_RegisterUser(APIView):
    
    def post(self, request):
        
        if request.data.get("name") == None or not(request.data.get("name")):
            return JsonResponse({"Status": "Error", "message": "name field is necesary"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("email") == None or not(request.data.get("email")):
            return JsonResponse({"Status": "Error", "message": "email field is necesary"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password") == None or not(request.data.get("password")):
            return JsonResponse({"Status": "Error", "message": "password field is necesary"}, status=HTTPStatus.BAD_REQUEST)
        if User.objects.filter(email=request.data['email']).exists():
            return JsonResponse({"status": "Error", "message": "Email already exists"}, status=HTTPStatus.BAD_REQUEST)
        try:
            uuidVar = uuid.uuid4()
            hash = make_password(request.data['password'])
            User.objects.create(name=request.data['name'], email=request.data['email'], password_hash=hash, created_at=datetime.datetime.now(), active=False, token=uuidVar)
            url = f"{os.getenv("BASE_URL")}auth/activate/{uuidVar}"
            html=f"""
            <h3>Verificación de cuenta</h3>
            Hola {request.data['name']}, estás a punto de ser parte de la familia ToDo-App.<br/>
            
            Haz click en el siguiente enlace para verificar tu cuenta.<br/>
            <a href="{url}">{url}</a> 
            """
            utilidades.sendMail(html, "Verificación", request.data['email'])
        except Exception as e:
            print(e)
            return JsonResponse({"status": "Error", "message": "Internal Server Error"}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse({"status": "OK", "message": "Created"}, status=HTTPStatus.CREATED)

class Class_ActivateUser(APIView):
    
    def get(self, request, token):
        if token==None or not token:
            return JsonResponse({"status": "error", "message":"Not found"}, status=Http404)
        try:
            tok = User.objects.filter(token=token).get()
            print(tok)
            User.objects.filter(id=tok.id).update(active=1)
            User.objects.filter(id=tok.id).update(token="")
            return HttpResponseRedirect(os.getenv("BASE_FRONTEND"))
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            
class Class_LoginUser(APIView):
    
    def post(self, request):
        
        if request.data.get("email")==None or not request.data.get("email"):
            return JsonResponse({"status": "error", "message": "Bad Request"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("password")==None or not request.data.get("password"):
            return JsonResponse({"status": "error", "message": "Bad Request"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            user = User.objects.filter(email=request.data.get("email")).get()
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not exists, try register user"}, status=HTTPStatus.NOT_FOUND)
        
        if user.active==0:
            return JsonResponse({"status": "error", "message": "User is inactive, check your email to activate your account"}, status=HTTPStatus.NOT_FOUND)
        auth = check_password(request.data.get("password"), user.password_hash)
        if auth is True:
            date = datetime.datetime.now()
            after = date + datetime.timedelta(days=1)
            date_number = int(datetime.datetime.timestamp(after))
            payload = {"id": user.id, "ISS": os.getenv("BASE_URL"), "iat": int(time.time()), "exp": int(date_number)}
            try:
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id": user.id, "name": user.name, "token": token})
            except Exception as e:
                print(e)
                return JsonResponse({"status": "error", "message": "Internal Server Error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)    
        else:
            return JsonResponse({"status": "error", "message": "User or password invalid"}, status=HTTPStatus.BAD_REQUEST)