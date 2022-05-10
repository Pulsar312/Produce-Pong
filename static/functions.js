function pageLoaded() {
    makeAjaxRequest('GET', '/homepage', loadDiv, {}, "div");
    makeAjaxRequest('GET', '/header', loadDiv, {}, "header");
    setInterval(pageloadNotification, 1000);
}

//Generic method to make a request and get a response
//method: 'GET', 'POST', 'PUT', 'DELETE', etc.
//path: the path for the request
//inputFunction: function to call after getting response from the server
//data: the data to send- note that it will be converted to a json string before sending
//"makeAjaxRequest(`POST`, `/auth/logout`, loadDiv, {}, 'div', false, true);"
function makeAjaxRequest(method, path, inputFunction, data, divId, isBinaryData = false, reloadHeader = false) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (divId !== "") {
                inputFunction(this, divId, reloadHeader);
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

function submitAjaxForm(form, callback, reloadHeader = false) {
    makeAjaxRequest(form.method, form.action, callback, new FormData(form), "div", true, reloadHeader);
    return false; // This is important! Prevents the browser from loading a new page on form submission.
}

function loadDiv(data, divId, reloadHeader = false) {
    const div = document.getElementById(divId);
    div.innerHTML = data.responseText;
    if (reloadHeader) {
        makeAjaxRequest('GET', '/header', loadDiv, {}, "header");
        makeAjaxRequest('GET', '/newmessage', loadDiv, {}, "notification");
    }
}

function pageloadNotification() {
    makeAjaxRequest('GET', '/newmessage', loadDiv, {}, "notification");
}

// about page randomize button
function ingredRandom() {
    makeAjaxRequest('GET', '/about_ingredients', loadDiv, {}, 'preview-ingreds')
    const div = document.getElementById("preview-ingreds")
    var ingredients = JSON.parse(div.innerHTML)
    var imgID = ["ingred1", "ingred2", "ingred3", "ingred4", "ingred5"]
    for (let i = 0; i < imgID.length; i++) {
        document.getElementById(imgID[i]).src = ingredients[i]
    }
}

