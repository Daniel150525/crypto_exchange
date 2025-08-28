from django import forms
from .models import Trade
from .models import Currency

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ["currency", "amount", "trade_type"]

class TradeForm(forms.Form):
    TRADE_TYPES = (("BUY", "Buy"), ("SELL", "Sell"))
    trade_type = forms.ChoiceField(choices=TRADE_TYPES)
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    amount = forms.DecimalField(min_value=0.00000001, max_digits=18, decimal_places=8)