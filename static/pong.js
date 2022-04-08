// Websocket connection is dynamically created in the HTML template
// Accessible via `socket`

socket.addEventListener("message", event => {
    updateGame(JSON.parse(event.data));
});

function updateGame(data) {
    const left = document.getElementById("left");
    left.style.top = `${data.left.paddle.y}px`;
    const right = document.getElementById("right");
    right.style.top = `${data.right.paddle.y}px`;
    const ball = document.getElementById("ball");
    ball.style.top = `${data.ball.physics_object.y}px`;
    ball.style.left = `${data.ball.physics_object.x}px`;
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