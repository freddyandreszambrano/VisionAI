from django.urls import path

from . import views

app_name = 'Account'
urlpatterns = [
    path('', views.show_login_page, name='Account_view'),
]
