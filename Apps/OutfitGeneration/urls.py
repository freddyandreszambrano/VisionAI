
from django.urls import path,include
from Apps.OutfitGeneration.views import OutfitGenerationTemplate
from . import views

app_name = 'OutfitGeneration'
urlpatterns = [
    path('', views.OutfitGeneration, name='OutfitGeneration'),
    path('', OutfitGenerationTemplate.as_view(), name='Outfit_Generation_Template'),
]
