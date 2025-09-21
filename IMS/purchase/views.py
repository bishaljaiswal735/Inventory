from django.shortcuts import render, redirect, get_object_or_404
from .models import Purchase, PurchaseProduct, Supplier
from .forms import PurchaseForm, PurchaseProductFormSet, SupplierForm
from django.http import JsonResponse
from stock.models import Product, Size_Variation, Length_Variation
from django.contrib import messages
from django.db.models import Q



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
            product_name__icontains=query, is_avialable=True
        )  # filter by typing
    else:
        products = Product.objects.all()  # if nothing typed, return all products

    # prepare data as list of dicts
    data = [{"id": p.id, "product_name": p.product_name} for p in products]
    return JsonResponse(data, safe=False)


def get_sizes(request):
    sizes = Size_Variation.objects.all()
    data = [{"id": s.id, "size": s.size} for s in sizes]
    return JsonResponse(data, safe=False)


def get_lengths(request):
    lengths = Length_Variation.objects.all()
    data = [{"id": l.id, "length_in_inch": l.length_in_inch} for l in lengths]
    return JsonResponse(data, safe=False)


def purchase(request):
    query = request.GET.get('q','').strip()
    if query:
        purchases = Purchase.objects.filter(supplier__supplier_name__icontains=query).order_by("-date")
    else:
        purchases = Purchase.objects.all().order_by("-date")
    return render(request, "purchase.html", {"purchases": purchases})


def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    return render(request, "purchase_detail.html", {"purchase": purchase})


def add_purchase(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseProductFormSet(request.POST, prefix="products")
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            checkExistingPurchase = Purchase.objects.filter(
                invoice_no__iexact=purchase.invoice_no
            ).exists()
            if checkExistingPurchase:
                messages.error(
                    request, "Invoice Number is Matched.Change Invoice Number!!"
                )
                return render(
                    request,
                    "add_purchase.html",
                    {"form": form, "formset": formset, "data": request.POST},
                )
            else:
                purchase.save()
                for item in formset:
                    name = item.cleaned_data["product"]
                    size = item.cleaned_data["size"]
                    length = item.cleaned_data["length"]
                    quantity = item.cleaned_data["qty"]
                    unit_price = item.cleaned_data["price"]

                    # Normalize empty values
                    size = None if size in ("", "----") else size
                    length = None if length in ("", "----") else length

                    # Get or create size/length variations
                    size_obj = Size_Variation.objects.get_or_create(size=size)[0] if size else None
                    length_obj = Length_Variation.objects.get_or_create(length_in_inch=length)[0] if length else None

                    # Check if product exists
                    product = Product.objects.filter(
                        product_name__iexact=name,
                        size=size_obj,
                        length=length_obj
                    ).first()

                    if product:
                        # Update stock
                        product.stock += quantity
                        product.save()
                    else:
                        # Create new product
                        product = Product.objects.create(
                            product_name=name.title(),
                            size=size_obj,
                            length=length_obj,
                            stock=quantity
                        )

                    # Create purchase product
                    PurchaseProduct.objects.create(
                        purchase=purchase,
                        product=product,
                        size_variation=size_obj,
                        length_variation=length_obj,
                        quantity=quantity,
                        unit_price=unit_price,
                    )
                return redirect('purchase')
    else:
        form = PurchaseForm()
        formset = PurchaseProductFormSet(prefix="products")
        return render(
            request,
            "add_purchase.html",
            {"form": form, "formset": formset},
        )

def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier_obj = form.save(commit=False)
            checking_existing_supplier = Supplier.objects.filter(Q(supplier_name__iexact = supplier_obj.supplier_name) | Q(vat_no = supplier_obj.vat_no)).exists()
            if checking_existing_supplier:
                messages.error(request,'This supplier already exist.')
                return render(request,'add_supplier.html',{'form':form})
            else:
                supplier_obj.save()
                messages.success(request, "Saved Successfully!!")
                return redirect ('supplier_list')
    else:
        form = SupplierForm()
        return render(request,'add_supplier.html',{'form':form})
    
def supplier_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        suppliers = Supplier.objects.filter(supplier_name__icontains=query).order_by("supplier_name")
    else:
       suppliers = Supplier.objects.all().order_by("supplier_name")
    return render(request,'supplier_list.html',{'suppliers':suppliers})

def supplier_modify(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier_name = form.cleaned_data['supplier_name']
            vat_no = form.cleaned_data['vat_no']

            # Check for duplicates EXCLUDING the current supplier
            duplicate = Supplier.objects.filter(
                Q(supplier_name__iexact=supplier_name) |
                Q(vat_no=vat_no)
            ).exclude(id=supplier_id).exists()

            if duplicate:
                messages.error(request, 'Name or VAT Number matched with another supplier.')
                return render(request, 'add_supplier.html', {'form': form})
            else:
                form.save()
                messages.success(request, 'Modified Successfully!!')
                return redirect("supplier_list")
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'add_supplier.html', {'form': form})

def purchase_modify(request,purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase_products = PurchaseProduct.objects.filter(purchase=purchase)

    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseProductFormSet(request.POST, prefix="products")
        checking_existing_purchase = Purchase.objects.filter(supplier__supplier_name__iexact = purchase.supplier.supplier_name , invoice_no__iexact = purchase.invoice_no).exclude(id=purchase_id).exists()
        if form.is_valid() and formset.is_valid():
            if checking_existing_purchase:
                messages.error(request,'Name and Invoice No is matched with another Purchase.')
                return render(request,'add_purchase.html',{'form':form,'formset':formset,'data':request.POST})
             # Delete existing items and recreate them
            purchase_products.delete()
            form.save()
            for item in formset:
                data = item.cleaned_data
                if not data:
                    continue
                product_name = data['product']
                size = data['size'] if data['size'] not in ("", "----", "-") else None
                length = data['length'] if data['length'] not in ("", "----", "-") else None
                qty = data['qty']
                price = data['price']

                # Get or create size/length variations
                size_obj = Size_Variation.objects.get_or_create(size=size)[0] if size else None
                length_obj = Length_Variation.objects.get_or_create(length_in_inch=length)[0] if length else None
                print(product_name)

                # Get or create product
                try:
                        product = Product.objects.get(
                            product_name__iexact=product_name,
                            size=size_obj,
                            length=length_obj
                        )
                        product.stock += qty
                        product.save()
                except Product.DoesNotExist:
                    product = Product.objects.create(
                        product_name=product_name.title(),
                        size=size_obj,
                        length=length_obj,
                        stock=qty
                    )
                
                # Create purchase product
                PurchaseProduct.objects.create(
                    purchase=purchase,
                    product=product,
                    size_variation=size_obj,
                    length_variation=length_obj,
                    quantity=qty,
                    unit_price=price
                )

            messages.success(request, "Purchase modified successfully!")
            return redirect('purchase')

    else:
        form = PurchaseForm(instance=purchase)
        vat_no = purchase.supplier.vat_no
        phone = purchase.supplier.phone
        address = purchase.supplier.address
        data = {'vat_no':vat_no, 'phone':phone, 'address':address}
        # prepare initial data for formset
        initial_data = []
        for item in purchase_products:
            initial_data.append({
                'product': item.product.product_name,
                'size': item.size_variation.size if item.size_variation else '',
                'length': item.length_variation.length_in_inch if item.length_variation else '',
                'qty': item.quantity,
                'price': item.unit_price,
                'total': item.quantity * item.unit_price,
            })
        formset = PurchaseProductFormSet(prefix="products", initial=initial_data)

    return render(request, 'add_purchase.html', {"form": form, "formset": formset, 'data':data})
