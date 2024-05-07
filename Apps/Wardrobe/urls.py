from django.urls import path
from . import views
app_name = 'Wardrobe'
urlpatterns = [
    path('', views.show_Wardrobe, name='Wardrobe_view'),
]
