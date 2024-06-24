
from django.urls import path,include
from Apps.Main.views import RopaListView, delete_prenda

app_name = 'Main'
urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
    path('delete_prenda/<int:prenda_id>/', delete_prenda, name='delete_prenda'),  
]

