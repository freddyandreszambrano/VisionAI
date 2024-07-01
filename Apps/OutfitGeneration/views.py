import json
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from Apps.Wardrobe.models import Clothes
from Apps.OutfitSaving.models import OutfitSaving 
from Apps.OutfitGeneration.Logic.Load_Model import generate_outfits
from Apps.OutfitGeneration.Logic.Get_outfits import Fn_generate_outfits
from Apps.OutfitGeneration.Logic.filtros_outfi import function_generate_outfits
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import logging

class PreseleccionView(TemplateView):
    template_name = 'PreSeleccion_Outfit/Preseleccion.html'
    


class OutfitGenerationView(CreateView):
    model = Clothes
    template_name = 'Outfit_Generation/OutfitGeneration.html'
    context_object_name = 'ctx_clothes'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_clothes = Clothes.objects.all()
        
        lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
        lista_categorias_inferior = ['Trouser']
        lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']
        
        prendas_superior = [g for g in all_clothes if g.category in lista_categorias_superior]
        prendas_inferior = [g for g in all_clothes if g.category in lista_categorias_inferior]
        prendas_zapatos = [g for g in all_clothes if g.category in lista_categorias_zapatos]

        if not prendas_superior or not prendas_inferior or not prendas_zapatos:
            context['error'] = "No hay suficientes prendas para generar un outfit."
            return context

        all_data_for_generation = [
            {
                'id': clothes.id,
                'category': clothes.category,
                'dominant_color': clothes.dominant_color,
                'image': clothes.garment.url  
            }
            for clothes in all_clothes
        ]

        model_path = 'Outfit_Generator_Model.h5'
        try:
            outfits = generate_outfits(model_path, all_data_for_generation, num_outfits=3)  
            context['outfits'] = outfits
        except Exception as e:
            logging.error("Error al generar outfits: %s", e)
            context['error'] = "Hubo un error al generar outfits. Inténtelo de nuevo más tarde."

        return context



    
    
class SeleccionPrendasOutfitGeneratorView(TemplateView):
    model = Clothes
    template_name = 'Seleccion_Prenda/SeleccionPrenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctx_Prendas_superior'] = Clothes.objects.filter(category__in=['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt'])
        context['ctx_Prendas_inferior'] = Clothes.objects.filter(category__in=['Trouser'])
        context['ctx_zapato'] = Clothes.objects.filter(category__in=['Sneaker', 'Sandal', 'Ankle boot'])
        return context


class ProcessSelectionView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        request.session['selected_items'] = data
        return JsonResponse({'status': 'success'})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'fail'})

class ShowSelectionView(TemplateView):
    template_name = 'outfit_preseleccionado/outfit_preseleccionado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_items = self.request.session.get('selected_items', {})
        
        if not selected_items:
            context['error'] = "No se han seleccionado prendas."
            return context
        
        if not (selected_items.get('superior') and selected_items.get('inferior') and selected_items.get('zapatos')):
            context['error'] = "Debe elegir al menos una prenda de cada categoría (superior, inferior y zapatos)."
            return context
        
        ids_to_fetch = [int(item['id']) for item in selected_items.values() if item]
        selected_clothes = Clothes.objects.filter(id__in=ids_to_fetch)

        for clothes in selected_clothes:
            for key in selected_items:
                if selected_items[key] and clothes.id == int(selected_items[key]['id']):
                    selected_items[key]['dominant_color'] = clothes.dominant_color

        model_path = 'Outfit_Generator_Model.h5'
        all_clothes = Clothes.objects.all()

        all_data_for_generation = []
        for clothes in all_clothes:
            if (selected_items.get('superior') and clothes.id == int(selected_items['superior']['id'])) or \
            (selected_items.get('inferior') and clothes.id == int(selected_items['inferior']['id'])) or \
            (selected_items.get('zapatos') and clothes.id == int(selected_items['zapatos']['id'])):
                continue  

            all_data_for_generation.append({
                'id': clothes.id,
                'category': clothes.category,
                'dominant_color': clothes.dominant_color,
                'image': clothes.garment.url
            })
        

        context['selected_items'] = selected_items
        print(f'data seleccion de items con color {selected_items}')
        try:
            outfits = Fn_generate_outfits(model_path, selected_items, all_data_for_generation, num_outfits=3)
            context['outfits'] = outfits
        except Exception as e:
            logging.error("Error al generar outfits: %s", e)
            context['error'] = "Hubo un error al generar outfits. Inténtelo de nuevo más tarde."

        return context
    

class Eleccion_filtrosView(TemplateView):
    template_name = 'PresentarFiltros/Prensentar_filtros.html'

class FiltrosOutfitGenerationView(CreateView):
    model = Clothes
    template_name = 'PresentarFiltros/outfit_filtros.html'
    context_object_name = 'ctx_clothes'
    fields = '__all__'
    
    def Fn_load_json_type_combinations(self):
        try:
            with open('Color_combinations_type_classes.json', 'r') as file:
                Tipo_de_combinaciones = json.load(file)
                return Tipo_de_combinaciones
        except Exception as e:
            print(f"Error al cargar el archivo de combinaciones: {e}")
            
    def get(self, request, *args, **kwargs):
        label = request.GET.get('label', None)
        if label:
            print(f"Label recibido: {label}")
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_clothes = Clothes.objects.all()
        
        Type_combinations = self.Fn_load_json_type_combinations()
        print(f"Type_combinations: {Type_combinations}")
        
        label = self.request.GET.get('label', None)
        if label:
            context['label'] = label
            print(f"Label en contexto: {label}")
            
        lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
        lista_categorias_inferior = ['Trouser']
        lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']
        
        if label == 'DIA':
            prendas_superior = [g for g in all_clothes if g.category in lista_categorias_superior and g.type in ['casual', 'deportivo']]
            prendas_inferior = [g for g in all_clothes if g.category in lista_categorias_inferior and g.type in ['casual', 'deportivo']]
            prendas_zapatos = [g for g in all_clothes if g.category in lista_categorias_zapatos and g.type in ['casual', 'deportivo']]
        elif label == 'NOCHE':
            prendas_superior = [g for g in all_clothes if g.category in lista_categorias_superior and g.type in ['casual', 'formal']]
            prendas_inferior = [g for g in all_clothes if g.category in lista_categorias_inferior and g.type in ['casual', 'formal']]
            prendas_zapatos = [g for g in all_clothes if g.category in lista_categorias_zapatos and g.type in ['casual', 'formal']]
        elif label == 'BODA':
            prendas_superior = [g for g in all_clothes if g.category in lista_categorias_superior and g.type in ['formal']]
            prendas_inferior = [g for g in all_clothes if g.category in lista_categorias_inferior and g.type in ['formal']]
            prendas_zapatos = [g for g in all_clothes if g.category in lista_categorias_zapatos and g.type in ['formal']]
        else:
            prendas_superior = [g for g in all_clothes if g.category in lista_categorias_superior]
            prendas_inferior = [g for g in all_clothes if g.category in lista_categorias_inferior]
            prendas_zapatos = [g for g in all_clothes if g.category in lista_categorias_zapatos]

        if not prendas_superior or not prendas_inferior or not prendas_zapatos:
            context['error'] = "No hay suficientes prendas para generar un outfit."
            return context

        all_filtered_clothes = prendas_superior + prendas_inferior + prendas_zapatos
        print(f"filtro: {label}   all_filtered_clothes: {all_filtered_clothes}")
        all_data_for_generation = [
            {
                'id': clothes.id,
                'category': clothes.category,
                'dominant_color': clothes.dominant_color,
                'image': clothes.garment.url  # Asegúrate de que el campo 'garment' esté en el modelo Clothes
            }
            for clothes in all_filtered_clothes
        ]

        model_path = 'Outfit_Generator_Model.h5'
        try:
            outfits = function_generate_outfits(model_path, all_data_for_generation, label)  
            context['outfits'] = outfits
        except Exception as e:
            logging.error("Error al generar outfits: %s", e)
            context['error'] = "Hubo un error al generar outfits. Inténtelo de nuevo más tarde."

        return context


@method_decorator(csrf_exempt, name='dispatch')
class GuardarOutfitView(View):
    def post(self, request, *args, **kwargs):
        prenda_superior_id = request.POST.get('prenda_superior_id')
        prenda_inferior_id = request.POST.get('prenda_inferior_id')
        zapato_id = request.POST.get('zapato_id')

        try:
            prenda_superior = Clothes.objects.get(id=prenda_superior_id)
            prenda_inferior = Clothes.objects.get(id=prenda_inferior_id)
            zapato = Clothes.objects.get(id=zapato_id) if zapato_id else None

            outfit = Clothes(prenda_superior, prenda_inferior=prenda_inferior, zapato=zapato)
            outfit.save()

            return JsonResponse({'success': True})
        except Clothes.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Prenda no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': False, 'error': 'Método no permitido'})



