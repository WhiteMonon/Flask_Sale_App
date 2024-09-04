function Checkout(event) {
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;
    const paymentMethod = document.getElementById('payment-method').value;
    event.preventDefault();

    fetch('/api/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            
            phone: phone,
            address: address,
            paymentMethod: paymentMethod
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            console.log(data.message);
            window.location.href = '/';
        } else {
            alert(data.message);
            console.log(data.message);
        }
    });
};
