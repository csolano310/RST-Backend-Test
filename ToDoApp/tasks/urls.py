from django.urls import path
from .views import *

urlpatterns = [
    
    path('tasks', Class_ListTask.as_view()),
    path('tasks/<int:id>', Class_DeleteTask.as_view()),
    path('task/<int:id_task>', Class_EditTask.as_view()),
    path('task', Class_CreateTask.as_view())
]