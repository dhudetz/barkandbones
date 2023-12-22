document.addEventListener('DOMContentLoaded', () => {
    const addToCartButton = document.getElementById('add-to-cart');
    const clearCartButton = document.getElementById('clear-cart');
    const cartItemsList = document.getElementById('cart-items');
    const subcartItemsList = document.getElementById('subcart-items');
    const totalCostSpan = document.getElementById('total-cost');
    const subtotalCostSpan = document.getElementById('subtotal-cost');
    const productSelect = document.getElementById('product-select');
    const orderType = document.getElementById('order-type');

    const productPrices = {
        'small-treats': 5.00,
        'large-treats': 5.00,
        'delivery': 5.00
    };

    let cart = [];
    let submitting = false;

    function updateCart() {
        // Clear the current items lists
        cartItemsList.innerHTML = '';
        subcartItemsList.innerHTML = '';
        let subtotal = 0;
    
        // Group items by id and sum their quantities and prices
        const groupedItems = cart.reduce((acc, item) => {
            if (!acc[item.id]) {
                acc[item.id] = {
                    id: item.id,
                    name: item.name,
                    price: item.price,
                    quantity: 0,
                    totalPrice: 0
                };
            }
            acc[item.id].quantity++;
            acc[item.id].totalPrice += item.price;
            return acc;
        }, {});
    
        // Update list with grouped cart items and subcart items
        Object.entries(groupedItems).forEach(([id, item]) => {
            const li = document.createElement('li');
            li.textContent = `${item.quantity}x ${item.name} - $${item.totalPrice.toFixed(2)}`;
            cartItemsList.appendChild(li);
    
            // If the item is not a delivery fee, add it to the subcart
            if (id !== 'delivery') {
                const subLi = li.cloneNode(true);
                subcartItemsList.appendChild(subLi);
            }
        });
    
        // Calculate subtotal (excluding delivery fee)
        subtotal = Object.values(groupedItems).reduce((total, item) => {
            return item.id !== 'delivery' ? total + item.totalPrice : total;
        }, 0);
    
        // Update subtotal and total costs
        subtotalCostSpan.textContent = subtotal.toFixed(2);
        const totalCost = subtotal + (groupedItems['delivery'] ? groupedItems['delivery'].totalPrice : 0);
        totalCostSpan.textContent = totalCost.toFixed(2);
    }

    // Add event listeners for each item card.
    document.querySelectorAll('.product-item').forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('product-item-scale');
            setTimeout(() => {
                item.classList.remove('product-item-scale');
            }, 110); // This duration should match the CSS transition duration

            const selectedValue = item.getAttribute('data-value');
            const selectedLabel = item.querySelector('label').textContent;
    
            if (selectedValue) {
                cart.push({
                    id: selectedValue,
                    name: selectedLabel.split(' - ')[0], // Just get the name without price
                    price: productPrices[selectedValue]
                });
    
                updateCart();
            } else {
                alert('Please select a product to add to your cart.');
            }
        });
    });

    // Additional variables for new form fields
    const orderForm = document.getElementById('order-form');
    const customerNameInput = document.getElementById('customer-name');
    const customerPhoneInput = document.getElementById('customer-phone');
    const customerEmailInput = document.getElementById('customer-email');
    const orderNotesTextarea = document.getElementById('order-notes');
    const customerAddressInput = document.getElementById('customer-address');
    const customerAddressLabel = document.getElementById('customer-address-label');
    
    // Function to submit the order
    function submitOrder() {
        const orderType = document.getElementById('order-type').value;
        const customerName = customerNameInput.value.trim();
        const customerPhone = customerPhoneInput.value.trim();
        const customerEmail = customerEmailInput.value.trim();
        const customerAddress = customerAddressInput.value.trim();
        const orderNotes = orderNotesTextarea.value.trim();
        
        // Construct the order data
        const orderData = {
            orderType: orderType,
            customerName: customerName,
            phoneNumber: customerPhone,
            email: customerEmail,
            address: customerAddress,
            specialInstructions: orderNotes,
            orderItems: cart
        };
        
        // Set flag to prevent overlapping submit calls
        submitting = true;

        // Send the order data to the server
        fetch(`${config.API_BASE_URL}/api/order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            window.setActivePage("thank-you");
            rainBones();
            cart = []; // Clear the cart array
            updateCart(); // Update the cart display
            orderForm.reset(); // Reset the form
            customerAddressLabel.hidden = true;
            customerAddressInput.hidden = true;
            customerAddressInput.removeAttribute('required');
            submitting = false;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error submitting your order.');
            submitting = false;
        });
    }

    orderType.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
    
        // Assuming productPrices is defined somewhere with 'delivery' as a key
        const deliveryFee = { id: 'delivery', name: 'Delivery Fee', price: productPrices['delivery'] };
    
        if (selectedValue === 'delivery') {
            // Show the address
            customerAddressLabel.hidden = false;
            customerAddressInput.hidden = false;
            customerAddressInput.setAttribute('required', '');
            // Add the delivery fee to the cart
            cart.push(deliveryFee);
        } else if (selectedValue === 'pickup') {
            // Hide address
            customerAddressLabel.hidden = true;
            customerAddressInput.hidden = true;
            customerAddressInput.removeAttribute('required');
            // Remove the delivery fee from the cart
            const index = cart.findIndex(item => item.id === 'delivery');
            if (index !== -1) {
                cart.splice(index, 1);
            }
        }
    
        updateCart();
    });

    // Event listener for form submission
    orderForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Check if the cart contains only 'Delivery Fee' or is empty
        const hasItemsOtherThanDeliveryFee = cart.some(item => item.id !== 'delivery');
        if (!hasItemsOtherThanDeliveryFee) {
            alert('Please select at least one item besides the delivery fee.');
            return;
        }

        if (submitting) {
            alert('Multiple submissions at once are not permitted!');
        } else {
            submitOrder();
        }
    });

    clearCartButton.addEventListener('click', () => {
        cart = []; // Clear the cart array
        if (orderType.value == 'delivery'){
            cart.push({
                id: 'delivery',
                name: 'Delivery Fee', // Just get the name without price
                price: productPrices['delivery']
            });
        }
        updateCart(); // Update the cart display
    });
});
