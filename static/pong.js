// Websocket connection is dynamically created in the HTML template
// Accessible via `socket`

socket.addEventListener("message", event => {
    updateGame(event.data);
});

function updateGame(data) {
    console.log("Update game (got from server) " + data);
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