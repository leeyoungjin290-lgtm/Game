<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>6 Stage Battle</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game {
    display: block;
    background: #181818;
    margin: auto;
}

#ui {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 10;
    font-size: 16px;
    line-height: 1.6;
    pointer-events: none;
}

#message {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: rgba(0,0,0,0.75);
    z-index: 20;
}

#message h1 {
    font-size: 48px;
    margin: 10px;
}

button {
    padding: 12px 20px;
    margin: 5px;
    border: none;
    border-radius: 8px;
    background: #444;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #666;
}

.upgrade {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: rgba(0,0,0,0.8);
    z-index: 15;
}

.upgrade h2 {
    font-size: 36px;
}

.upgrade button {
    width: 260px;
}
</style>
</head>

<body>

<canvas id="game" width="1000" height="650"></canvas>

<div id="ui">
    <div>❤️ HP: <span id="hp">100</span></div>
    <div>⚔️ ATK: <span id="atk">10</span></div>
    <div>⚡ 공격속도: <span id="speed">1.0</span></div>
    <div>🎯 치명타: <span id="crit">5</span>%</div>
    <div>💥 치명타 피해: <span id="critDmg">150</span>%</div>
    <div>💰 PT: <span id="pt">0</span></div>
    <div>🏆 Stage: <span id="stage">1</span> / 6</div>
    <div>👾 남은 적: <span id="enemyCount">0</span></div>
</div>

<div id="upgrade" class="upgrade">
    <h2>STAGE CLEAR!</h2>
    <p>획득한 PT를 사용해서 능력을 강화하세요.</p>

    <button onclick="upgradeStat('atk')">
        공격력 +5 — 50 PT
    </button>

    <button onclick="upgradeStat('speed')">
        공격속도 +10% — 70 PT
    </button>

    <button onclick="upgradeStat('crit')">
        치명타 확률 +5% — 80 PT
    </button>

    <button onclick="upgradeStat('critDmg')">
        치명타 피해 +25% — 100 PT
    </button>

    <button onclick="nextStage()">
        다음 스테이지 →
    </button>
</div>

<div id="message">
    <h1 id="messageTitle"></h1>
    <p id="messageText"></p>
    <button onclick="location.reload()">다시 시작</button>
</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

const keys = {};

let mouse = {
    x: W / 2,
    y: H / 2,
    down: false
};

document.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()] = true;
});

document.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});

canvas.addEventListener("mousemove", e => {
    const rect = canvas.getBoundingClientRect();

    mouse.x = (e.clientX - rect.left) * W / rect.width;
    mouse.y = (e.clientY - rect.top) * H / rect.height;
});

canvas.addEventListener("mousedown", () => {
    mouse.down = true;
});

canvas.addEventListener("mouseup", () => {
    mouse.down = false;
});


/* =========================
   게임 데이터
========================= */

let gameRunning = true;
let stage = 1;
let pt = 0;

let player = {
    x: W / 2,
    y: H / 2,

    radius: 18,

    hp: 100,
    maxHp: 100,

    atk: 10,

    attackSpeed: 1.0,
    attackCooldown: 0,

    crit: 5,
    critDmg: 150,

    moveSpeed: 4
};

let enemies = [];
let bullets = [];

let kills = 0;


/* =========================
   스테이지
========================= */

function spawnStage() {

    enemies = [];
    bullets = [];

    let count;

    if (stage === 6) {
        // 보스
        enemies.push({
            x: W / 2,
            y: 100,

            radius: 55,

            hp: 1500,
            maxHp: 1500,

            speed: 1.2,

            damage: 15,

            boss: true
        });

        count = 0;

    } else {

        count = 5 + stage * 3;

        for (let i = 0; i < count; i++) {

            let type = Math.random();

            let enemy;

            if (type < 0.7) {

                enemy = {
                    x: Math.random() * (W - 100) + 50,
                    y: Math.random() * (H - 100) + 50,

                    radius: 15,

                    hp: 30 + stage * 10,
                    maxHp: 30 + stage * 10,

                    speed: 1 + stage * 0.1,

                    damage: 5 + stage,

                    boss: false
                };

            } else {

                enemy = {
                    x: Math.random() * (W - 100) + 50,
                    y: Math.random() * (H - 100) + 50,

                    radius: 22,

                    hp: 70 + stage * 15,
                    maxHp: 70 + stage * 15,

                    speed: 0.6 + stage * 0.08,

                    damage: 10 + stage * 2,

                    boss: false
                };

            }

            enemies.push(enemy);
        }
    }

    updateUI();
}


/* =========================
   플레이어 이동
========================= */

function updatePlayer() {

    let dx = 0;
    let dy = 0;

    if (keys["w"]) dy--;
    if (keys["s"]) dy++;
    if (keys["a"]) dx--;
    if (keys["d"]) dx++;

    if (dx !== 0 || dy !== 0) {

        let length = Math.sqrt(dx * dx + dy * dy);

        dx /= length;
        dy /= length;

        player.x += dx * player.moveSpeed;
        player.y += dy * player.moveSpeed;
    }

    player.x = Math.max(player.radius, Math.min(W - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(H - player.radius, player.y));
}


/* =========================
   공격
========================= */

function shoot() {

    if (player.attackCooldown > 0) return;

    let dx = mouse.x - player.x;
    let dy = mouse.y - player.y;

    let length = Math.sqrt(dx * dx + dy * dy);

    dx /= length;
    dy /= length;

    let critical = Math.random() * 100 < player.crit;

    let damage = player.atk;

    if (critical) {
        damage *= player.critDmg / 100;
    }

    bullets.push({

        x: player.x,
        y: player.y,

        vx: dx * 9,
        vy: dy * 9,

        damage: damage,

        critical: critical,

        radius: 5
    });

    player.attackCooldown = 30 / player.attackSpeed;
}


/* =========================
   총알
========================= */

function updateBullets() {

    for (let i = bullets.length - 1; i >= 0; i--) {

        let b = bullets[i];

        b.x += b.vx;
        b.y += b.vy;

        if (
            b.x < 0 ||
            b.x > W ||
            b.y < 0 ||
            b.y > H
        ) {
            bullets.splice(i, 1);
            continue;
        }

        for (let j = enemies.length - 1; j >= 0; j--) {

            let e = enemies[j];

            let dx = b.x - e.x;
            let dy = b.y - e.y;

            let dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < b.radius + e.radius) {

                e.hp -= b.damage;

                bullets.splice(i, 1);

                if (e.hp <= 0) {

                    let reward = e.boss ? 500 : 10 + stage * 2;

                    pt += reward;

                    kills++;

                    enemies.splice(j, 1);
                }

                break;
            }
        }
    }
}


/* =========================
   적 AI
========================= */

function updateEnemies() {

    for (let e of enemies) {

        let dx = player.x - e.x;
        let dy = player.y - e.y;

        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > player.radius + e.radius) {

            e.x += dx / dist * e.speed;
            e.y += dy / dist * e.speed;

        } else {

            player.hp -= e.damage * 0.02;

            if (player.hp <= 0) {

                player.hp = 0;

                gameOver();
            }
        }
    }
}


/* =========================
   게임 업데이트
========================= */

function update() {

    if (!gameRunning) return;

    updatePlayer();

    if (mouse.down) {
        shoot();
    }

    if (player.attackCooldown > 0) {
        player.attackCooldown--;
    }

    updateBullets();
    updateEnemies();

    if (enemies.length === 0) {
        stageClear();
    }

    updateUI();
}


/* =========================
   스테이지 클리어
========================= */

let stageCleared = false;

function stageClear() {

    if (stageCleared) return;

    stageCleared = true;

    gameRunning = false;

    if (stage >= 6) {

        victory();

    } else {

        document.getElementById("upgrade").style.display = "flex";
    }
}


function nextStage() {

    stage++;

    stageCleared = false;

    gameRunning = true;

    player.hp = player.maxHp;

    document.getElementById("upgrade").style.display = "none";

    spawnStage();
}


/* =========================
   업그레이드
========================= */

function upgradeStat(stat) {

    let cost = 0;

    if (stat === "atk") {

        cost = 50;

        if (pt >= cost) {
            pt -= cost;
            player.atk += 5;
        }

    }

    else if (stat === "speed") {

        cost = 70;

        if (pt >= cost) {
            pt -= cost;
            player.attackSpeed += 0.1;
        }

    }

    else if (stat === "crit") {

        cost = 80;

        if (pt >= cost) {
            pt -= cost;
            player.crit += 5;
        }

    }

    else if (stat === "critDmg") {

        cost = 100;

        if (pt >= cost) {
            pt -= cost;
            player.critDmg += 25;
        }
    }

    updateUI();
}


/* =========================
   UI
========================= */

function updateUI() {

    document.getElementById("hp").textContent =
        Math.ceil(player.hp);

    document.getElementById("atk").textContent =
        player.atk;

    document.getElementById("speed").textContent =
        player.attackSpeed.toFixed(1);

    document.getElementById("crit").textContent =
        player.crit;

    document.getElementById("critDmg").textContent =
        player.critDmg;

    document.getElementById("pt").textContent =
        pt;

    document.getElementById("stage").textContent =
        stage;

    document.getElementById("enemyCount").textContent =
        enemies.length;
}


/* =========================
   게임 오버
========================= */

function gameOver() {

    gameRunning = false;

    document.getElementById("message").style.display = "flex";

    document.getElementById("messageTitle").textContent =
        "GAME OVER";

    document.getElementById("messageText").innerHTML =
        `획득 PT: ${pt}<br>처치한 적: ${kills}`;
}


/* =========================
   게임 클리어
========================= */

function victory() {

    gameRunning = false;

    document.getElementById("message").style.display = "flex";

    document.getElementById("messageTitle").textContent =
        "🏆 ALL STAGES CLEAR!";

    document.getElementById("messageText").innerHTML =
        `
        최종 점수: <strong>${pt} PT</strong><br>
        처치한 적: ${kills}<br><br>

        최종 능력치<br>
        공격력: ${player.atk}<br>
        공격속도: ${player.attackSpeed.toFixed(1)}<br>
        치명타 확률: ${player.crit}%<br>
        치명타 피해: ${player.critDmg}%
        `;
}


/* =========================
   렌더링
========================= */

function draw() {

    ctx.clearRect(0, 0, W, H);

    // 배경
    ctx.fillStyle = "#181818";
    ctx.fillRect(0, 0, W, H);


    // 플레이어
    ctx.beginPath();

    ctx.arc(
        player.x,
        player.y,
        player.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#4da6ff";
    ctx.fill();


    // 총알
    for (let b of bullets) {

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            b.critical ? "#ffff00" : "#ffffff";

        ctx.fill();
    }


    // 적
    for (let e of enemies) {

        ctx.beginPath();

        ctx.arc(
            e.x,
            e.y,
            e.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            e.boss ? "#9b35ff" : "#e74c3c";

        ctx.fill();


        // HP bar
        let barWidth = e.radius * 2;

        ctx.fillStyle = "#333";

        ctx.fillRect(
            e.x - barWidth / 2,
            e.y - e.radius - 10,
            barWidth,
            5
        );

        ctx.fillStyle = "#2ecc71";

        ctx.fillRect(
            e.x - barWidth / 2,
            e.y - e.radius - 10,
            barWidth * (e.hp / e.maxHp),
            5
        );
    }


    // 스테이지 표시
    ctx.fillStyle = "white";

    ctx.font = "24px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        `STAGE ${stage}`,
        W / 2,
        35
    );
}


/* =========================
   게임 루프
========================= */

function loop() {

    update();

    draw();

    requestAnimationFrame(loop);
}


spawnStage();

loop();

</script>

</body>
</html>
