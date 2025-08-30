from django.shortcuts import render
from .models import Purchase, PurchaseProduct, Supplier
from .forms import PurchaseForm
from django.http import JsonResponse
from stock.models import Product,Size_Variation,Length_Variation
# Create your views here.
def supplier_info(request, supplier_id):
    try:
      supplier = Supplier.objects.get(id = supplier_id)
      data = {'vat_no':supplier.vat_no,'phone':supplier.phone, 'address':supplier.address}
      return JsonResponse(data)
    except Supplier.DoesNotExist:
        return JsonResponse({'error':'Supplier doesn\'t exist'},status=404)

def purchase(request):
    purchases = Purchase.objects.all()
    return render(request,'purchase.html',{'purchases':purchases})

def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(id = purchase_id)
    return render(request,'purchase_detail.html',{'purchase':purchase})

def add_purchase(request):
    form = PurchaseForm()
    products = Product.objects.all()
    sizes = Size_Variation.objects.all()
    lengths = Length_Variation.objects.all()
    return render(request,"add_purchase.html",{"form":form,'products':products,'sizes':sizes,'lengths':lengths})