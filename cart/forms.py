from django import forms

class AddToCartForm(forms.Form):
    """Форма для добавления товара в корзину"""
    quantity = forms.IntegerField(
        label="Количество",
        min_value=1,
        max_value=99,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        })
    )