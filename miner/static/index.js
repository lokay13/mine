document.addEventListener("DOMContentLoaded", () => {
    updateInventory();
    updateBalance();

    const mineOreButton = document.getElementById("mine-ore");
    const sellOreButton = document.getElementById("sell-ore");

    mineOreButton.addEventListener("click", mineOre);
    sellOreButton.addEventListener("click", sellOre);
});
 
function mineOre() {
    fetch("/mine_ore", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                updateInventory(); // Update the inventory section
                updateBalance(); // Update the balance
            } else {
                alert("Failed to mine ore.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function sellOre() {
    fetch("/sell_ore", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                updateInventory(); // Update the inventory section
                updateBalance(); // Update the balance
            } else {
                alert("Failed to sell ore.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function updateInventory() {
    fetch("/get_inventory")
        .then((response) => response.json())
        .then((data) => {
            // Update the inventory section with the new inventory data
            const inventorySection = document.getElementById("inventory-section");
            inventorySection.innerHTML = data.inventoryHTML;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function updateBalance() {
    fetch("/get_balance")
        .then((response) => response.json())
        .then((data) => {
            // Update the balance with the new balance value
            const balanceElement = document.getElementById("balance");
            balanceElement.innerText = `Balance: ${data.balance} coins`;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

// Add the following function to handle buying a pickaxe
function buyPickaxe(pickaxeId, buyPrice, currentPickaxeId) {
    if (currentPickaxeId === 15) {
        alert("You already have the maximum level pickaxe.");
        return;
    }

    if (pickaxeId <= currentPickaxeId) {
        alert("You can only buy a pickaxe with a higher ID.");
        return;
    }

    if (confirm(`Buy this pickaxe for ${buyPrice} coins?`)) {
        fetch(`/buy_pickaxe/${pickaxeId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("Pickaxe bought successfully!");
                    location.reload(); // Refresh the page to show the new pickaxe for purchase
                } else {
                    alert(data.message || "Failed to buy pickaxe.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }
}

// Function to get the value of a cookie by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}
