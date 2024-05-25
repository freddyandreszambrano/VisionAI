from django.urls import path
from .views import login_view, register, logout, edit_profile

from . import views

app_name = 'Account'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/',views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

