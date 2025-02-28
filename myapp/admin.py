from django.contrib import admin
from django.contrib import messages
from decimal import Decimal
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Product,Category,Supplier,SupplierDetail
#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('image_tag','name', 'price', 'quantity','stock_status','supplier','formatted_created_at','short_description','categories_list')
    search_fields = ('name','price')
    list_filter = ('created_at','price','quantity')
    ordering = ('-created_at',)
    fields = ('name' , 'price', 'description','quantity','categories','image','image_tag','supplier','created_at' )
    readonly_fields = ('created_at','image_tag')
    list_per_page = 10
    def formatted_created_at(self,obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M:%S')
    formatted_created_at.short_description = 'Ajouté le'
    def short_description(self,obj):
        return obj.description[:20] + '...'
    short_description.short_description = 'Description'

    actions = ['set_price_zero','duplicate_products','apply_discount']
    def set_price_zero(self,request,queryset):
        queryset.update(price=0)
        self.message_user(request,'Le prix des produits selectionnés a été mis à 0')
    set_price_zero.short_description = 'Mettre le prix à 0'

    def duplicate_products(self,request,queryset):
        for obj in queryset:
            obj.pk = None
            obj.save()
        self.message_user(request,'Les produits selectionnés ont été dupliqués')    
    duplicate_products.short_description = 'Dupliquer les produits'
    
    def apply_discount(self, request, queryset):
        """
        Applique une remise de 10% sur les produits sélectionnés.
        """
        discount_percentage = Decimal("10.0")  # Utiliser Decimal
        for product in queryset:
            if product.price:  # Vérifier que price est défini
                new_price = Decimal(product.price) * (Decimal("1.0") - discount_percentage / Decimal("100.0"))
                product.price = new_price.quantize(Decimal("0.01"))  # Arrondi à 2 décimales
                product.save()

        self.message_user(request, f"Une remise de 10% a été appliquée.", messages.SUCCESS)

    apply_discount.short_description = "Appliquer une remise de 10 pourcent"

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />'.format(obj.image.url))
        return "Pas d'image"

    image_tag.short_description = 'Aperçu'


    
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','products_list','products_count']    
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    fields = ['name',]
    list_per_page = 10 

 # Admin pour SupplierDetail
@admin.register(SupplierDetail)  # Utiliser le nouveau nom ici
class SupplierDetailAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'address', 'contact_email', 'website', 'contact_person',)
    search_fields = ('contact_person',)
    list_filter = ('supplier',)
    fields = ('supplier', 'address', 'contact_email', 'website', 'contact_person', 'supplier_type', 
               'country', 'payment_terms', 'bank_account', 'region_served')
    list_per_page = 10   
 
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fields = ('name', 'phone',)
    list_display = ('name', 'phone')
    search_fields = ['name']


