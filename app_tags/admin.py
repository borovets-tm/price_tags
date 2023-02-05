from django.contrib import admin
from app_tags.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'price', 'old_price', 'country', 'is_red_price']

	def is_red_price(self, obj):
		if obj.is_red_price:
			return 'Красный ценник'
		return 'Черный ценник'

	is_red_price.short_description = 'Цвет ценника'
