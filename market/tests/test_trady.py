from decimal import Decimal
import pytest
from django.urls import reverse
from market.models import Trade
from wallets.models import Wallet, Transaction

@pytest.mark.django_db
def test_trade_buy_creates_trade_and_increases_balance(client, user, currency_btc):
    client.force_login(user)
    url = reverse("market:make-trade", kwargs={"wallet_id": 1})
    resp = client.post(url, {"trade_type": "BUY", "currency": currency_btc.id, "amount": "10.5"})
    assert resp.status_code in (302, 303)
    wallet = Wallet.objects.get(owner=user, currency=currency_btc)
    assert wallet.balance == Decimal("10.5")
    assert Trade.objects.filter(wallet=wallet, currency=currency_btc, amount=Decimal("10.5"), trade_type="BUY").exists()
    assert Transaction.objects.filter(wallet=wallet, amount=Decimal("10.5"), tx_type=Transaction.DEPOSIT).exists()

@pytest.mark.django_db
def test_trade_sell_decreases_balance(client, user, currency_btc, wallet_btc):
    wallet_btc.balance = Decimal("7")
    wallet_btc.save()
    client.force_login(user)
    url = reverse("market:make-trade", kwargs={"wallet_id": wallet_btc.id})
    resp = client.post(url, {"trade_type": "SELL", "currency": currency_btc.id, "amount": "2"})
    assert resp.status_code in (302, 303)
    wallet_btc.refresh_from_db()
    assert wallet_btc.balance == Decimal("5")
    assert Trade.objects.filter(wallet=wallet_btc, trade_type="SELL", amount=Decimal("2")).exists()
    assert Transaction.objects.filter(wallet=wallet_btc, amount=Decimal("2"), tx_type=Transaction.WITHDRAW).exists()

@pytest.mark.django_db
def test_trade_sell_insufficient_funds_shows_error(client, user, currency_btc):
    client.force_login(user)
    url = reverse("market:make-trade", kwargs={"wallet_id": 1})
    resp = client.post(url, {"trade_type": "SELL", "currency": currency_btc.id, "amount": "1"})
    assert resp.status_code == 200
    assert b"Insufficient funds" in resp.content