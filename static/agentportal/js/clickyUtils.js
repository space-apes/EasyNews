/*
	to be called whenever delivery checkbox is 
	clicked
 */
function onDeliveryClick(id)
{
	let xhr = new XMLHttpRequest();
	xhr.open('POST', 'updateDeliveryStatus', true)
	xhr.setRequestHeader('X-CSRFToken', csrfToken)
	xhr.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
	dataObj = {id: id}
	xhr.send(JSON.stringify(dataObj));

}
