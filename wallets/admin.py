from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "currency", "balance", "created_at")
    list_filter = ("currency",)
    search_fields = ("owner__username",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "tx_type", "amount", "created_at")
    list_filter = ("tx_type", "wallet__currency")
    search_fields = ("wallet__owner__username",)