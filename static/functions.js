window.onload = toggle_homepage;

//Generic method to make a request and get a response
//method: 'GET', 'POST', 'PUT', 'DELETE', etc.
//path: the path for the request
//inputFunction: function to call after getting response from the server
//data: the data to send- note that it will be converted to a json string before sending
function makeAjaxRequest(method, path, inputFunction, data) {
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { inputFunction(this); }
    };
    xhttp.open(method, path);
    xhttp.send(JSON.stringify(data));
}


//Sign in request + response
function sign_in() {
    const username = document.getElementById("sign-in-username").value;
    const password = document.getElementById("sign-in-password").value;
    const data = {"username":username, "password":password};
    makeAjaxRequest('POST', '/sign-in', sign_in_complete, data);
}

function sign_in_complete(xhttp) {
    const user_id = JSON.parse(xhttp.responseText)["id"];
    if (user_id > 0){
        document.cookie = "id=" + user_id; //save the cookie
        toggle_homepage(); //go to homepage
    }
    document.getElementById("sign-in-username").value = "";
    document.getElementById("sign-in-password").value = "";
}



//logout function
function logout(){
    //TODO: delete cookies
    toggle_homepage();
}



//-------------------------TOGGLE FUNCTIONS-----------------------------

function toggle_all_off(){
    document.getElementById("div_homepage_signed_out").style.display = "none";
    document.getElementById("div_homepage_signed_in").style.display = "none";
    document.getElementById("div_about").style.display = "none";
    document.getElementById("div_contact").style.display = "none";
    document.getElementById("div_play").style.display = "none";
    document.getElementById("div_profile").style.display = "none";
}

function toggle_homepage(){
    toggle_all_off();
    console.log(get_cookie("id"));
    if(get_cookie("id") != ""){
        document.getElementById("div_homepage_signed_in").style.display = "block";
        document.getElementById("Play").style.display = "none"; //hide sign-in option
        document.getElementById("Profile").style.display = "block"; //show profile option
        document.getElementById("Logout").style.display = "block"; //show Logout option
    }
    else{
        document.getElementById("div_homepage_signed_out").style.display = "block";
        document.getElementById("Play").style.display = "block"; //show sign-in option
        document.getElementById("Profile").style.display = "none"; //hide profile option
        document.getElementById("Logout").style.display = "none"; //hide Logout option
    }
}

function toggle_about(){
    toggle_all_off();
    document.getElementById("div_about").style.display = "block";
}

function toggle_contact(){
    toggle_all_off();
    document.getElementById("div_contact").style.display = "block";
}

function toggle_play(){
    toggle_all_off();
    document.getElementById("div_play").style.display = "block";
}


function toggle_profile(){
    toggle_all_off();
    document.getElementById("div_profile").style.display = "block";
}





// ------------------------------------COOKIE FUNCTIONS ---------------------------

// function gets the cookie, given the cookie id. If cookie is not found, it returns ""
function get_cookie(key){ //TODO: this will probably be wrong for the future, need to figure out exactly how cookies are stored, but for now it works
    all_cookies = document.cookie;
    cookie_splits = all_cookies.split(";");
    for(var i = 0; i < cookie_splits.length; i++){
        cookie_values = cookie_splits[i].split("=");
        if(cookie_values.length == 2){
            if(cookie_values[0] == key){
                return cookie_values[1];
            }
        }
    }
    return "";
}