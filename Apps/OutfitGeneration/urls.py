
from django.urls import path,include
from Apps.OutfitGeneration.views import OutfitGenerationView, PreseleccionView,SeleccionPrendasOutfitGeneratorView,Eleccion_filtrosView,ProcessSelectionView,ShowSelectionView,GuardarOutfitView

app_name = 'OutfitGeneration'
urlpatterns = [
    path('outfit_generation/', OutfitGenerationView.as_view(), name='outfit_generation'),
    path('outfit_preseleccion/', PreseleccionView.as_view(), name='outfit_preseleccion'),
    path('seleccion_prendas_outfit_generacion/', SeleccionPrendasOutfitGeneratorView.as_view(), name='seleccion_prendas_outfit_generacion'),
    path('Presentar_filtros/', Eleccion_filtrosView.as_view(), name='Presentar_filtros'),
    path('process_selection/', ProcessSelectionView.as_view(), name='process_selection'),
    path('show_selection/', ShowSelectionView.as_view(), name='show_selection'),
    path('Outfit_saving/', GuardarOutfitView.as_view(), name='Outfit_saving'),
]
