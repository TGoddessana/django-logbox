from django.urls import path
from django.http import JsonResponse

def temp_view(request):
    return JsonResponse({"message": "Hello, world!"})

urlpatterns = [
    path('temp/', temp_view, name='temp_view'),
]