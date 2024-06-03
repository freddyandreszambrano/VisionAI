
from django.urls import path,include
from Apps.Main.views import RopaListView

app_name = 'Main'


urlpatterns = [
    path('Main/list', RopaListView.as_view(), name='Main_list'),
]

