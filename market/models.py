from django.db import models


class Currency(models.Model):
    """Model měny, kterou lze obchodovat (např. Bitcoin nebo Ethereum)."""
    name = models.CharField(max_length=50, unique=True)      # např. Bitcoin
    symbol = models.CharField(max_length=10, unique=True)    # např. BTC

    def __str__(self):
        return self.symbol


class Trade(models.Model):
    """Model obchodu – záznam o nákupu nebo prodeji měny v rámci peněženky."""
    BUY = "BUY"
    SELL = "SELL"
    TRADE_TYPES = [(BUY, "Buy"), (SELL, "Sell")]

    wallet = models.ForeignKey(
        "wallets.Wallet", on_delete=models.CASCADE, related_name="trades"
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="trades"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.amount} {self.currency.symbol}"