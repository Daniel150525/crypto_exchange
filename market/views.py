from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, ListView

from wallets.models import Wallet, Transaction
from .models import Currency, Trade
from .forms import TradeForm


class CurrencyListView(ListView):
    """Zobrazuje seznam všech dostupných měn v systému."""
    model = Currency
    template_name = "market/currency_list.html"
    context_object_name = "currencies"


class CurrencyDetailView(DetailView):
    """Zobrazuje detail vybrané měny a její informace."""
    model = Currency
    template_name = "market/currency_detail.html"
    context_object_name = "currency"


@method_decorator(login_required, name="dispatch")
class TradeView(FormView):
    """Umožňuje uživateli provést obchod (nákup nebo prodej) vybrané měny."""
    template_name = "market/trade.html"
    form_class = TradeForm
    success_url = reverse_lazy("wallets:dashboard")

    def form_valid(self, form):
        user = self.request.user
        trade_type = form.cleaned_data["trade_type"]  # "BUY" | "SELL"
        currency = form.cleaned_data["currency"]
        amount = form.cleaned_data["amount"]
        wallet, _ = Wallet.objects.get_or_create(owner=user, currency=currency)

        if trade_type == "BUY":
            wallet.balance = (wallet.balance or Decimal("0")) + amount
            tx_type = Transaction.DEPOSIT
            msg = f"Bought {amount} {currency.symbol}"
        else:
            if wallet.balance < amount:
                form.add_error("amount", "Insufficient funds.")
                return self.form_invalid(form)
            wallet.balance -= amount
            tx_type = Transaction.WITHDRAW
            msg = f"Sold {amount} {currency.symbol}"

        wallet.save()

        Trade.objects.create(
            wallet=wallet, currency=currency, amount=amount, trade_type=trade_type
        )
        Transaction.objects.create(wallet=wallet, tx_type=tx_type, amount=amount)

        messages.success(self.request, msg)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TradeHistoryView(ListView):
    """
    Zobrazuje historii obchodů přihlášeného uživatele (seřazeno od nejnovějších).
    """
    template_name = "market/trade_history.html"
    context_object_name = "trades"

    def get_queryset(self):
        return (
            Trade.objects
            .filter(wallet__owner=self.request.user)
            .select_related("currency", "wallet")
            .order_by("-created_at")
        )