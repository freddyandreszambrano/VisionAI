from django.shortcuts import render

# Create your views here.
def show_Wardrobe(request):
    return render(request, 'Wardrobe.html')