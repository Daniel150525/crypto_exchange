from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("market/", include("market.urls")),
    path("wallets/", include("wallets.urls")),
]