from django.urls import path,include

from Apps.OutfitSaving.views import OutfitSavingView, delete_outfit
# from Apps.OutfitSaving.views import OutfitSavingView

app_name = 'OutfitSaving'
urlpatterns = [
    path('', OutfitSavingView, name='OutfitSaving'),
    path('delete_outfit/<int:outfit_id>/', delete_outfit, name='delete_outfit'),
]
