function pageLoaded() {
    makeAjaxRequest('GET', '/homepage', loadDiv, {}, "div");
    makeAjaxRequest('GET', '/header', loadDiv, {}, "header");
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
    console.log(data, divId, reloadHeader)
    if (reloadHeader) {
        makeAjaxRequest('GET','/header', loadDiv, {}, "header", true, false);
    }
}

// about page randomize button
function ingredRandom() {
    var ingredients = []
    ingredients[0] = "avocado.png"
    ingredients[1] = "bacon.png"
    ingredients[2] = "banana.png"
    ingredients[3] = "beef.png"
    ingredients[4] = "bell_pepper.png"
    ingredients[5] = "blueberry.png"
    ingredients[6] = "bread.png"
    ingredients[7] = "broccoli.png"
    ingredients[8] = "broth.png"
    ingredients[9] = "butter.png"
    ingredients[10] = "caesar_dressing.png"
    ingredients[11] = "carrot.png"
    ingredients[12] = "cheese.png"
    ingredients[13] = "cherry.png"
    ingredients[14] = "chicken.png"
    ingredients[15] = "cinnamon.png"
    ingredients[16] = "corn.png"
    ingredients[17] = "cream.png"
    ingredients[18] = "cucumber.png"
    ingredients[19] = "egg.png"
    ingredients[20] = "flour.png"
    ingredients[21] = "garlic.png"
    ingredients[22] = "ham.png"
    ingredients[23] = "hot_sauce.png"
    ingredients[24] = "ice.png"
    ingredients[25] = "ketchup.png"
    ingredients[26] = "lettuce.png"
    ingredients[27] = "macaroni.png"
    ingredients[28] = "milk.png"
    ingredients[29] = "mushroom.png"
    ingredients[30] = "noodle.png"
    ingredients[31] = "onion.png"
    ingredients[32] = "pancake_mix.png"
    ingredients[33] = "pea.png"
    ingredients[34] = "peach.png"
    ingredients[35] = "pepperoni.png"
    ingredients[36] = "pork.png"
    ingredients[37] = "potato.png"
    ingredients[38] = "raspberry.png"
    ingredients[39] = "rice.png"
    ingredients[40] = "salt.png"
    ingredients[41] = "scallion.png"
    ingredients[42] = "sesame_oil.png"
    ingredients[43] = "soy_sauce.png"
    ingredients[44] = "strawberry.png"
    ingredients[45] = "sugar.png"
    ingredients[46] = "tomato.png"
    ingredients[47] = "vegetable_oil.png"

    var path = "./static/ingredients/"
    var id = ["ingred1", "ingred2", "ingred3", "ingred4", "ingred5"]

    var num = []
    for (let i = 0; i < id.length; i++) {
        num[i] = Math.floor(Math.random() * ingredients.length)
    }
 
    for (let i = 0; i < id.length; i++) {
        document.getElementById(id[i]).src = path + ingredients[num[i]]
    }
}