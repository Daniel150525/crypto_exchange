from django import forms
from market.models import Currency
from .models import Transaction

class DepositForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=0.00000001)

class WithdrawForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    amount = forms.DecimalField(max_digits=18, decimal_places=8, min_value=0.00000001)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["tx_type", "amount"]