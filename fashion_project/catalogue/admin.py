from django.contrib import admin
from django.http import HttpResponse
from .models import Designer, Trend, Garment

# exporter en PDF 
import reportlab
from reportlab.pdfgen import canvas

def export_to_pdf(modeladmin, request, queryset):
    """
    Cette fonction génère un PDF simple avec la liste des vêtements sélectionnés.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="catalogue_fashionbook.pdf"'

    p = canvas.Canvas(response)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "FashionBook - Export Catalogue")
    
    p.setFont("Helvetica", 12)
    y = 750 
    
    for garment in queryset:
        text = f"- {garment.name} ({garment.designer.name}) : {garment.price} euros"
        p.drawString(50, y, text)
        y -= 20 
        
        if y < 50: 
            p.showPage() 
            y = 800      

    p.save()
    return response

export_to_pdf.short_description = "Générer un PDF des éléments sélectionnés"

# tables 
@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'designer', 'price', 'stock_quantity', 'is_sustainable')
    
    search_fields = ('name', 'sku', 'designer__name')
    
    list_filter = ('is_sustainable', 'designer', 'trends')
    
    list_editable = ('stock_quantity', 'price')
    
    list_per_page = 20

    actions = [export_to_pdf]