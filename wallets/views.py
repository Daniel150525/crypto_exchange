# wallets/views.py
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from .models import Wallet, Transaction
from .forms import DepositForm, WithdrawForm


@method_decorator(login_required, name="dispatch")
class WalletDashboardView(TemplateView):
    """Zobrazuje přehled peněženek uživatele a jeho oblíbených měn."""
    template_name = "wallets/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["wallets"] = (
            Wallet.objects
            .filter(owner=self.request.user)
            .select_related("currency")
        )
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["wallets"] = Wallet.objects.filter(owner=self.request.user).select_related("currency")
        if hasattr(self.request.user, "profile"):
            ctx["favorite_currencies"] = self.request.user.profile.favorite_currencies.all()
        return ctx


@method_decorator(login_required, name="dispatch")
class DepositView(FormView):
    """Zpracuje formulář pro vložení peněz do vybrané peněženky."""
    template_name = "wallets/deposit.html"
    form_class = DepositForm
    success_url = reverse_lazy("wallets:dashboard")

    def form_valid(self, form):
        user = self.request.user
        currency = form.cleaned_data["currency"]
        amount: Decimal = form.cleaned_data["amount"]

        wallet, _ = Wallet.objects.get_or_create(
            owner=user,
            currency=currency
        )
        wallet.balance = (wallet.balance or Decimal("0")) + amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            tx_type=Transaction.DEPOSIT,
            amount=amount,
        )
        messages.success(self.request, f"Deposited {amount} {currency.symbol}.")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class WithdrawView(FormView):
    """Zpracuje formulář pro výběr peněz z vybrané peněženky."""
    template_name = "wallets/withdraw.html"
    form_class = WithdrawForm
    success_url = reverse_lazy("wallets:dashboard")

    def form_valid(self, form):
        user = self.request.user
        currency = form.cleaned_data["currency"]
        amount: Decimal = form.cleaned_data["amount"]

        wallet, _ = Wallet.objects.get_or_create(
            owner=user,
            currency=currency
        )

        if wallet.balance < amount:
            form.add_error("amount", "Insufficient funds.")
            return self.form_invalid(form)

        wallet.balance -= amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            tx_type=Transaction.WITHDRAW,
            amount=amount,
        )
        messages.success(self.request, f"Withdrew {amount} {currency.symbol}.")
        return super().form_valid(form)