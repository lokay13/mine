from django.db import models

class UserProfile(models.Model):
    money = models.IntegerField(default=100)
    pickaxe = models.ForeignKey('Pickaxe', on_delete=models.SET_NULL, null=True, default=1)

class Inventory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ore = models.ForeignKey('Ore', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

class Pickaxe(models.Model):
    name = models.CharField(max_length=100)
    buy_price = models.IntegerField(default=0)
    efficiency = models.IntegerField(default=0)
    mining_chance_modifier = models.FloatField(default=0)

class Ore(models.Model):
    name = models.CharField(max_length=100)
    sell_price = models.IntegerField(default=0)
    mining_chance = models.FloatField(default=0)