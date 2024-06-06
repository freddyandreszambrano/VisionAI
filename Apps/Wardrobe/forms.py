from django import forms
from django.forms import ModelForm
from Apps.Wardrobe.models import Clothes

class ClothesImageForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['prenda']

class ClothesDetailsForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['categoria', 'dominant_color']
        widgets = {
            'categoria': forms.TextInput(attrs={'readonly': True})
        }