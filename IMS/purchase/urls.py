from django.urls import path
from . import views

urlpatterns = [
    path('',views.purchase,name='purchase'),
    path('purchase_detail/<int:purchase_id>/',views.purchase_detail,name='purchase_detail'),
    path('add_purchase/', views.add_purchase, name="add_purchase"),
    path('supplier_info/<int:supplier_id>/',views.supplier_info,name='supplier_info'),

]
