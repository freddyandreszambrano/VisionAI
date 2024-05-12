from django.urls import path,include

from . import views

app_name = 'OutfitSaving'
urlpatterns = [
    path('', views.OutfitSaving, name='OutfitSaving'),

]
