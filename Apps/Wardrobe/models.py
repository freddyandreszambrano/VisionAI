from django.db import models

# Create your models here.
class Clothes(models.Model):
    CATEGORIA_CHOICES = [
        ('camiseta', 'Camiseta'),
        ('pantalon', 'Pantalón'),
        ('zapatos', 'Zapatos'),
        
        # Agrega más opciones según sea necesario
    ]
    prenda = models.ImageField(upload_to='Clothes/')
    categoria = models.CharField(max_length=50)
    dominant_color = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.categoria}"