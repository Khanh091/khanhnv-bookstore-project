// Utility functions

function showMessage(elementId, message, type = 'error') {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = `message ${type}`;
        element.style.display = 'block';
        
        if (type === 'success') {
            setTimeout(() => {
                element.style.display = 'none';
            }, 3000);
        }
    }
}

function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

// Tab switching
function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
}

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
}

// Authentication handlers
async function handleRegister(event) {
    event.preventDefault();
    hideMessage('registerMessage');
    
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    
    try {
        const response = await fetch(`${API_CONFIG.CUSTOMER_SERVICE}/api/customers/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('registerMessage', 'Registration successful! Please login.', 'success');
            setTimeout(() => {
                showLogin();
                document.querySelector('.tab').click();
            }, 1500);
        } else {
            showMessage('registerMessage', data.error || 'Registration failed');
        }
    } catch (error) {
        showMessage('registerMessage', `Error: ${error.message}`);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    hideMessage('loginMessage');
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_CONFIG.CUSTOMER_SERVICE}/api/customers/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store customer info in localStorage
            localStorage.setItem(STORAGE_KEYS.CUSTOMER_ID, data.id);
            localStorage.setItem(STORAGE_KEYS.CUSTOMER_NAME, data.name);
            
            // Redirect to catalog
            window.location.href = 'catalog.html';
        } else {
            showMessage('loginMessage', data.error || 'Invalid credentials');
        }
    } catch (error) {
        showMessage('loginMessage', `Error: ${error.message}`);
    }
}

function logout() {
    localStorage.removeItem(STORAGE_KEYS.CUSTOMER_ID);
    localStorage.removeItem(STORAGE_KEYS.CUSTOMER_NAME);
    window.location.href = 'index.html';
}

// Check authentication
function checkAuth() {
    const customerId = localStorage.getItem(STORAGE_KEYS.CUSTOMER_ID);
    if (!customerId) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

function getCustomerId() {
    return localStorage.getItem(STORAGE_KEYS.CUSTOMER_ID);
}

function getCustomerName() {
    return localStorage.getItem(STORAGE_KEYS.CUSTOMER_NAME);
}
