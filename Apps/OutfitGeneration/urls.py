
from django.urls import path,include
from Apps.OutfitGeneration.views import OutfitGenerationView

app_name = 'OutfitGeneration'
urlpatterns = [
    path('outfit_generation/', OutfitGenerationView.as_view(), name='outfit_generation'),
]
