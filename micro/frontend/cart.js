// Cart page functionality

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect in checkAuth()
} else {
    loadCart();
}

async function loadCart() {
    const loadingDiv = document.getElementById('loading');
    const cartContainer = document.getElementById('cartContainer');
    const customerId = getCustomerId();
    
    try {
        // Get cart items
        const cartResponse = await fetch(`${API_CONFIG.CART_SERVICE}/api/carts/${customerId}/`);
        const cartData = await cartResponse.json();
        
        if (!cartResponse.ok) {
            throw new Error(cartData.error || 'Failed to load cart');
        }
        
        // Get all books
        const booksResponse = await fetch(`${API_CONFIG.BOOK_SERVICE}/api/books/`);
        const booksData = await booksResponse.json();
        
        if (!booksResponse.ok) {
            throw new Error('Failed to load book details');
        }
        
        loadingDiv.style.display = 'none';
        
        // Create books map
        const booksMap = {};
        booksData.books.forEach(book => {
            booksMap[book.id] = book;
        });
        
        // Enrich cart items with book details
        const items = cartData.items || [];
        const enrichedItems = items.map(item => {
            const book = booksMap[item.book_id];
            if (book) {
                return {
                    ...item,
                    book: book,
                    subtotal: parseFloat(book.price) * item.quantity
                };
            }
            return null;
        }).filter(item => item !== null);
        
        // Calculate total
        const total = enrichedItems.reduce((sum, item) => sum + item.subtotal, 0);
        
        displayCart(enrichedItems, total);
        
    } catch (error) {
        loadingDiv.style.display = 'none';
        showMessage('message', `Error: ${error.message}`);
    }
}

function displayCart(items, total) {
    const container = document.getElementById('cartContainer');
    
    if (items.length === 0) {
        container.innerHTML = '<p>Your cart is empty</p>';
        return;
    }
    
    const itemsHTML = items.map(item => `
        <div class="cart-item">
            <div class="item-info">
                <h3>${item.book.title}</h3>
                <p class="author">by ${item.book.author}</p>
                <p class="price">$${item.book.price} each</p>
            </div>
            <div class="item-quantity">
                <span>Quantity: ${item.quantity}</span>
            </div>
            <div class="item-subtotal">
                <strong>$${item.subtotal.toFixed(2)}</strong>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = `
        <div class="cart-items">
            ${itemsHTML}
        </div>
        <div class="cart-total">
            <h2>Total: $${total.toFixed(2)}</h2>
        </div>
    `;
}
