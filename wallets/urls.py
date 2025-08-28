from django.urls import path
from .views import WalletDashboardView, DepositView, WithdrawView

app_name = "wallets"

urlpatterns = [
    path("", WalletDashboardView.as_view(), name="dashboard"),
    path("deposit/",   DepositView.as_view(),  name="deposit"),
    path("withdraw/",  WithdrawView.as_view(), name="withdraw"),
]