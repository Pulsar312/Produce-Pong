// Websocket connection is dynamically created in the HTML template
// Accessible via `socket`

socket.addEventListener("message", event => {
    updateGame(JSON.parse(event.data));
});

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
    const left_score = document.getElementById("left_score");
    const right_score = document.getElementById("right_score");
    const left_username = document.getElementById("left_username");
    const right_username = document.getElementById("right_username");
    const ingredient_image = document.getElementById("current_ingredient_img");
    const ingredient_text = document.getElementById("current_ingredient_name");
    left_score.innerHTML = data.left.score;
    right_score.innerHTML = data.right.score;
    left_username.innerHTML = data.left.username;
    right_username.innerHTML = data.right.username;
    ingredient_text.innerHTML = data.current_ingredient.name;
    ingredient_image.src = data.current_ingredient.image;

    // Update which ingredients both players have
    const left_ingredients = document.getElementById("left_ingredients");
    const right_ingredients = document.getElementById("right_ingredients");

    left_ingredients.innerHTML = "";
    right_ingredients.innerHTML = "";

    // TODO: this is incredibly laggy and makes way too many GET requests. We're going to need some kind of caching.

    for (let ingredient of data.left.chef.ingredients) {
        const elem = document.createElement("img");
        elem.src = ingredient.image;
        elem.id = "left-ingredient";
        left_ingredients.appendChild(elem);
    }

    for (let ingredient of data.right.chef.ingredients) {
        const elem = document.createElement("img");
        elem.src = ingredient.image;
        elem.id = "right-ingredient"
        right_ingredients.appendChild(elem);
    }


}

function movePlayer(velocity) {
    const data = {"velocity": velocity};
    socket.send(JSON.stringify(data));
}

document.addEventListener("keydown", event => {
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