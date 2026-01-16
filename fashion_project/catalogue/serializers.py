from rest_framework import serializers
from .models import Garment, Designer, Trend

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['id', 'name']

class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = ['id', 'name', 'country']

class GarmentSerializer(serializers.ModelSerializer):
    # On veut voir le nom du designer, pas juste son ID (ex: "Chanel" au lieu de "12")
    designer_name = serializers.ReadOnlyField(source='designer.name')
    
    # Pour les tendances, on veut la liste des noms
    trends = serializers.StringRelatedField(many=True)

    class Meta:
        model = Garment
        fields = ['id', 'name', 'sku', 'price', 'description', 
                  'cover_image_url', 'stock_quantity', 
                  'designer_name', 'trends', 'is_sustainable']