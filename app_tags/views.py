import os
from _csv import reader
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from app_tags.forms import BarcodeForm, ProductsReceiptForm, ProductForm, UpdatePriceForm, AddPriceTagsByMarkdown
from app_tags.models import Product
from price_tags.settings import BASE_DIR

BIG_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'big.txt')
BIG_SALE_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'big_sale.txt')
SMALL_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'small.txt')
SMALL_SALE_FILE = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'small_sale.txt')
FREE_TAGS_SMALL = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'free_tags_small.txt')
FREE_TAGS_BIG = os.path.join(BASE_DIR, 'static', 'price_tag_list', 'free_tags_big.txt')
FILE_LIST = [BIG_FILE, BIG_SALE_FILE, FREE_TAGS_BIG, SMALL_FILE, SMALL_SALE_FILE, FREE_TAGS_SMALL]
SIZE_LIST = ['BIG', 'BIG_SALE', 'FREE_BIG', 'SMALL', 'SMALL_SALE', 'FREE_SMALL']
UPDATE_ERRORS = []


class BarcodeScannerView(View):

	@classmethod
	def get(cls, request):
		UPDATE_ERRORS.clear()
		for file_tags in FILE_LIST:
			with open(file_tags, 'w') as file:
				print(file=file)
		form = BarcodeForm()
		free_form = AddPriceTagsByMarkdown()
		return render(
			request,
			'app_tags/barcode_scanner.html',
			context={
				'form': form,
				'free_form': free_form
			}
		)

	@classmethod
	def post(cls, request):
		barcode_for_big_tags = 0
		barcode_for_big_sale_tags = 0
		barcode_for_small_tags = 0
		barcode_for_small_sale_tags = 0
		numbers_free_tags = 0
		numbers_list = [
			'barcode_for_big_tags',
			'barcode_for_big_sale_tags',
			'numbers_free_tags',
			'barcode_for_small_tags',
			'barcode_for_small_sale_tags',
			'numbers_free_tags'
		]
		form = BarcodeForm(request.POST)
		free_form = AddPriceTagsByMarkdown(request.POST)
		size = request.POST.get('size')
		data = ''
		if form.is_valid():
			data = form.cleaned_data.get('ean')
			FILE_TAGS = FILE_LIST[SIZE_LIST.index(size)]
			with open(FILE_TAGS, 'a', encoding='utf-8') as file:
				print(data, file=file)
		elif free_form.is_valid():
			free_data = free_form.cleaned_data
			file = FREE_TAGS_SMALL if free_data.get('size_of_tags') == '0' else FREE_TAGS_BIG
			with open(file, 'a', encoding='utf-8') as file:
				title = free_data.get('title')
				category = free_data.get('category').title
				country = free_data.get('country').title
				old_price = free_data.get('old_price')
				price = free_data.get('price')
				discount_type = free_data.get('discount_type')
				is_red_price = '1' if free_data.get('is_red_price') else '0'
				free_data = ','.join([title, category, country, old_price, price, discount_type, is_red_price])
				print(free_data, file=file)
		form = BarcodeForm()
		free_form = AddPriceTagsByMarkdown()
		context = {
			'form': form,
			'free_form': free_form,
			'barcode_for_big_tags': barcode_for_big_tags,
			'barcode_for_big_sale_tags': barcode_for_big_sale_tags,
			'barcode_for_small_tags': barcode_for_small_tags,
			'barcode_for_small_sale_tags': barcode_for_small_sale_tags,
			'last_enter': data,
			'size': size,
			'numbers_free_tags': numbers_free_tags
		}
		for file_tags in FILE_LIST:
			with open(file_tags, 'r') as file:
				context[numbers_list[FILE_LIST.index(file_tags)]] += len(file.readlines()) - 1
		return render(
			request,
			'app_tags/barcode_scanner.html',
			context=context
		)


def print_tags(request):
	max_height = 290
	max_weight = 180
	product_list = Product.objects.all()
	date = datetime.today().strftime('%d.%m.%Y')
	tags_list = []
	order_list = ['big_tags', 'big_sale_tags', 'free_tags_big', 'small_tags', 'small_sale_tags', 'free_tags_small']
	for file_tags in FILE_LIST:
		with open(file_tags, 'r', encoding='utf-8') as file:
			data = file.read().strip('\n ').split('\n')
			if file_tags not in [FREE_TAGS_BIG, FREE_TAGS_SMALL]:
				ean = [item for item in data if item.isdigit()]
				title = [item for item in data if not item.isdigit()]
				if data[0] != '':
					barcode = list(map(int, ean)) + [
						product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
					]
					tags_list.extend(
						[
							[order_list[FILE_LIST.index(file_tags)], product_list.get(ean=ean)] for ean in barcode if
							product_list.filter(ean=ean)
						]
					)
			else:
				if data[0] != '':
					for line in data:
						tag = dict()
						line = line.split(',')
						tag['title'] = line[0]
						tag['category'] = line[1]
						tag['country'] = line[2]
						tag['old_price'] = int(line[3])
						tag['price'] = int(line[4])
						tag['discount_type'] = line[5]
						tag['is_red_price'] = bool(line[6])
						tags_list.append([order_list[FILE_LIST.index(file_tags)], tag])

	# with open(BIG_FILE, 'r') as file:
	# 	data = file.read().strip('\n ').split('\n')
	# 	ean = [item for item in data if item.isdigit()]
	# 	title = [item for item in data if not item.isdigit()]
	# 	if data[0] == '':
	# 		barcode_for_big_tags = []
	# 	else:
	# 		barcode_for_big_tags = list(map(int, ean)) + [
	# 			product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
	# 		]
	# with open(BIG_SALE_FILE, 'r') as file:
	# 	data = file.read().strip('\n ').split('\n')
	# 	ean = [item for item in data if item.isdigit()]
	# 	title = [item for item in data if not item.isdigit()]
	# 	if data[0] == '':
	# 		barcode_for_big_sale_tags = []
	# 	else:
	# 		barcode_for_big_sale_tags = list(map(int, ean)) + [
	# 			product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
	# 		]
	# with open(SMALL_FILE, 'r') as file:
	# 	data = file.read().strip('\n ').split('\n')
	# 	ean = [item for item in data if item.isdigit()]
	# 	title = [item for item in data if not item.isdigit()]
	# 	if data[0] == '':
	# 		barcode_for_small_tags = []
	# 	else:
	# 		barcode_for_small_tags = list(map(int, ean)) + [
	# 			product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
	# 		]
	# with open(SMALL_SALE_FILE, 'r') as file:
	# 	data = file.read().strip('\n ').split('\n')
	# 	ean = [item for item in data if item.isdigit()]
	# 	title = [item for item in data if not item.isdigit()]
	# 	if data[0] == '':
	# 		barcode_for_small_sale_tags = []
	# 	else:
	# 		barcode_for_small_sale_tags = list(map(int, ean)) + [
	# 			product.ean for product in [product_list.filter(title__iexact=item).first() for item in title]
	# 		]
	# tags_list.extend([
	# 	['big_tags', product_list.get(ean=ean)] for ean in barcode_for_big_tags if product_list.filter(ean=ean)
	# ])
	# tags_list.extend([
	# 	['big_sale_tags', product_list.get(ean=ean)] for ean in barcode_for_big_sale_tags if product_list.filter(
	# 		ean=ean
	# 	)
	# ])
	# tags_list.extend([
	# 	['small_tags', product_list.get(ean=ean)] for ean in barcode_for_small_tags if product_list.filter(ean=ean)
	# ])
	# tags_list.extend([
	# 	['small_sale_tags', product_list.get(ean=ean)] for ean in barcode_for_small_sale_tags if product_list.filter(
	# 		ean=ean
	# 	)
	# ])
	pages_tags = [[]]
	height = 0
	weight = 0
	for tags in tags_list:
		pages_tags[-1].append(tags)
		if tags[0] in ('big_tags', 'big_sale_tags', 'free_tags_big'):
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

	@classmethod
	def get(cls, request):
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

	@classmethod
	def post(cls, request):
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

	@classmethod
	def get(cls, request):
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

	@classmethod
	def post(cls, request):
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

	@classmethod
	def multy_add_product(cls, request):
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
