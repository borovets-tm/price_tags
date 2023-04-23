from django.db import models


COUNTRY = (
			('Вьетнам', 'Вьетнам'),
			('Китай', 'Китай'),
			('Малайзия', 'Малайзия'),
			('Мьянма', 'Мьянма'),
			('Словакия', 'Словакия'),
			('Тайвань', 'Тайвань'),
			('Таиланд', 'Таиланд'),
			('Филиппины', 'Филиппины'),
			('Япония', 'Япония')
		)

class Category(models.Model):
	title = models.CharField(
		max_length=30,
		verbose_name='категория товара',
		help_text='наушники'
	)

	class Meta:
		db_table = 'category'
		verbose_name = 'категория товара'
		verbose_name_plural = 'категории товаров'

	def __str__(self):
		return self.title

class Country(models.Model):
	title = models.CharField(
		max_length=30,
		verbose_name='страна',
		help_text='Китай'
	)

	class Meta:
		db_table = 'country'
		verbose_name = 'страна производства'
		verbose_name_plural = 'страны производства'

	def __str__(self):
		return self.title

class Product(models.Model):
	sku = models.CharField(
		max_length=15,
		null=True,
		blank=True,
		unique=True,
		verbose_name='номенклатура(sku/sap)',
		help_text='IERM7.WW2'
	)
	ean = models.IntegerField(
		unique=True,
		verbose_name='EAN/Штрихкод',
		help_text='4548736081680'
	)
	title = models.CharField(
		max_length=200,
		verbose_name='наименование товара',
		help_text='IER-M7'
	)
	country = models.ForeignKey(
		Country,
		on_delete=models.CASCADE,
		verbose_name='страна производства',
		help_text='Китай'
	)
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		verbose_name='категория товара',
		help_text='наушники'
	)
	old_price = models.IntegerField(
		verbose_name='старая цена',
		null=True,
		blank=True
	)
	price = models.IntegerField(
		verbose_name='цена товара'
	)
	is_red_price = models.BooleanField(
		verbose_name='Красный ценник',
	)
	discount_type = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		verbose_name='причина скидки',
		choices=(
			('Акция !!!', 'Акция !!!'),
			('Уценка', 'Уценка'),
			('Витринный образец', 'Витринный образец'),
			('Последний экземпляр', 'Последний экземпляр'),
		),
		default='Акция !!!'
	)

	class Meta:
		db_table = 'price'
		ordering = ['ean']
		verbose_name = 'товар'
		verbose_name_plural = 'товары'

	def __str__(self):
		return self.title
