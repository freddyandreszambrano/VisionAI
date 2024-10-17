
from django.urls import path,include
from Apps.OutfitGeneration.views import PreseleccionView

app_name = 'OutfitGeneration'
urlpatterns = [
    path('outfit_preseleccion/', PreseleccionView.as_view(), name='outfit_preseleccion'),
]
