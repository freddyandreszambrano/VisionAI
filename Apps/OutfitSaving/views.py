from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def OutfitSaving(request):
    return render(request, 'saving/saving.html')
    
class OutfitSavingTemplate(TemplateView):
    template_name = 'OutfitSaving/saving/saving.html'