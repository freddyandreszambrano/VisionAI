from django.urls import path
from Apps.Wardrobe.views import WardrobeTemplate
from . import views
app_name = 'Wardrobe'
urlpatterns = [
    path('', views.show_Wardrobe, name='Wardrobe_view'),
    path('', WardrobeTemplate.as_view(), name='Wardrobe_Template'),
]
