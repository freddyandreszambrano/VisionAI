
from django.urls import path,include
from Apps.OutfitGeneration.views import OutfitGenerationView, PreseleccionView,SeleccionPrendasOutfitGeneratorView,ProcesarSeleccionView,Eleccion_filtrosView

app_name = 'OutfitGeneration'
urlpatterns = [
    path('outfit_generation/', OutfitGenerationView.as_view(), name='outfit_generation'),
    path('outfit_preseleccion/', PreseleccionView.as_view(), name='outfit_preseleccion'),
    path('seleccion_prendas_outfit_generacion/', SeleccionPrendasOutfitGeneratorView.as_view(), name='seleccion_prendas_outfit_generacion'),
    path('procesar_seleccion/', ProcesarSeleccionView.as_view(), name='procesar_seleccion'),
    path('Presentar_filtros/', Eleccion_filtrosView.as_view(), name='Presentar_filtros'),
]
