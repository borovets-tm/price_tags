from django.urls import path

from app_tags.views import BarcodeScannerView, print_tags, ProductsReceiptView, ProductCreateBeforeUpdateView
from app_tags.views import AddNewProduct, ProductMultyUpdateView, instruction_products_receipt
from app_tags.views import instruction_add_products

urlpatterns = [
	path('', BarcodeScannerView.as_view(), name='barcode_scanner'),
	path('print_list/', print_tags, name='print_tags'),
	path('products_receipt/', ProductsReceiptView.as_view(), name='products_receipt'),
	path('add_product/', ProductCreateBeforeUpdateView.as_view(), name='create_product_before_update'),
	path('new_product/', AddNewProduct.as_view(), name='create_product'),
	path('update_price/', ProductMultyUpdateView.as_view(), name='update_price'),
	path('update_price/<int:pk>=<int:color>/', ProductMultyUpdateView.edit_color_price_tags, name='change_color'),
	path('instruction_products_receipt/', instruction_products_receipt, name='instruction_products_receipt'),
	path('instruction_add_products/', instruction_add_products, name='instruction_add_products'),
]
