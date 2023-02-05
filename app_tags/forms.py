from django import forms

from app_tags.models import Product


class BarcodeForm(forms.Form):
	ean = forms.CharField(widget=forms.TextInput(attrs={
			'class': 'form-input',
			'placeholder': '4548736107281',
			'type': 'text'
		}))


class ProductsReceiptForm(forms.Form):
	file = forms.FileField(widget=forms.FileInput(attrs={
		'class': 'form-input',
		'type': 'file'
	}))


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
