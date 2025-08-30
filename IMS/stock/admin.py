from django.contrib import admin
from . models import Product, Size_Variation,Length_Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ("product_name",'slug','created_date','price')

class Size_VariationAdmin(admin.ModelAdmin):
    list_display=("product","size","price_per_unit" ,'stock')
  
class Length_VariationAdmin(admin.ModelAdmin):
    list_display=("size","length_in_inch","total_price" )

admin.site.register(Product, ProductAdmin)
admin.site.register(Size_Variation, Size_VariationAdmin)
admin.site.register(Length_Variation,Length_VariationAdmin)