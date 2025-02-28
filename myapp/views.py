from django.shortcuts import render
from django.db import models
from django.db.models import Count
from .models import Product

# Create your views here.
def product_graph(request):
    # Regrouper les produits par mois et année
    products = Product.objects.annotate(month=models.functions.TruncMonth('created_at')) \
                              .values('month') \
                              .annotate(count=Count('id')) \
                              .order_by('month')
 
    # Extraire les mois et les nombres de produits pour le graphique
    months = [product['month'].strftime('%B %Y') for product in products]
    counts = [product['count'] for product in products]
 
    return render(request, 'admin/product_graph.html', {
        'months': months,
        'counts': counts
    })
