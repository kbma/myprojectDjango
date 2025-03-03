from django.shortcuts import render
from .models import Product, HomePage
from .forms import CommandeForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Commande
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os


# Create your views here.
def home(request):
    products = Product.objects.filter(quantity__gt=0)  # Récupère seulement les produits avec quantité > 0
    home_data = HomePage.objects.first()
    return render(request, 'home.html', {'home_data':home_data,'products': products})

def commande(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Récupération du produit
    if request.method == "POST":
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.product = product
            commande.save()
            return redirect('commande_confirmation', commande.id)
    else:
        form = CommandeForm()
    
    return render(request, 'commande.html', {'form': form, 'product': product})

def commande_confirmation(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande_confirmation.html', {'commande': commande})

def generate_pdf(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="commande_{commande.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # 📌 Ajout du logo (remplace 'logo.png' par le chemin réel de ton logo)
    logo_path = os.path.join("media", "logo.png")  # Change le chemin selon ton projet
    if os.path.exists(logo_path):
        p.drawImage(ImageReader(logo_path), 50, height - 47, width=80, height=25, mask='auto')

    # 📌 En-tête du PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"Confirmation de Commande - #{commande.id}")

    # 📌 Ligne de séparation
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 60, 550, height - 60)

    # 📌 Informations sur la commande
    p.setFont("Helvetica", 12)
    y_position = height - 100  # Position de départ

    details = [
        ("Nom du client", commande.customer_name),
        ("Produit", commande.product.name),
        ("Quantité", str(commande.quantity)),
        ("Adresse de livraison", commande.customer_address),
        ("Méthode de paiement", commande.payment),
        ("Date de commande", commande.created_at.strftime("%d/%m/%Y %H:%M")),
        ("Total", f"{commande.quantity * commande.product.price} €"),
    ]

    for label, value in details:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y_position, f"{label} :")
        p.setFont("Helvetica", 12)
        p.drawString(250, y_position, value)
        y_position -= 25  # Espacement entre les lignes

    # 📌 Ligne de fin
    p.line(50, y_position - 10, 550, y_position - 10)

    # 📌 Remerciement
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position - 40, "Merci pour votre confiance ! 🚀")

    p.showPage()
    p.save()

    return response

