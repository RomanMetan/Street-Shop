from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile


class RegistrationForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""

    # Поля для User (встроенная модель)
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте логин'
        })
    )
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )

    # Поля для пароля
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = UserProfile
        # 👇 ТОЛЬКО ПОЛЯ, КОТОРЫЕ ЕСТЬ В UserProfile
        fields = ['age', 'gender', 'delivery_address']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш возраст'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите адрес доставки'
            })
        }
        labels = {
            'age': 'Возраст',
            'gender': 'Пол',
            'delivery_address': 'Адрес доставки'
        }

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован')
        return email

    def clean_username(self):
        """Проверка уникальности username"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        # Создаём пользователя User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Создаём профиль UserProfile
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user