import json
from django.shortcuts import render, redirect
from Apps.Wardrobe.forms import ClothesImageForm, ClothesDetailsForm
from django.views.generic import CreateView, UpdateView
from Apps.Wardrobe.models import Clothes
from django.urls import reverse_lazy
from Neural_Network_Model.Convolutional_Neural_Network.Predict_IA import Fn_Main
from Neural_Network_Model.Get_colors.prediccion_colores_img import Fn_segmentar_y_analizar_prenda

#ingresa y guarda la imagen
class ClothesImageView(CreateView):
    model = Clothes
    form_class = ClothesImageForm
    template_name = 'upload_image.html'

    def form_valid(self, form):
        self.object = form.save()
        # AQUI OCURRE LA MAGIA DE PREDICCIÓN  
        image_path = self.object.garment.path
        predicted_category = Fn_Main(image_path)
        Colores_dominantes = Fn_segmentar_y_analizar_prenda(image_path)
        
        self.object.category = predicted_category
        self.object.dominant_color = json.dumps(Colores_dominantes)
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

    
