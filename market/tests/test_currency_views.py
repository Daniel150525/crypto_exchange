import pytest
from django.urls import reverse
from market.models import Currency


@pytest.mark.django_db
def test_currency_list_view_status_and_contents(client):
    Currency.objects.create(name="Bitcoin", symbol="BTC")
    Currency.objects.create(name="Ethereum", symbol="ETH")

    url = reverse("market:currency_list")
    resp = client.get(url)

    assert resp.status_code == 200
    content = resp.content.decode()
    assert "Bitcoin" in content and "BTC" in content
    assert "Ethereum" in content and "ETH" in content


@pytest.mark.django_db
def test_currency_list_view_empty_state(client):
    url = reverse("market:currency_list")
    resp = client.get(url)

    assert resp.status_code == 200
    assert "No currencies yet" in resp.content.decode() or "Currencies" in resp.content.decode()


@pytest.mark.django_db
def test_currency_detail_view_status_and_object(client):
    c = Currency.objects.create(name="Bitcoin", symbol="BTC")

    url = reverse("market:currency_detail", args=[c.id])
    resp = client.get(url)

    assert resp.status_code == 200
    content = resp.content.decode()
    assert "Bitcoin" in content and "BTC" in content


@pytest.mark.django_db
def test_currency_detail_view_404_for_missing(client):
    url = reverse("market:currency_detail", args=[999999])
    resp = client.get(url)
    assert resp.status_code == 404