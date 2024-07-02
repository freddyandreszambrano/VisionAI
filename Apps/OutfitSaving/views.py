from django.shortcuts import render, redirect, get_object_or_404
from Apps.OutfitSaving.models import OutfitSaving
from django.urls import reverse

def OutfitSavingView(request):
    outfits = OutfitSaving.objects.all()
    return render(request, 'saving/saving.html', {'outfits': outfits})


def delete_outfit(request, outfit_id):
    outfit = get_object_or_404(OutfitSaving, id=outfit_id)
    outfit.delete()
    return redirect(reverse('OutfitSaving:OutfitSaving'))