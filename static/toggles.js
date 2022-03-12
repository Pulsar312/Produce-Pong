function toggle_all_off(){
    document.getElementById("div_homepage").style.display = "none";
    document.getElementById("div_about").style.display = "none";
    document.getElementById("div_contact").style.display = "none";
    document.getElementById("div_play").style.display = "none";
}

function toggle_homepage(){
    toggle_all_off();
    document.getElementById("div_homepage").style.display = "block";
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