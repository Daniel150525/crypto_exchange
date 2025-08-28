from django.contrib import admin
from .models import Currency, Trade

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "symbol")
    search_fields = ("name", "symbol")

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "currency", "amount", "trade_type", "created_at")
    list_filter = ("trade_type", "currency")
    search_fields = ("wallet__id", "currency__symbol")