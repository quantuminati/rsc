// If you have jquery installed
$(
	function sendData (url, data, func) {
		$.ajax({
			method: "POST",
			url: url,
			data: data,
			success: func
		});
	}
);
