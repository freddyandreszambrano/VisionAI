from django.shortcuts import render

# Create your views here.
def OutfitSaving(request):
    return render(request, 'saving/saving.html')