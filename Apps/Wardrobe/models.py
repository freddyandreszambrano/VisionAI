from django.db import models

class Clothes(models.Model):
    #prenda = models.ImageField(upload_to='Clothes/')
    prenda = models.ImageField()
    categoria = models.CharField(max_length=50)
    dominant_color = models.TextField()
    
    def __str__(self):
        return f"{self.categoria}"