from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def show_Wardrobe(request):
    return render(request, 'Wardrobe.html')

class WardrobeTemplate(TemplateView):
    template_name = 'Wardrobe/Wardrobe.html'