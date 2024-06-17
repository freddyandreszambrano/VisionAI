from django import forms
from django.forms import ModelForm,widgets
from Apps.Wardrobe.models import Clothes


class ClothesImageForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['garment']




class ClothesDetailsForm(forms.ModelForm):

    class Meta:
        model = Clothes
        fields = ['category', 'dominant_color', 'type']
        widgets = {
            'type': forms.Select(),
        }
    

