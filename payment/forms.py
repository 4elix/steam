from django import forms

from .models import ShippingAddress, Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-custom',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-custom',
                'placeholder': 'Фамилия'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control form-custom',
                'placeholder': 'Ваш адрес'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select form-custom',
                'placeholder': 'Ваш город'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control form-custom',
                'placeholder': 'Ваш регион'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-custom',
                'placeholder': 'Ваш телефон'
            })
        }




