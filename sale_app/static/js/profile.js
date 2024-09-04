
function UpdateProfile() {
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const fullname = document.getElementById('fullname').value;

    fetch('/api/update_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            address: address,
            phone: phone,
            fullname: fullname
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Cập nhật thông tin thành công!');
            window.location.reload();
        } else {
            alert('Có lỗi xảy ra khi cập nhật thông tin. Vui lòng thử lại.');   
        }
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert('Đã xảy ra lỗi. Vui lòng thử lại sau.');
    });
}
