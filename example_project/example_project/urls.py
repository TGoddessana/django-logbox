from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ok/", views.ok_view),
    path("handled_error/", views.handled_error_view),
    path("unhandled_error/", views.unhandled_error_view),
]
