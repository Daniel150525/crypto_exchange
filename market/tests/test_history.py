from decimal import Decimal
import pytest
from django.urls import reverse
from market.models import Trade
from wallets.models import Wallet

@pytest.mark.django_db
def test_trade_history_lists_user_trades(client, user, currency_btc, wallet_btc):
    Trade.objects.create(wallet=wallet_btc, currency=currency_btc, amount=Decimal("1"), trade_type="BUY")
    Trade.objects.create(wallet=wallet_btc, currency=currency_btc, amount=Decimal("2"), trade_type="SELL")
    client.force_login(user)
    url = reverse("market:trade-history")
    resp = client.get(url)
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "BUY 1" in content or "BUY" in content
    assert "SELL 2" in content or "SELL" in content