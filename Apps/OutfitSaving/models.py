from django.db import models
from Apps.Wardrobe.models import Clothes


class OutfitSaving(models.Model):
    top_clothes = models.ForeignKey(Clothes, related_name='top_outfit', on_delete=models.CASCADE)
    bottom_clothes = models.ForeignKey(Clothes, related_name='bottom_outfit', on_delete=models.CASCADE)
    shoe_clothes = models.ForeignKey(Clothes, related_name='shoe_outfit', on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Outfit Guardado: {self.date_saved}"
    class Meta:
        verbose_name = "Outfit"
        verbose_name_plural = "Outfits"
