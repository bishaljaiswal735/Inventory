from django.contrib import admin
from . models import Product, Size_Variation,Length_Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ("product_name",'slug','size','length','stock','created_date','modified_date')

class Size_VariationAdmin(admin.ModelAdmin):
    list_display=("size",)
  
class Length_VariationAdmin(admin.ModelAdmin):
    list_display=("length_in_inch", )

admin.site.register(Product, ProductAdmin)
admin.site.register(Size_Variation, Size_VariationAdmin)
admin.site.register(Length_Variation,Length_VariationAdmin)