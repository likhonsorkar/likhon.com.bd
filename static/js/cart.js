document.addEventListener('DOMContentLoaded', () => {
    // Try to get cart from localStorage, or initialize an empty array
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Function to save the cart to localStorage and update the count in the nav
    const saveCart = () => {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
    };

    // Function to update the cart count indicator in the navigation
    const updateCartCount = () => {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            cartCountElement.textContent = totalItems;
        }
    };

    // Add event listeners to all "Add to Cart" buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (e) => {
            const productCard = e.target.closest('.product-card');
            const productId = productCard.dataset.id;
            const productName = productCard.dataset.name;
            const productPrice = parseFloat(productCard.dataset.price);
            
            const existingItem = cart.find(item => item.id === productId);

            if (existingItem) {
                existingItem.quantity++;
            } else {
                cart.push({ id: productId, name: productName, price: productPrice, quantity: 1 });
            }
            
            saveCart();
            alert(`${productName} was added to your cart.`);
        });
    });

    // --- Cart Page Specific Logic ---
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');

    // Function to render cart items on the cart page
    const renderCartPage = () => {
        if (!cartItemsContainer || !cartTotalElement) return;

        cartItemsContainer.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p>Your cart is empty.</p>';
            cartTotalElement.textContent = '$0.00';
            return;
        }

        cart.forEach((item, index) => {
            total += item.price * item.quantity;
            const itemElement = document.createElement('div');
            itemElement.className = 'flex items-center justify-between py-4 border-b';
            itemElement.innerHTML = `
                <div class="flex items-center">
                    <img src="../img/${item.id}.jpg" alt="${item.name}" class="w-20 h-20 object-cover rounded-md mr-4">
                    <div>
                        <h3 class="font-bold">${item.name}</h3>
                        <p class="text-gray-600">$${item.price.toFixed(2)}</p>
                    </div>
                </div>
                <div class="flex items-center">
                    <input type="number" value="${item.quantity}" min="1" class="w-16 p-2 border rounded-md quantity-input" data-index="${index}">
                    <button class="ml-4 text-red-500 hover:text-red-700 remove-item" data-index="${index}"><i class="fas fa-trash"></i></button>
                </div>
            `;
            cartItemsContainer.appendChild(itemElement);
        });

        cartTotalElement.textContent = `$${total.toFixed(2)}`;
    };

    // Event delegation for quantity changes and item removal
    if (cartItemsContainer) {
        cartItemsContainer.addEventListener('change', e => {
            if (e.target.classList.contains('quantity-input')) {
                const index = parseInt(e.target.dataset.index);
                const newQuantity = parseInt(e.target.value);
                if (newQuantity > 0) {
                    cart[index].quantity = newQuantity;
                    saveCart();
                    renderCartPage();
                }
            }
        });

        cartItemsContainer.addEventListener('click', e => {
            const removeButton = e.target.closest('.remove-item');
            if (removeButton) {
                const index = parseInt(removeButton.dataset.index);
                cart.splice(index, 1);
                saveCart();
                renderCartPage();
            }
        });
    }

    // Initial setup on page load
    updateCartCount();
    renderCartPage(); // This will only run on the cart page
});
