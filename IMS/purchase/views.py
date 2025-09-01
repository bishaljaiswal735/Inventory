from django.shortcuts import render
from .models import Purchase, PurchaseProduct, Supplier
from .forms import PurchaseForm
from django.http import JsonResponse
from stock.models import Product, Size_Variation, Length_Variation


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
    form = PurchaseForm()
    products = Product.objects.all()
    sizes = Size_Variation.objects.all()
    lengths = Length_Variation.objects.all()
    return render(
        request,
        "add_purchase.html",
        {"form": form, "products": products, "sizes": sizes, "lengths": lengths},
    )
