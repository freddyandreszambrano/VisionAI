from django.urls import path,include
from Apps.OutfitSaving.views import OutfitSavingTemplate
from . import views

app_name = 'OutfitSaving'
urlpatterns = [
    path('', views.OutfitSaving, name='OutfitSaving'),
    path('', OutfitSavingTemplate.as_view(), name='Outfit_Saving_Template'),
]
