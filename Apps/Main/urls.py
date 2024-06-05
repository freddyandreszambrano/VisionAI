
from django.urls import path,include
from Apps.Main.views import RopaListView

app_name = 'Main'
urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
]

