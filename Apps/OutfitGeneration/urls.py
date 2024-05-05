
from django.urls import path,include

from . import views

app_name = 'OutfitGeneration'
urlpatterns = [
    path('', views.OutfitGeneration, name='OutfitGeneration'),
]
