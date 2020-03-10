from django.urls import path
from .views import *

urlpatterns = [
    path('reg/', RegView.as_view()),
    path('login/', LoginView.as_view()),
    path('music/', Get_musicAPI.as_view()),
]
