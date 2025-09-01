from django.urls import path
from . import views

urlpatterns = [
    path("", views.purchase, name="purchase"),
    path(
        "purchase_detail/<int:purchase_id>/",
        views.purchase_detail,
        name="purchase_detail",
    ),
    path("add_purchase/", views.add_purchase, name="add_purchase"),
    path("supplier_info/<int:supplier_id>/", views.supplier_info, name="supplier_info"),
    path("get_products/", views.get_products, name="get_product"),
    path('get_sizes/<int:product_id>/', views.get_sizes, name='get_sizes'),
    path('get_lengths/<int:size_id>/', views.get_lengths, name='get_lengths'),
]
