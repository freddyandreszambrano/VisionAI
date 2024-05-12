from django.shortcuts import render

# Create your views here.
def OutfitGeneration(request):
    return render(request, 'Outfit_Generation/OutfitGeneration.html')

