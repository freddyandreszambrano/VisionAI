from django.db import models

class Clothes(models.Model):
    TYPE_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('deportivo', 'Deportivo'),
    ]
    garment = models.ImageField(upload_to='Clothes/')
    category = models.CharField(max_length=50)
    dominant_color = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.category} - {self.garment.name}"
    
    class Meta:
        verbose_name = "Prenda"
        verbose_name_plural = "Prendas"