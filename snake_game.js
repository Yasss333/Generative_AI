// Simple Snake Game in JavaScript

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let snake = [{ x: 10, y: 10 }];
let direction = { x: 1, y: 0 };
let food = { x: 15, y: 15 };
let gameOver = false;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (gameOver) {
        ctx.fillStyle = 'red';
        ctx.fillText('Game Over', canvas.width / 2 - 30, canvas.height / 2);
        return;
    }

    // Draw Snake
    ctx.fillStyle = 'green';
    snake.forEach(part => {
        ctx.fillRect(part.x * 10, part.y * 10, 10, 10);
    });

    // Draw Food
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x * 10, food.y * 10, 10, 10);
}

function update() {
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    // Check for collision with food
    if (head.x === food.x && head.y === food.y) {
        snake.unshift(head);
        spawnFood();
    } else {
        snake.unshift(head);
        snake.pop();
    }

    // Check for wall collisions
    if (head.x < 0 || head.x >= canvas.width / 10 || head.y < 0 || head.y >= canvas.height / 10) {
        gameOver = true;
    }
}

function spawnFood() {
    food = { x: Math.floor(Math.random() * (canvas.width / 10)), y: Math.floor(Math.random() * (canvas.height / 10)) };
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp' && direction.y === 0) {
        direction = { x: 0, y: -1 };
    } else if (event.key === 'ArrowDown' && direction.y === 0) {
        direction = { x: 0, y: 1 };
    } else if (event.key === 'ArrowLeft' && direction.x === 0) {
        direction = { x: -1, y: 0 };
    } else if (event.key === 'ArrowRight' && direction.x === 0) {
        direction = { x: 1, y: 0 };
    }
});

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();