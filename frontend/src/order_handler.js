document.addEventListener('DOMContentLoaded', () => {
    const addToCartButton = document.getElementById('add-to-cart');
    const clearCartButton = document.getElementById('clear-cart');
    const cartItemsList = document.getElementById('cart-items');
    const totalCostSpan = document.getElementById('total-cost');
    const productSelect = document.getElementById('product-select');

    const prices = {
        'small-treats': 6.42,
        'large-treats': 8.06
    };

    let cart = [];

    function updateCart() {
        // Clear the current items list
        cartItemsList.innerHTML = '';

        // Update list with cart items
        cart.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.name}`;
            cartItemsList.appendChild(li);
        });

        // Calculate total cost
        const totalCost = cart.reduce((total, item) => total + item.price, 0);
        totalCostSpan.textContent = totalCost.toFixed(2);
    }

    addToCartButton.addEventListener('click', () => {
        const selectedValue = productSelect.value;
        const selectedOption = productSelect.options[productSelect.selectedIndex];

        if (selectedValue) {
            cart.push({
                name: selectedOption.text,
                price: prices[selectedValue]
            });

            updateCart();
        } else {
            alert('Please select a product to add to your cart.');
        }
    });

    clearCartButton.addEventListener('click', () => {
        cart = []; // Clear the cart array
        updateCart(); // Update the cart display
    });
});
