document.addEventListener('DOMContentLoaded', () => {

    const addToCartButton = document.getElementById('add-to-cart');
    const clearCartButton = document.getElementById('clear-cart');
    const cartItemsList = document.getElementById('cart-items');
    const totalCostSpan = document.getElementById('total-cost');
    const productSelect = document.getElementById('product-select');

    const prices = {
        'small-treats': 10.00,
        'large-treats': 10.00
    };

    let cart = [];
    let submitting = false;

    function updateCart() {
        // Clear the current items list
        cartItemsList.innerHTML = '';

        // Group items by name and sum their quantities and prices
        const groupedItems = cart.reduce((acc, item) => {
            if (!acc[item.name]) {
                acc[item.name] = {
                    price: item.price,
                    quantity: 0,
                    totalPrice: 0
                };
            }
            acc[item.name].quantity++;
            acc[item.name].totalPrice += item.price;
            return acc;
        }, {});

        // Update list with grouped cart items
        Object.entries(groupedItems).forEach(([name, item]) => {
            const li = document.createElement('li');
            li.textContent = `${item.quantity}x ${name} - $${item.totalPrice.toFixed(2)}`;
            cartItemsList.appendChild(li);
        });

        // Calculate total cost
        const totalCost = Object.values(groupedItems).reduce((total, item) => total + item.totalPrice, 0);
        totalCostSpan.textContent = totalCost.toFixed(2);
    }

    addToCartButton.addEventListener('click', () => {
        
        const selectedValue = productSelect.value;
        const selectedOption = productSelect.options[productSelect.selectedIndex];

        if (selectedValue) {
            cart.push({
                name: selectedOption.text.split(' - ')[0], // Just get the name without price
                price: prices[selectedValue]
            });

            updateCart();
        } else {
            alert('Please select a product to add to your cart.');
        }
    });

    // Additional variables for new form fields
    const orderForm = document.getElementById('order-form');
    const customerNameInput = document.getElementById('customer-name');
    const customerPhoneInput = document.getElementById('customer-phone');
    const customerEmailInput = document.getElementById('customer-email');
    const orderNotesTextarea = document.getElementById('order-notes');
    
    // Function to submit the order
    function submitOrder() {
        const orderType = document.getElementById('order-type').value;
        const customerName = customerNameInput.value.trim();
        const customerPhone = customerPhoneInput.value.trim();
        const customerEmail = customerEmailInput.value.trim();
        const orderNotes = orderNotesTextarea.value.trim();
        
        // Construct the order data
        const orderData = {
            orderType: orderType,
            customerName: customerName,
            phoneNumber: customerPhone,
            email: customerEmail,
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
            rainBones();
            alert('Order submitted successfully!');
            rainBones(); // Call rainBones() to start the animation
            cart = []; // Clear the cart array
            updateCart(); // Update the cart display
            orderForm.reset(); // Reset the form
            submitting = false;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error submitting your order.');
            submitting = false;
        });
    }

    // Event listener for form submission
    orderForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission
        if(cart.length == 0){
            alert('Please select at least one item. You can\'t buy nothing!');
            return;
        }
        if (submitting)
            alert('Multiple submissions at once is not permitted!')
        else
            submitOrder();
    });

    clearCartButton.addEventListener('click', () => {
        cart = []; // Clear the cart array
        updateCart(); // Update the cart display
    });
});
