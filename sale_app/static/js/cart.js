function updateCartCount() {
    fetch('/count_cart_item')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cart-count').textContent = data.count;
            updateCartTotal();
        });
}

function updateCartTotalItem(id) {
    fetch('/api/get_cart_total_item', {
        method: 'POST',
        body: JSON.stringify({
            id: id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`cart-total-${id}`).textContent = data.total;
        });
}
    
// thêm sản phẩm vào giỏ hàng
function addToCart(productId, productName, productPrice, quantity = 1) {
    if (quantity == 'inputQuantity') {
        quantity = document.getElementById('inputQuantity').value;
    }

    if (isNaN(quantity)) {
        quantity = 0;
    }
    fetch('/api/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        updateCartCount(data.count);
        if (data.success) {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message , 'error');
        }

    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function removeFromCart(id) {
    fetch('/api/remove_from_cart', {
        method: 'POST',
        body: JSON.stringify({
            id: id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        updateCartCount();  

        const row = document.getElementById(`cart-item-${id}`);
        if (row) {
            row.remove();
        }
        
        if (data.count === 0) {
            const tableBody = document.querySelector('tbody');
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center">Giỏ hàng của bạn đang trống</td></tr>';
        }
    });
}

function updateCartItem(id, quantity) {
    fetch('/api/update_cart_item', {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            quantity: quantity,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount();  
            updateCartTotalItem(id);
        } else {
            const cart_item_quantity = document.getElementById(`cart-item-quantity-${id}`);
            cart_item_quantity.value = cart_item_quantity.getAttribute('max');
            showNotification(data.message , 'error');
        }
    }); 
}

function updateCartTotal() {
    fetch('/api/get_cart_total')
        .then(response => response.json())
        .then(data => {
            if (window.location.pathname === '/cart') {
                document.getElementById('cart-total').textContent = data.total;
            }
        });
}

function showNotification(message, type = 'success') {
    const notifications = document.getElementById('notifications-container');
    if (!notifications) {
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000;';
        document.body.appendChild(container);
    }

    const notification = document.createElement('div');
    notification.className = `alert ${type === 'success' ? 'alert-success' : 'alert-danger'}`;
    notification.style.cssText = 'margin-bottom: 10px; min-width: 200px;';
    notification.textContent = message;

    document.getElementById('notifications-container').appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            notification.remove();
            if (document.getElementById('notifications-container').childElementCount === 0) {
                document.getElementById('notifications-container').remove();
            }
        }, 500);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', updateCartCount);
