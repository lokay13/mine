from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.Inventory)
admin.site.register(models.Pickaxe)
admin.site.register(models.Ore)