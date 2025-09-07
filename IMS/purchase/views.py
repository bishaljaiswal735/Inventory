from django.shortcuts import render, redirect
from .models import Purchase, PurchaseProduct, Supplier
from .forms import PurchaseForm , PurchaseProductFormSet
from django.http import JsonResponse
from stock.models import Product, Size_Variation, Length_Variation
from django.contrib import messages

# Create your views here.
def supplier_info(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        data = {
            "vat_no": supplier.vat_no,
            "phone": supplier.phone,
            "address": supplier.address,
        }
        return JsonResponse(data)
    except Supplier.DoesNotExist:
        return JsonResponse({"error": "Supplier doesn't exist"}, status=404)



def get_products(request):
        query = request.GET.get("q", "")  # get the search term from query string
        if query:
            products = Product.objects.filter(
                product_name__icontains=query, is_avialable = True
            )  # filter by typing
        else:
            products = Product.objects.all()  # if nothing typed, return all products

        # prepare data as list of dicts
        data = [{"id": p.id, "product_name": p.product_name} for p in products]
        return JsonResponse(data, safe=False)

def get_sizes(request, product_id):
       sizes = Size_Variation.objects.filter(product_id=product_id)
       data = [{"id": s.id, "size": s.size} for s in sizes]
       return JsonResponse(data, safe=False)
        
def get_lengths(request, size_id):
    lengths = Length_Variation.objects.filter(size_id=size_id)
    data = [{"id": l.id, "length_in_inch": l.length_in_inch} for l in lengths]
    return JsonResponse(data, safe=False)

def purchase(request):
    purchases = Purchase.objects.all()
    return render(request, "purchase.html", {"purchases": purchases})


def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    return render(request, "purchase_detail.html", {"purchase": purchase})


def add_purchase(request):
   if request.method == "POST":
         form = PurchaseForm(request.POST)
         formset = PurchaseProductFormSet(request.POST,prefix='products')
         for item in formset.cleaned_data:
                        print(item)
         if form.is_valid() and formset.is_valid():
              purchase = form.save(commit=False)
              checkExistingPurchase = Purchase.objects.filter(invoice_no__iexact = purchase.invoice_no).exists()
              if checkExistingPurchase :
                    messages.error(request,"Invoice Number is Matched.Change Invoice Number!!")
                    return render(request,'add_purchase.html',{"form": form,'formset':formset, 'data': request.POST})
              else:
                   purchase.save()
                   for item in formset:
                        purchase_product = PurchaseProduct()
                        purchase_product.purchase = purchase
                        name = item.cleaned_data['product']
                        size = item.cleaned_data['size']
                        length = item.cleaned_data['length']
                        quantity = item.cleaned_data['qty']
                        unit_price = item.cleaned_data['price']
                        print(size,length)
                        try:
                             product = Product.objects.get(product_name__iexact=name)
                        except Product.DoesNotExist:
                            if size == '----' and length == '----':
                             product = Product.objects.create(product_name = name.title(), price = unit_price )  
                            else:
                              product = Product.objects.create(product_name = name.title() )  
                        try:
                             size = Size_Variation.objects.get(product = product,size = size, price_per_unit = unit_price)
                             size.stock += quantity
                             size.save()
                        except Size_Variation.DoesNotExist:
                             size = Size_Variation.objects.create(product = product, size = size, price_per_unit =  unit_price, stock = quantity)
                       

                   return redirect('purchase')
   else:
        form = PurchaseForm()
        formset = PurchaseProductFormSet(prefix='products')
        return render(
            request,
            "add_purchase.html",
            {"form": form,'formset':formset},
        )
