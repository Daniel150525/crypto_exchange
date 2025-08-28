import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_wallets_dashboard_requires_login(client):
    url = reverse("wallets:dashboard")
    resp = client.get(url)
    assert resp.status_code in (302, 301)

@pytest.mark.django_db
def test_wallets_dashboard_ok_after_login(client, django_user_model):
    u = django_user_model.objects.create_user(username="u2", password="p")
    client.force_login(u)
    url = reverse("wallets:dashboard")
    resp = client.get(url)
    assert resp.status_code == 200