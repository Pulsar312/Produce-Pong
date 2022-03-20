function pageLoaded() {
    makeAjaxRequest('POST', '/homepage', loadDiv, {});
    makeAjaxRequest('POST', '/header', loadHeader, {});
}

//Generic method to make a request and get a response
//method: 'GET', 'POST', 'PUT', 'DELETE', etc.
//path: the path for the request
//inputFunction: function to call after getting response from the server
//data: the data to send- note that it will be converted to a json string before sending
function makeAjaxRequest(method, path, inputFunction, data, isBinaryData = false) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            inputFunction(this);
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
    makeAjaxRequest(form.method, form.action, callback, new FormData(form), true);
    return false; // Avoid a page reload
}

function loadDiv(data) {
    const div = document.getElementById("div");
    div.innerHTML = data.responseText;
}

function loadHeader(data) {
    const div = document.getElementById("header");
    div.innerHTML = data.responseText;
}
