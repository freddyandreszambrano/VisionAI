from django import forms
from django.forms import ModelForm
from Apps.Wardrobe.models import Clothes

class ClothesForm(ModelForm):
    
    class Meta:
        model= Clothes
        fields = ['prenda', 'categoria']
