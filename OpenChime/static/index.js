var error_displayed = false
setInterval(function(){$.ajax({
url: '/update',
type: 'POST',
success: function(response) {
	console.log(response);
	$("#time").html("Current time: " + response["time"]);
	$("#uptime").html("Uptime: " + response["uptime"]);
	$("#status").html("Status: " + response["status"]);
	$("#internet_status").html("Internet status: " + response["internet_status"]);
	$("#ip_address").html("IP Address: " + response["ip_address"]);
	$("#con_type").html("Connection Type: " + response["con_type"]);
	$("#last_bell").html("Last Bell: " + response["last_bell"]);
	$("#next_bell").html("Next Bell: " + response["next_bell"]);
	error_displayed = false
},
error: function(error) {
	console.log(error);
	if (error_displayed == false) {
		window.alert("The web interface has been disconnected. Attempting to reconnect");
		error_displayed = true;
	}
}
})}, 1000);