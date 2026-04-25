from django import forms


class CheckoutForm(forms.Form):
    """Форма оформления заказа"""

    delivery_address = forms.CharField(
        label="Адрес доставки",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Город, улица, дом, квартира'
        })
    )

    payment_method = forms.ChoiceField(
        label="Способ оплаты",
        choices=[
            ('card', '💳 Банковская карта'),
            ('cash', '💰 Наличные при получении'),
            ('online', '🏦 Онлайн-банк'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class FakePaymentForm(forms.Form):
    """Форма фейк-оплаты (упрощённая, работает всегда)"""

    card_number = forms.CharField(
        label="Номер карты",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '4242 4242 4242 4242'
        }),
        required=True
    )

    card_holder = forms.CharField(
        label="Владелец карты",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'IVAN IVANOV'
        }),
        required=True
    )

    expiry_date = forms.CharField(
        label="Срок действия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12/28'
        }),
        required=True
    )

    cvv = forms.CharField(
        label="CVV",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '123'
        }),
        required=True,
        max_length=10  # просто ограничение длины, без проверки на цифры
    )