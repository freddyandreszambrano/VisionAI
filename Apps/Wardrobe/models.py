from django.db import models

class Clothes(models.Model):
    TYPE_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('Deportivo', 'Deportivo'),
    ]
    garment = models.ImageField(upload_to='clothes/')
    category = models.CharField(max_length=50)
    dominant_color = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.category} - {self.type}"
    
    class Meta:
        verbose_name = "Garment"
        verbose_name_plural = "Garments"