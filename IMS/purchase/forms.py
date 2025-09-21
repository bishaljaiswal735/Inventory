from django import forms
from .models import Purchase, Supplier
from django.forms import formset_factory

class PurchaseForm(forms.ModelForm): 
    class Meta:
        model = Purchase
        fields = ("supplier",'invoice_no')
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ("supplier_name",'vat_no','phone','address')

class PurchaseProductForm(forms.Form):
    product = forms.CharField(required=True)
    size = forms.CharField(required=False)
    length = forms.CharField(required=False)
    qty = forms.IntegerField(min_value=1, initial=1, required=True)
    price = forms.DecimalField(min_value=0, decimal_places=2, required=True)
    total = forms.CharField(required=True)


# Formset for multiple products
PurchaseProductFormSet = formset_factory(PurchaseProductForm, extra=1)