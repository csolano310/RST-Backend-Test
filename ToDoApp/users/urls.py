from django.urls import path
from .views import *

urlpatterns = [
    
    path('auth/register', Class_RegisterUser.as_view()),
    path('auth/activate/<str:token>', Class_ActivateUser.as_view()),
    path('auth/login', Class_LoginUser.as_view())
]