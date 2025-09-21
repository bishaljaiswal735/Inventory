from django.urls import path
from . import views

urlpatterns = [
    path("", views.purchase, name="purchase"),
    path(
        "purchase_detail/<int:purchase_id>/",
        views.purchase_detail,
        name="purchase_detail",
    ),
     path(
        "purchase_modify/<int:purchase_id>/",
        views.purchase_modify,
        name="purchase_modify",
    ),
    path("add_purchase/", views.add_purchase, name="add_purchase"),
    path('add_supplier',views.add_supplier, name='add_supplier'),
    path('supplier_list',views.supplier_list, name='supplier_list'),
    path('supplier_modify/<int:supplier_id>/',views.supplier_modify, name='supplier_modify'),
    path("supplier_info/<int:supplier_id>/", views.supplier_info, name="supplier_info"),
    path("get_products/", views.get_products, name="get_product"),
    path('get_sizes/', views.get_sizes, name='get_sizes'),
    path('get_lengths/', views.get_lengths, name='get_lengths'),
]
