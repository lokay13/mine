from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mine_ore", views.mine_ore, name="mine_ore"),
    path("sell_ore", views.sell_ore, name="sell_ore"),
    path("get_inventory", views.get_inventory, name="get_inventory"),
    path("get_balance", views.get_balance, name="get_balance"),
    path("buy_pickaxe/<int:pickaxe_id>", views.buy_pickaxe, name="buy_pickaxe"),  # Add this URL pattern
]