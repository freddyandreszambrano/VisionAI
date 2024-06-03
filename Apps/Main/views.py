from django.views.generic import ListView
from Apps.Wardrobe.models import Clothes


class RopaListView(ListView):
    model = Clothes
    template_name = 'Home/main.html'
    context_object_name = 'prendas'



