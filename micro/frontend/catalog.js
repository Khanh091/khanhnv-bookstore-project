// Catalog page functionality

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect in checkAuth()
} else {
    const userName = getCustomerName();
    if (userName) {
        document.getElementById('userName').textContent = `Welcome, ${userName}!`;
    }
    
    loadBooks();
}

async function loadBooks() {
    const loadingDiv = document.getElementById('loading');
    const booksContainer = document.getElementById('booksContainer');
    
    try {
        const response = await fetch(`${API_CONFIG.BOOK_SERVICE}/api/books/`);
        const data = await response.json();
        
        loadingDiv.style.display = 'none';
        
        if (response.ok && data.books) {
            displayBooks(data.books);
        } else {
            showMessage('message', 'Failed to load books');
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        showMessage('message', `Error: ${error.message}`);
    }
}

function displayBooks(books) {
    const container = document.getElementById('booksContainer');
    
    if (books.length === 0) {
        container.innerHTML = '<p>No books available</p>';
        return;
    }
    
    container.innerHTML = books.map(book => `
        <div class="book-card">
            <h3>${book.title}</h3>
            <p class="author">by ${book.author}</p>
            <p class="price">$${book.price}</p>
            <p class="stock">Stock: ${book.stock}</p>
            <div class="book-actions">
                <input type="number" id="qty_${book.id}" value="1" min="1" max="${book.stock}" class="quantity-input">
                <button onclick="addToCart(${book.id})">Add to Cart</button>
            </div>
        </div>
    `).join('');
}

async function addToCart(bookId) {
    const quantity = parseInt(document.getElementById(`qty_${bookId}`).value) || 1;
    const customerId = getCustomerId();
    
    try {
        const response = await fetch(`${API_CONFIG.CART_SERVICE}/api/carts/add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_id: customerId,
                book_id: bookId,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('message', 'Book added to cart!', 'success');
        } else {
            showMessage('message', data.error || 'Failed to add to cart');
        }
    } catch (error) {
        showMessage('message', `Error: ${error.message}`);
    }
}
