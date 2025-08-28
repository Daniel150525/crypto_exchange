from django.urls import path
from .views import CurrencyListView, CurrencyDetailView, TradeView, TradeHistoryView

app_name = "market"

urlpatterns = [
    path("currencies/", CurrencyListView.as_view(), name="currency_list"),
    path("currencies/<int:pk>/", CurrencyDetailView.as_view(), name="currency_detail"),
    path("trade/<int:wallet_id>/", TradeView.as_view(), name="make-trade"),
    path("trades/history/", TradeHistoryView.as_view(), name="trade-history"),
]