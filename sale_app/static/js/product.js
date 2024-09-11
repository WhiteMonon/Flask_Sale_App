// nút tăng giảm số lượng sản phẩm
document.addEventListener('DOMContentLoaded', function () {
	const decrementButton = document.getElementById('button-decrement');
	const incrementButton = document.getElementById('button-increment');
	const inputQuantity = document.getElementById('inputQuantity');

	// nút giảm số lượng sản phẩm
	decrementButton.addEventListener('click', function () {
		let currentValue = parseInt(inputQuantity.value);
		if (currentValue > 1) {
			inputQuantity.value = currentValue - 1;
		}
	});

	// nút tăng số lượng sản phẩm
	incrementButton.addEventListener('click', function () {
		let currentValue = parseInt(inputQuantity.value);
		let max = parseInt(inputQuantity.getAttribute('max'));
		if (currentValue < max) {
			inputQuantity.value = currentValue + 1;

		}
	});
});