from django.urls import path
from .views import registro, login_request

from . import views

app_name = 'Account'
urlpatterns = [
    #path('', views.show_Base_account_page, name='Account_view'),
    path('', views.login_request, name='login'),
    path('registro/',views.registro, name='registro'),
    path('logout/', views.logout_request, name='logout'),
]
