from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_video, name="uploads"),
    path("stream/<int:video_hash>/", views.stream_video, name="stream")
]