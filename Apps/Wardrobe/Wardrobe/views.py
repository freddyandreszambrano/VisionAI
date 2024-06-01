from django.shortcuts import render, redirect
from Apps.Wardrobe.forms import ClothesForm
from Apps.Wardrobe.models import Clothes



# Create your views here.
# def show_Wardrobe(request):
#     return render(request, 'Wardrobe.html')

    
def show_and_save_Wardrobe(request):
    if request.method == 'POST':
        form = ClothesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Wardrobe:Wardrobe_view')
    else:
        form = ClothesForm()
    
    # Obtener todas las prendas para mostrarlas junto con el formulario
    prendas = Clothes.objects.all()

    return render(request, 'wardrobe.html', {'form': form, 'prendas': prendas})
