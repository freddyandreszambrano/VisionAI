
from django.urls import path,include
from Apps.Main.views import MainViewTemplate
from . import views

app_name = 'Main'
urlpatterns = [
    path('', views.Main_view, name='main_view'),
    path('', views.Details_view, name='ItemDetails_view'),
    path('', MainViewTemplate.as_view(), name='main_view_tempale'),
]
