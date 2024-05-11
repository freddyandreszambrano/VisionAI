from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def OutfitGeneration(request):
    return render(request, 'Outfit_Generation/OutfitGeneration.html')

class OutfitGenerationTemplate(TemplateView):
    template_name = 'OutfitGeneration/Outfit_Generation/OutfitGeneration.html'