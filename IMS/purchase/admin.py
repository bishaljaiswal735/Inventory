from django.contrib import admin
from .models import Supplier, Purchase, PurchaseProduct
# Register your models here.
class PurchaseProductInline(admin.TabularInline):
    model = PurchaseProduct
    extra = 1  # Number of extra blank forms
    fields = ('product', 'size_variation', 'length_variation', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)  # total_price calculated automatically

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name','address','vat_no','phone', 'created_at', 'modified_at')
    search_fields = ('supplier_name', 'phone', 'vat_no')
    list_filter = ('created_at',)
    ordering = ('supplier_name',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'invoice_no', 'date', 'total_amount','tax','Grand_amount')
    search_fields = ('supplier__supplier_name', 'invoice_no')
    list_filter = ('date', 'supplier')
    inlines = [PurchaseProductInline]  # show PurchaseProduct inline
    readonly_fields = ('total_amount','tax', 'Grand_amount')  # total_amount can be calculated automatically later

class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'product', 'size_variation', 'length_variation', 'quantity', 'unit_price', 'total_price')
    search_fields = ('product__product_name', 'purchase__invoice_no')
    list_filter = ('product', 'size_variation', 'length_variation')
    readonly_fields = ('total_price',)


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseProduct, PurchaseProductAdmin)