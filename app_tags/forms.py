from django import forms

from app_tags.models import Product, Category, Country


class BarcodeForm(forms.Form):
	ean = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-input',
				'placeholder': '4548736107281',
				'type': 'text'
			}
		)
	)


class ProductsReceiptForm(forms.Form):
	file = forms.FileField(
		widget=forms.FileInput(
			attrs={
				'class': 'form-input',
				'type': 'file',
				'style': 'min-width: 180px; width: 1000px; min-height: 58px; height: 58px; align-content: center; justify-content: center'
			}
		)
	)


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['sku', 'ean', 'title', 'country', 'category', 'old_price', 'price', 'is_red_price', 'discount_type']
		widgets = {
			'sku': forms.TextInput(
				attrs={
					'class': 'form-input'
				}
			),
			'ean': forms.TextInput(
				attrs={
					'class': 'form-input'
				}
			),
			'title': forms.TextInput(
				attrs={
					'class': 'form-input'
				}
			),
			'country': forms.Select(
				attrs={
					'class': 'form-select'
				}
			),
			'category': forms.Select(
				attrs={
					'class': 'form-select'
				}
			),
			'price': forms.TextInput(
				attrs={
					'class': 'form-input'
				}
			),
			'old_price': forms.TextInput(
				attrs={
					'class': 'form-input'
				}
			),
			'is_red_price': forms.CheckboxInput(),
			'discount_type': forms.Select(
				attrs={
					'class': 'form-select'
				}
			),
		}


class UpdatePriceForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textarea', 'style': 'font-size: 70%'}))


class AddPriceTagsByMarkdown(forms.Form):
	title = forms.CharField(
		label='Название товара',
		widget=forms.TextInput(
			attrs={
				'class': 'form-input',
				'placeholder': 'WF-1000XM4',
				'type': 'text',
				'style': 'min-width: 180px; width:180px; min-height: 30px; height: 30px;'
			}
		)
	)
	category = forms.ModelChoiceField(
		label='Категория',
		queryset=Category.objects.all(),
		widget=forms.Select(
			attrs={
				'class': 'form-select',
				'placeholder': 'BT наушники',
				'type': 'text',
				'style': 'min-width: 180px; width:180px; min-height: 30px; height: 30px'
			}
		)
	)
	country = forms.ModelChoiceField(
		label='Страна',
		queryset=Country.objects.all(),
		widget=forms.Select(
			attrs={
				'class': 'form-select',
				'placeholder': 'Малайзия',
				'type': 'text',
				'style': 'min-width: 180px; width:180px; min-height: 30px; height: 30px'
			}
		)
	)
	old_price = forms.CharField(
		label='Старая цена',
		widget=forms.TextInput(
			attrs={
				'class': 'form-input',
				'placeholder': '19990',
				'type': 'text',
				'style': 'min-width: 150px; width:150px; min-height: 30px; height: 30px'
			}
		)
	)
	price = forms.CharField(
		label='Цена',
		widget=forms.TextInput(
			attrs={
				'class': 'form-input',
				'placeholder': '15990',
				'type': 'text',
				'style': 'min-width: 150px; width:150px; min-height: 30px; height: 30px'
			}
		)
	)
	discount_type = forms.CharField(
		label='Причина скидки',
		widget=forms.TextInput(
			attrs={
				'class': 'form-input',
				'placeholder': 'Без упаковки',
				'type': 'text',
				'style': 'min-width: 180px; width:180px; min-height: 30px; height: 30px'
			}
		)
	)
	is_red_price = forms.BooleanField(
		label='Красный',
		widget=forms.CheckboxInput(
			attrs={
				'class': 'toggle',
				'type': 'checkbox',
				'style': 'min-width: 100px; width:100px; min-height: 30px; height: 30px',
			}
		),
		required=False
	)
	size_of_tags = forms.CharField(
		label='Размер ценника',
		widget=forms.Select(
			attrs={
				'class': 'form-input',
				'type': 'text',
				'style': 'min-width: 180px; width:180px; min-height: 30px; height: 30px'
			},
			choices=((0, 'Маленький'), (1, 'Большой'),)
		)
	)
