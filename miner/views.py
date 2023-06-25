from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserProfile, Inventory, Pickaxe, Ore
import random
from django.template.loader import render_to_string

def index(request):
    user_profile = UserProfile.objects.first()
    current_pickaxe_id = user_profile.pickaxe.id

    next_pickaxe = Pickaxe.objects.filter(id=current_pickaxe_id + 1).first()

    context = {
        'next_pickaxe': next_pickaxe,
        'current_pickaxe_id': current_pickaxe_id,
        'inventory': Inventory.objects.filter(user_profile=user_profile),
        'money': user_profile.money,
    }
    return render(request, "miner/index.html", context)

def mine_ore(request):
    user_profile = UserProfile.objects.first()  # Assuming there is only one user profile
    pickaxe = user_profile.pickaxe

    # Determine the range of mineable ores based on pickaxe's ID
    min_pickaxe_id = pickaxe.id - 2
    max_pickaxe_id = pickaxe.id + 3

    # Get the mineable ores within the pickaxe's ID range
    ores = Ore.objects.filter(id__gte=min_pickaxe_id, id__lte=max_pickaxe_id)

    # Calculate total mining chance based on the pickaxe efficiency
    total_mining_chance = sum(ore.mining_chance for ore in ores)
    modified_mining_chance = total_mining_chance * pickaxe.mining_chance_modifier

    # Generate a random number between 0 and the modified mining chance
    random_number = random.uniform(0, modified_mining_chance)

    mined_ore = None
    for ore in ores:
        # Calculate the range for each ore based on its mining chance
        ore_range = ore.mining_chance * pickaxe.mining_chance_modifier

        # Check if the random number falls within the range of the current ore
        if random_number < ore_range:
            mined_ore = ore
            break

        # Subtract the current ore's range from the random number for the next iteration
        random_number -= ore_range

    if mined_ore:
        # Check if an inventory entry for the mined ore already exists
        inventory, _ = Inventory.objects.get_or_create(user_profile=user_profile, ore=mined_ore)

        # Update the amount of the existing inventory entry
        inventory.amount += pickaxe.efficiency
        inventory.save()

        # Remove duplicate inventory entries for the mined ore (if any)
        Inventory.objects.filter(user_profile=user_profile, ore=mined_ore).exclude(pk=inventory.pk).delete()

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def sell_ore(request):
    user_profile = UserProfile.objects.first()  # Assuming there is only one user profile
    inventory = Inventory.objects.filter(user_profile=user_profile)

    total_sell_price = 0
    for inventory_entry in inventory:
        ore = inventory_entry.ore
        sell_price = ore.sell_price
        amount = inventory_entry.amount
        total_sell_price += sell_price * amount
        inventory_entry.delete()

    user_profile.money += total_sell_price
    user_profile.save()

    return JsonResponse({"success": True, "totalSellPrice": total_sell_price})

def get_inventory(request):
    user_profile = UserProfile.objects.first()  # Assuming there is only one user profile
    inventory = Inventory.objects.filter(user_profile=user_profile)
    inventory_html = render_to_string("miner/inventory.html", {"inventory": inventory})
    return JsonResponse({"inventoryHTML": inventory_html})

def get_balance(request):
    user_profile = UserProfile.objects.first()  # Assuming there is only one user profile
    balance = user_profile.money
    return JsonResponse({"balance": balance})   

def buy_pickaxe(request, pickaxe_id):
    user_profile = UserProfile.objects.first()
    current_pickaxe_id = user_profile.pickaxe.id

    pickaxe_to_buy = Pickaxe.objects.filter(id=pickaxe_id).first()
    if pickaxe_to_buy:
        if pickaxe_id <= current_pickaxe_id:
            return JsonResponse({"success": False, "message": "You can only buy a pickaxe with a higher ID."})

        if user_profile.money >= pickaxe_to_buy.buy_price:
            user_profile.pickaxe = pickaxe_to_buy
            user_profile.money -= pickaxe_to_buy.buy_price
            user_profile.save()
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "message": "Insufficient funds."})

    return JsonResponse({"success": False, "message": "Invalid pickaxe ID."})