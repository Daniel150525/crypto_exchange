import pytest
from django.contrib.auth.models import User
from market.models import Currency
from wallets.models import Wallet

@pytest.fixture
def user(db):
    u = User.objects.create_user(username="u1", password="pass12345")
    return u

@pytest.fixture
def currency_btc(db):
    return Currency.objects.create(name="Bitcoin", symbol="BTC")

@pytest.fixture
def wallet_btc(db, user, currency_btc):
    return Wallet.objects.create(owner=user, currency=currency_btc, balance=0)