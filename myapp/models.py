from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Catégorie'
 
    def __str__(self):
        return self.name
    @property
    def products_list(self):
        products = self.product_set.all()  # Récupérer tous les produits liés à cette catégorie
        if products.exists():
            return ", ".join(product.name for product in products)
        return "Aucun produit"

    products_list.fget.short_description = "Produits associés"

    def products_count(self):
        return self.product_set.count()
    products_count.short_description = "Nombre de produits"
    



class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=255)
 
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Fournisseur'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    quantity= models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL , null=True, blank=True,related_name='products')
    categories = models.ManyToManyField(Category, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Produit'
    
    @property
    def categories_list(self):
        cats = self.categories.all()
        if cats.exists():
            return ", ".join(cat.name for cat in cats)
        return "Aucune catégorie"
    categories_list.fget.short_description = "Catégories"
    
    @property
    def stock_status(self):
        if self.quantity > 0:
            return 'En stock'
        return 'Rupture de stock'
    stock_status.fget.short_description = 'Stock'


class SupplierDetail(models.Model): 
    supplier = models.OneToOneField(Supplier, on_delete=models.SET_NULL , null=True, blank=True, related_name='details')
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    supplier_type = models.CharField(
        max_length=50, 
        choices=[('distributeur', 'Distributeur'), ('fabricant', 'Fabricant'), ('revendeur', 'Revendeur')],
        blank=True, 
        null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    bank_account = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    region_served = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Details of {self.supplier.name}"

    class Meta:
        verbose_name = 'Détail Fournisseur'
        verbose_name_plural = 'Détails Fournisseurs'