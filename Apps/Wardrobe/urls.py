from django.urls import path
from Apps.Wardrobe.views import ClothesImageView, ClothesDetailsView
app_name = 'Wardrobe'
urlpatterns = [
    # path('', views.show_and_save_Wardrobe, name='Wardrobe_view'),
    path('upload/image/', ClothesImageView.as_view(), name='upload_image'),
    path('upload/details/<int:pk>/', ClothesDetailsView.as_view(), name='upload_details'),
]
