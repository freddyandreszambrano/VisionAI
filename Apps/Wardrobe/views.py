from django.shortcuts import render, redirect
from Apps.Wardrobe.forms import ClothesImageForm, ClothesDetailsForm
from django.views.generic import CreateView, UpdateView
from Apps.Wardrobe.models import Clothes
from django.urls import reverse_lazy
from Neural_Network_Model.Convolutional_Neural_Network.Predict_IA import Fn_Main

class ClothesImageView(CreateView):
    model = Clothes
    form_class = ClothesImageForm
    template_name = 'upload_image.html'

    def form_valid(self, form):
        self.object = form.save()
        # AQUI OCURRE LA MAGIA DE PREDICCIÓN  
        image_path = self.object.prenda.path
        print(f'Imagen cargada: {image_path}')
        predicted_category = Fn_Main(image_path)
        print(f'Clase predicción: {predicted_category}')
        self.object.categoria = predicted_category
        self.object.save()
        
        return redirect('Wardrobe:upload_details', pk=self.object.pk)

class ClothesDetailsView(UpdateView):
    model = Clothes
    form_class = ClothesDetailsForm
    template_name = 'upload_details.html'

    def get_success_url(self):
        return reverse_lazy('Main:Main_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clothes'] = self.object
        return context
    
    
    
