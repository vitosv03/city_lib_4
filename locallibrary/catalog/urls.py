from django.urls import path
from . import views


# urlpatterns = [
#
# ]

urlpatterns = [
    path('', views.index, name='index'),
]
