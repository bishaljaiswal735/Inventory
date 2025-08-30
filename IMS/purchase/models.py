from django.db import models
from stock.models import Product, Size_Variation, Length_Variation
from django.db.models import Sum
from decimal import Decimal


# Create your models here.
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    vat_no = models.IntegerField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
       return self.supplier_name
    
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    invoice_no = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    Grand_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0)

   
    def __str__(self):
       return f'{self.supplier} {self.invoice_no}'

class PurchaseProduct(models.Model):
        purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        size_variation = models.ForeignKey(Size_Variation, on_delete=models.CASCADE, null=True, blank=True)
        length_variation = models.ForeignKey(Length_Variation, on_delete=models.CASCADE, null=True, blank=True)
        quantity = models.DecimalField(max_digits=10, decimal_places=2)
        unit_price = models.DecimalField(max_digits=10, decimal_places=2)
        total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank = True)
   
        def save(self, *args, **kwargs):
        # calculate total price automatically
            self.total_price = self.unit_price * self.quantity
            super().save(*args, **kwargs)

            total_amt = self.purchase.items.aggregate(total = Sum('total_price'))['total'] or 0
            tax_amt = total_amt * Decimal('0.13')
            self.purchase.total_amount = total_amt
            self.purchase.tax = tax_amt
            self.purchase.Grand_amount = total_amt + tax_amt
            self.purchase.save()