//TODO: make an onload function
window.onload = makeAjaxRequest('POST', '/homepage', loadDiv, {"id": get_cookie("id")}, "div");
window.onload = makeAjaxRequest('POST', '/header', loadDiv, {"id": get_cookie("id")}, "header");

//Generic method to make a request and get a response
//method: 'GET', 'POST', 'PUT', 'DELETE', etc.
//path: the path for the request
//inputFunction: function to call after getting response from the server
//data: the data to send- note that it will be converted to a json string before sending
function makeAjaxRequest(method, path, inputFunction, data, div_id) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            inputFunction(this, div_id);
        }
    };
    xhttp.open(method, path);
    xhttp.send(JSON.stringify(data));
}

//Sign in request + response
function sign_in() {
    const username = document.getElementById("sign-in-username").value;
    const password = document.getElementById("sign-in-password").value;
    const data = {"username": username, "password": password};
    makeAjaxRequest('POST', '/sign-in', sign_in_complete, data);
}

function sign_in_complete(xhttp) {
    const user_id = JSON.parse(xhttp.responseText)["id"];
    if (user_id > 0) {
        document.cookie = "id=" + user_id; //save the cookie
        makeAjaxRequest('POST', '/homepage', loadDiv, {"id": get_cookie("id")}, "div");
        makeAjaxRequest('POST', '/header', loadDiv, {"id": get_cookie("id")}, "header");
    }
    document.getElementById("sign-in-username").value = "";
    document.getElementById("sign-in-password").value = "";
}

function loadDiv(data, div_id) {
    const div = document.getElementById(div_id);
    div.innerHTML = data.responseText;
}



// ------------------------------------COOKIE FUNCTIONS ---------------------------

// function gets the cookie, given the cookie id. If cookie is not found, it returns ""
function get_cookie(key) { //TODO: this will probably be wrong for the future, need to figure out exactly how cookies are stored, but for now it works
    all_cookies = document.cookie;
    cookie_splits = all_cookies.split(";");
    for (let i = 0; i < cookie_splits.length; i++) {
        cookie_values = cookie_splits[i].split("=");
        if (cookie_values.length == 2) {
            if (cookie_values[0] == key) {
                return cookie_values[1];
            }
        }
    }
    return "";
}