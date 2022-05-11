"use strict";
// Websocket connection is dynamically created in the HTML template
// Accessible via `socket`

socket.addEventListener("message", event => {
    updateGame(JSON.parse(event.data));
});

let previousFrame = null;  // The previous "data" received. Used for determining what has changed between frames

// Find all our elements only ONCE to reduce overhead in a loop
const left_score = document.getElementById("left_score");
const right_score = document.getElementById("right_score");
const left_username = document.getElementById("left_username");
const right_username = document.getElementById("right_username");
const ingredient_image = document.getElementById("current_ingredient_img");
const ingredient_text = document.getElementById("current_ingredient_name");
const left_ingredients = document.getElementById("left_ingredients");
const right_ingredients = document.getElementById("right_ingredients");
const loading_div = document.getElementById("loading-div");
const left_status = document.getElementById("left-status");
const right_status = document.getElementById("right-status");

function updateGame(data) {
    // Update the position of the paddles and ball
    const left = document.getElementById("left");
    left.style.top = `${data.left.paddle.y}px`;
    const right = document.getElementById("right");
    right.style.top = `${data.right.paddle.y}px`;
    const ball = document.getElementById("ball");
    ball.style.top = `${data.ball.physics_object.y}px`;
    ball.style.left = `${data.ball.physics_object.x}px`;

    // Update scores, usernames, and current ingredient

    if (!previousFrame || previousFrame.left.score !== data.right.score) {
        left_score.innerHTML = data.left.score;
    }

    if (!previousFrame || previousFrame.right.score !== data.right.score) {
        right_score.innerHTML = data.right.score;
    }

    if (!previousFrame || previousFrame.left.username !== data.left.username) {
        left_username.innerHTML = data.left.username;
    }

    if (!previousFrame || previousFrame.right.username !== data.right.username) {
        right_username.innerHTML = data.right.username;
    }

    if (!previousFrame || previousFrame.current_ingredient.name !== data.current_ingredient.name) {
        ingredient_text.innerHTML = data.current_ingredient.name;
    }

    if (!previousFrame || previousFrame.current_ingredient.image !== data.current_ingredient.image) {
        ingredient_image.src = data.current_ingredient.image;
    }

    // Update which ingredients both players have
    if (!previousFrame || previousFrame.left.chef.ingredients !== data.left.chef.ingredients) {
        left_ingredients.innerHTML = "";
        for (let ingredient of data.left.chef.ingredients) {
            const elem = document.createElement("img");
            elem.src = ingredient.image;
            elem.id = "left-ingredient";
            left_ingredients.appendChild(elem);
        }
    }

    if (!previousFrame || previousFrame.right.chef.ingredients !== data.right.chef.ingredients) {
        right_ingredients.innerHTML = "";
        for (let ingredient of data.right.chef.ingredients) {
            const elem = document.createElement("img");
            elem.src = ingredient.image;
            elem.id = "right-ingredient"
            right_ingredients.appendChild(elem);
        }
    }

    // Handle waiting before the game starts
    if (!data.game_started) {
        if (data.left.ready) {
            left_status.innerHTML = `${data.left.username} is ready!`;
        } else if (data.left.username) {
            left_status.innerHTML = `${data.left.username} is NOT ready.`;
        } else {
            left_status.innerHTML = "Waiting for the left player to join...";
        }

        if (data.right.ready) {
            right_status.innerHTML = `${data.right.username} is ready!`;
        } else if (data.right.username) {
            right_status.innerHTML = `${data.right.username} is NOT ready.`;
        } else {
            right_status.innerHTML = "Waiting for the right player to join...";
        }

    } else {
        loading_div.style.visibility = "hidden";
        ball.style.visibility = "";
    }

    // Handle the game ending
    if (data.game_over) {
        window.location.reload();
    }

    // Update the previous frame to this frame for the next time through this "loop"
    previousFrame = data;
}

function movePlayer(velocity) {
    const data = {"velocity": velocity};
    socket.send(JSON.stringify(data));
}

document.addEventListener("keydown", event => {
    event.preventDefault();  // Prevent scrolling the page

    let up_keys = ["KeyW", "ArrowUp", "KeyK"];
    let down_keys = ["KeyS", "ArrowDown", "KeyJ"];

    if (up_keys.includes(event.code)) {
        movePlayer(-1);
    } else if (down_keys.includes(event.code)) {
        movePlayer(1);
    }
});

document.addEventListener("keyup", event => {
    movePlayer(0);
});