from django.urls import path
from .views import *


urlpatterns = [
    path('', NoteAPIView.as_view(), name="NoteAPIVIew"),
    path('<int:pk>', NoteAPIView.as_view(), name="NoteAPIVIew")
]
