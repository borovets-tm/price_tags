import os
from _csv import reader

from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from app_tags.forms import BarcodeForm, ProductsReceiptForm, ProductForm, UpdatePriceForm
from app_tags.models import Product
from price_tags.settings import BASE_DIR


BIG_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'big.txt')
BIG_SALE_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'big_sale.txt')
SMALL_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'small.txt')
SMALL_SALE_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'small_sale.txt')
FILE_LIST = [BIG_FILE, BIG_SALE_FILE, SMALL_FILE, SMALL_SALE_FILE]
SIZE_LIST = ['BIG', 'BIG_SALE', 'SMALL', 'SMALL_SALE']
UPDATE_ERRORS = []


class BarcodeScannerView(View):

	def get(self, request):
		UPDATE_ERRORS.clear()
		with open(BIG_FILE, 'w') as file:
			print('', file=file)
		with open(BIG_SALE_FILE, 'w') as file:
			print('', file=file)
		with open(SMALL_FILE, 'w') as file:
			print('', file=file)
		with open(SMALL_SALE_FILE, 'w') as file:
			print('', file=file)
		form = BarcodeForm()
		return render(
			request,
			'app_tags/barcode_scanner.html',
			context={
				'form': form,
			}
		)

	def post(self, request):
		form = BarcodeForm(request.POST)
		size = request.POST.get('size')
		data = ''
		if form.is_valid():
			data = form.cleaned_data.get('ean')
			FILE_TAGS = FILE_LIST[SIZE_LIST.index(size)]
			with open(FILE_TAGS, 'a', encoding='utf-8') as file:
				print(data, file=file)
		form = BarcodeForm()
		with open(BIG_FILE, 'r') as file:
			barcode_for_big_tags = len(file.readlines()) - 1
		with open(BIG_SALE_FILE, 'r') as file:
			barcode_for_big_sale_tags = len(file.readlines()) - 1
		with open(SMALL_FILE, 'r') as file:
			barcode_for_small_tags = len(file.readlines()) - 1
		with open(SMALL_SALE_FILE, 'r') as file:
			barcode_for_small_sale_tags = len(file.readlines()) - 1
		return render(
			request,
			'app_tags/barcode_scanner.html',
			context={
				'form': form,
				'barcode_for_big_tags': barcode_for_big_tags,
				'barcode_for_big_sale_tags': barcode_for_big_sale_tags,
				'barcode_for_small_tags': barcode_for_small_tags,
				'barcode_for_small_sale_tags': barcode_for_small_sale_tags,
				'last_enter': data,
				'size': size
			}
		)

def print_tags(request):
	max_height = 290
	max_weight = 180
	# 53280 4050 1035
	product_list = Product.objects.all()
	date = datetime.today().strftime('%d.%m.%Y')
	with open(BIG_FILE, 'r') as file:
		data = file.read().strip('\n ').split('\n')
		ean = [item for item in data if item.isdigit()]
		title = [item for item in data if not item.isdigit()]
		if data[0] == '':
			barcode_for_big_tags = []
		else:
			barcode_for_big_tags = list(map(int, ean)) + [
				product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
			]
	with open(BIG_SALE_FILE, 'r') as file:
		data = file.read().strip('\n ').split('\n')
		ean = [item for item in data if item.isdigit()]
		title = [item for item in data if not item.isdigit()]
		if data[0] == '':
			barcode_for_big_sale_tags = []
		else:
			barcode_for_big_sale_tags = list(map(int, ean)) + [
				product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
			]
	with open(SMALL_FILE, 'r') as file:
		data = file.read().strip('\n ').split('\n')
		ean = [item for item in data if item.isdigit()]
		title = [item for item in data if not item.isdigit()]
		if data[0] == '':
			barcode_for_small_tags = []
		else:
			barcode_for_small_tags = list(map(int, ean)) + [
				product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
			]
	with open(SMALL_SALE_FILE, 'r') as file:
		data = file.read().strip('\n ').split('\n')
		ean = [item for item in data if item.isdigit()]
		title = [item for item in data if not item.isdigit()]
		if data[0] == '':
			barcode_for_small_sale_tags = []
		else:
			barcode_for_small_sale_tags = list(map(int, ean)) + [
				product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
			]
	tags_list = []
	tags_list.extend([
		['big_tags', product_list.get(ean=ean)] for ean in barcode_for_big_tags if product_list.filter(ean=ean)
	])
	tags_list.extend([
		['big_sale_tags', product_list.get(ean=ean)] for ean in barcode_for_big_sale_tags if product_list.filter(
			ean=ean
		)
	])
	tags_list.extend([
		['small_tags', product_list.get(ean=ean)] for ean in barcode_for_small_tags if product_list.filter(ean=ean)
	])
	tags_list.extend([
		['small_sale_tags', product_list.get(ean=ean)] for ean in barcode_for_small_sale_tags if product_list.filter(
			ean=ean
		)
	])
	pages_tags = [[]]
	height = 0
	weight = 0
	for tags in tags_list:
		pages_tags[-1].append(tags)
		if tags[0] in ('big_tags', 'big_sale_tags'):
			weight += 90
			if weight == max_weight:
				height += 45
				weight = 0
			if height + 45 > max_height:
				pages_tags.append([])
				height = 0
		else:
			weight += 45
			if weight == max_weight:
				height += 33
				weight = 0
			if height + 33 > max_height:
				pages_tags.append([])
				height = 0
	return render(
		request,
		'app_tags/print_tags.html',
		context={
			'pages_tags': pages_tags,
			'date': date
		}
	)

class ProductsReceiptView(View):
	product_list_error = []

	def get(self, request):
		form = ProductsReceiptForm()
		self.product_list_error.clear()
		return render(
			request,
			'app_tags/products_receipt.html',
			context={
				'form': form
			}
		)

	def post(self, request):
		form = ProductsReceiptForm(request.POST, request.FILES)
		product_list = []
		numbers_product_in_file = 0
		if form.is_valid():
			file = form.cleaned_data['file'].read().strip()
			price_str = file.decode('utf-8').split('\n')
			csv_reader = reader(price_str, delimiter=';', quotechar='"')
			sku_index = 0
			price_index = 0
			old_price_index = 0
			is_red_price_index = 0
			for row in csv_reader:
				if row[0].endswith('sku'):
					price_index = row.index('price')
					old_price_index = row.index('old_price')
					is_red_price_index = row.index('is_red_price')
				else:
					numbers_product_in_file += 1
					try:
						item = Product.objects.get(sku=row[sku_index])
						item.price = row[price_index]
						item.old_price = row[old_price_index]
						item.is_red_price = True if row[is_red_price_index] == '1' else False
						item.save(update_fields=['price', 'old_price', 'is_red_price'])
						product_list.append(item)
					except ObjectDoesNotExist:
						self.product_list_error.append({'sku': row[sku_index], 'error': 'Товар отсутствует в списке'})
						UPDATE_ERRORS.append(
							{
								'sku': row[sku_index],
								'price': row[price_index],
								'old_price': row[old_price_index],
								'is_red_price': True if row[is_red_price_index] == '1' else False
							}
						)
			numbers_update_item = len(product_list)
			numbers_errors = len(self.product_list_error)
			return render(
				request,
				'app_tags/result_update.html',
				context={
					'product_list': product_list,
					'product_list_error': self.product_list_error,
					'numbers_update_item': numbers_update_item,
					'numbers_errors': numbers_errors,
					'numbers_product_in_file': numbers_product_in_file,
				}
			)
		form = ProductsReceiptForm()
		return render(
			request,
			'app_tags/products_receipt.html',
			context={
				'form': form
			}
		)


class ProductCreateBeforeUpdateView(View):

	def get(self, request):
		item = UPDATE_ERRORS[0]
		form = ProductForm(
			initial={
				'sku': item['sku'],
				'price': item['price'],
				'old_price': item['old_price'],
				'is_red_price': item['is_red_price']
			}
		)
		UPDATE_ERRORS.pop(0)
		return render(
			request,
			'app_tags/product_form.html',
			context={
				'form': form
			}
		)

	def post(self, request):
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			if UPDATE_ERRORS:
				item = UPDATE_ERRORS[0]
				form = ProductForm(
					initial={
						'sku': item['sku'],
						'price': item['price'],
						'old_price': item['old_price'],
						'is_red_price': item['is_red_price']
					}
				)
				UPDATE_ERRORS.pop(0)
				return render(
					request,
					'app_tags/product_form.html',
					context={
						'form': form
					}
				)
			else:
				return render(
					request,
					'app_tags/product_form.html',
					context={
						'close': 'yes'
					}
				)
		return render(
			request,
			'app_tags/product_form.html',
			context={
				'form': form
			}
		)


class AddNewProduct(View):

	def get(self, request):
		form = ProductForm()
		form_file = ProductsReceiptForm()
		return render(
			request,
			'app_tags/product_form.html',
			context={
				'form': form,
				'file': form_file
			}
		)

	def post(self, request):
		form = ProductForm(request.POST)
		form_file = ProductsReceiptForm()
		if form.is_valid():
			sku = form.cleaned_data.get('sku')
			product_check = Product.objects.filter(sku=sku)
			if product_check:
				return render(
					request,
					'app_tags/product_form.html',
					context={
						'form': form,
						'file': form_file,
						'error': product_check[0]
					}
				)
			added_product = form.save()
			form = ProductForm()
			return render(
				request,
				'app_tags/product_form.html',
				context={
					'form': form,
					'file': form_file,
					'product': added_product
				}
			)
		return render(
			request,
			'app_tags/product_form.html',
			context={
				'form': form,
				'file': form_file
			}
		)

	def multy_add_product(self, request):
		form = ProductsReceiptForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data['file'].read().strip()
			price_str = file.decode('utf-8').split('\n')
			csv_reader = reader(price_str, delimiter=';', quotechar='"')
			sku_index = 0
			ean_index = 0
			title_index = 0
			country_index = 0
			category_index = 0
			price_index = 0
			old_price_index = 0
			is_red_price_index = 0
			numbers_of_products = 0
			numbers_of_products_ok = 0
			for row in csv_reader:
				if row[0].endswith('sku'):
					ean_index = row.index('ean')
					title_index = row.index('title')
					country_index = row.index('country')
					category_index = row.index('category')
					price_index = row.index('price')
					old_price_index = row.index('old_price')
					is_red_price_index = row.index('is_red_price')
				else:
					numbers_of_products += 1
					if not Product.objects.filter(sku=row[sku_index]):
						numbers_of_products_ok += 1
						Product.objects.create(
							sku=row[sku_index],
							ean=row[ean_index],
							title=row[title_index],
							country=row[country_index],
							category=row[category_index],
							price=row[price_index],
							old_price=row[old_price_index],
							is_red_price=row[is_red_price_index],
							discount_type='Акция !!!'
						)
			form = ProductForm()
			form_file = ProductsReceiptForm()
			return render(
				request,
				'app_tags/product_form.html',
				context={
					'form': form,
					'file': form_file,
					'numbers_of_product': numbers_of_products,
					'numbers_of_products_ok': numbers_of_products_ok
				}
			)
		form = ProductForm()
		form_file = ProductsReceiptForm()
		return render(
			request,
			'app_tags/product_form.html',
			context={
				'form': form,
				'file': form_file
			}
		)


class ProductMultyUpdateView(View):
	update_product_list = []

	@classmethod
	def get(cls, request):
		cls.update_product_list.clear()
		form = UpdatePriceForm()
		return render(
			request,
			'app_tags/price_update.html',
			context={
				'form': form
			}
		)

	@classmethod
	def post(cls, request):
		form = UpdatePriceForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text'].split('\r\n')
			processed_text = []
			for i_text in text:
				i_text = i_text.split()
				for s in i_text:
					s = s.strip('- ')
					if s:
						if not s.isdigit():
							processed_text.append([s])
						else:
							processed_text[-1].append(s)
			product_list = Product.objects.only('title', 'price', 'old_price')
			for item in processed_text:
				update_product = product_list.filter(title__iexact=item[0])
				if len(item) == 2:
					update_product.update(**{'price': int(item[1])})
				else:
					update_product.update(**{'old_price': int(item[1]), 'price': int(item[2])})
				cls.update_product_list.extend([item.id for item in update_product])
			print(cls.update_product_list)
			product_list = Product.objects.filter(id__in=cls.update_product_list)
			return render(
				request,
				'app_tags/price_update.html',
				context={
					'product_list': product_list
				}
			)
		return render(
			request,
			'app_tags/price_update.html',
			context={
				'form': form
			}
		)

	@classmethod
	def edit_color_price_tags(cls, request, pk, color):
		product = Product.objects.get(id=pk)
		product.is_red_price = color
		product.save(update_fields=['is_red_price'])
		product_list = Product.objects.filter(id__in=cls.update_product_list)
		return render(
			request,
			'app_tags/price_update.html',
			context={
				'product_list': product_list
			}
		)


def instruction_products_receipt(request):
	return render(
		request,
		'app_tags/instruction_products_receipt.html'
	)
