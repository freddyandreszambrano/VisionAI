from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def Main_view(request):
    return render(request, 'Home/main.html')

def Details_view(request):
    return render(request, 'Item_details/details.html')
    
class MainViewTemplate(TemplateView):
    template_name = 'Main/Home/main.html'
