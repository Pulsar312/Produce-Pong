function pageLoaded() {
    makeAjaxRequest('GET', '/homepage', loadDiv, {}, "div");
    makeAjaxRequest('GET', '/header', loadDiv, {}, "header");
}

//Generic method to make a request and get a response
//method: 'GET', 'POST', 'PUT', 'DELETE', etc.
//path: the path for the request
//inputFunction: function to call after getting response from the server
//data: the data to send- note that it will be converted to a json string before sending
function makeAjaxRequest(method, path, inputFunction, data, div_id, isBinaryData = false) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (div_id !== "") {
                inputFunction(this, div_id);
            } else {
                inputFunction(this);
            }
        }
    };
    xhttp.open(method, path);
    if (isBinaryData) {
        xhttp.send(data);
    } else {
        xhttp.send(JSON.stringify(data));
    }
}

function submitAjaxForm(form, callback) {
    makeAjaxRequest(form.method, form.action, callback, new FormData(form), "div", true);
    return false; // This is important! Prevents the browser from loading a new page on form submission.
}

function loadDiv(data, div_id) {
    const div = document.getElementById(div_id);
    div.innerHTML = data.responseText;
}
