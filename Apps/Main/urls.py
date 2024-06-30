
from django.urls import path,include
from Apps.Main.views import RopaListView, delete_prenda, prenda_detail

app_name = 'Main'

urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
    path('delete_prenda/<int:prenda_id>/', delete_prenda, name='delete_prenda'),  
    path('details/<int:prenda_id>/', prenda_detail, name='detail_prenda'),
]

