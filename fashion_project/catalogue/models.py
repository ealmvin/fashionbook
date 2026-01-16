from django.db import models

class Designer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la marque")
    country = models.CharField(max_length=50, verbose_name="Pays d'origine")
    founded_year = models.IntegerField(verbose_name="Année de création")

    def __str__(self):
        return self.name

class Trend(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom de la tendance")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Garment(models.Model):
    # Les champs de base
    name = models.CharField(max_length=200, verbose_name="Nom du vêtement")
    sku = models.CharField(max_length=20, unique=True, verbose_name="Référence SKU")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    description = models.TextField(verbose_name="Description")
    stock_quantity = models.IntegerField(default=0, verbose_name="Stock")
    release_date = models.DateField(verbose_name="Date de sortie")
    
    cover_image_url = models.URLField(max_length=500, verbose_name="URL Image", blank=True)
    
    is_sustainable = models.BooleanField(default=False, verbose_name="Éco-responsable")

    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="garments")
    trends = models.ManyToManyField(Trend, related_name="garments")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"