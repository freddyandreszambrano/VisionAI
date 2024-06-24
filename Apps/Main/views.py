from django.views.generic import ListView
from Apps.Wardrobe.models import Clothes

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from Apps.Wardrobe.models import Clothes

class RopaListView(ListView):
    model = Clothes
    template_name = 'Home/main.html'
    context_object_name = 'prendas'


def delete_prenda(request, prenda_id):
    prenda = get_object_or_404(Clothes, id=prenda_id)
    prenda.delete()
    return redirect(reverse('Main:Main_list'))

