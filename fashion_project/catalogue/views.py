from django.shortcuts import render
from django.db.models import Sum, Count

# Imports pour l'API (Django Rest Framework)
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

# Imports pour les Graphiques (Matplotlib)
import matplotlib.pyplot as plt
import io
import urllib, base64

# Imports de tes propres fichiers (Modèles et Serializers)
from .models import Garment, Designer, Trend
from .serializers import GarmentSerializer, DesignerSerializer, TrendSerializer

# ==========================================
# PARTIE 1 : STATISTIQUES (Back-Office)
# ==========================================

def get_graph():
    """Fonction utilitaire pour convertir le graphique Matplotlib en image affichable"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')

def stats_view(request):
    # --- GRAPHIQUE 1 : Histogramme des Stocks (Bar Chart) ---
    plt.switch_backend('Agg') 
    data_stock = Garment.objects.values('designer__name').annotate(total_stock=Sum('stock_quantity'))
    
    names = [entry['designer__name'] for entry in data_stock]
    stocks = [entry['total_stock'] for entry in data_stock]

    plt.figure(figsize=(8, 5))
    plt.bar(names, stocks, color='#4e73df') # Bleu pro
    plt.title('Stock par Créateur', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    graph_stock = get_graph()
    plt.close() # Important pour nettoyer la mémoire

    # --- GRAPHIQUE 2 : Répartition Éco-responsable (Pie Chart) ---
    # On compte combien sont True et combien sont False
    sustainable_count = Garment.objects.filter(is_sustainable=True).count()
    not_sustainable_count = Garment.objects.filter(is_sustainable=False).count()

    labels = ['Éco-responsable', 'Standard']
    sizes = [sustainable_count, not_sustainable_count]
    colors = ['#1cc88a', '#858796'] # Vert et Gris

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Répartition Écologique', fontsize=14)
    plt.tight_layout()
    graph_eco = get_graph()
    plt.close()

    # On envoie les deux graphiques au template
    context = {
        'graph_stock': graph_stock,
        'graph_eco': graph_eco,
        'total_garments': Garment.objects.count()
    }
    return render(request, 'stats.html', context)


# ==========================================
# PARTIE 2 : API (Pour React)
# ==========================================

# Configuration de la pagination (12 articles par page pour le catalogue)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'

# API pour les Vêtements
class GarmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Garment.objects.all().order_by('-id') # Les plus récents en premier
    serializer_class = GarmentSerializer
    pagination_class = StandardResultsSetPagination
    
    # Activation des filtres (Recherche et Tri)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'designer__name'] # Chercher par nom ou marque
    ordering_fields = ['price', 'release_date']

# API pour les Designers (Marques)
class DesignerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer

# API pour les Tendances
class TrendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer