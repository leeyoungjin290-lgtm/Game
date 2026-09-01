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
    overflow: hidden;
    font-family: Arial, sans-serif;
    color: white;
}

canvas {
    display: block;
    margin: auto;
    background: #222;
}

#ui {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 10;
    font-size: 17px;
    line-height: 1.6;
    text-shadow: 1px 1px 3px black;
}

#stageText {
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 25px;
    font-weight: bold;
    z-index: 10;
}

#upgrade {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.8);
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    z-index: 20;
}

#upgrade h1 {
    font-size: 40px;
}

.upgradeButton {
    width: 280px;
    padding: 13px;
    margin: 5px;
    font-size: 17px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

#result {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.85);
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    z-index: 30;
}

#result h1 {
    font-size: 50px;
}

#result button {
    padding: 14px 30px;
    font-size: 18px;
}
</style>
</head>

<body>

<canvas id="game" width="1000" height="650"></canvas>

<div id="stageText">
    STAGE 1
</div>

<div id="ui">
    ❤️ HP: <span id="hp">100</span> / 100<br>
    ⚔️ 공격력: <span id="atk">10</span><br>
    ⚡ 공격속도: <span id="attackSpeed">1.0</span><br>
    🎯 치명타 확률: <span id="crit">5</span>%<br>
    💥 치명타 피해: <span id="critDamage">150</span>%<br>
    💰 PT: <span id="pt">0</span><br>
    👾 남은 적: <span id="enemyCount">0</span>
</div>


<!-- 업그레이드 화면 -->

<div id="upgrade">

    <h1>STAGE CLEAR!</h1>

    <p>
        PT를 사용해서 능력을 강화하세요.
    </p>

    <p>
        현재 PT:
        <strong id="upgradePT">0</strong>
    </p>

    <button class="upgradeButton"
            onclick="upgrade('atk')">
        공격력 +5
        <br>
        50 PT
    </button>

    <button class="upgradeButton"
            onclick="upgrade('attackSpeed')">
        공격속도 +10%
        <br>
        70 PT
    </button>

    <button class="upgradeButton"
            onclick="upgrade('crit')">
        치명타 확률 +5%
        <br>
        80 PT
    </button>

    <button class="upgradeButton"
            onclick="upgrade('critDamage')">
        치명타 피해 +25%
        <br>
        100 PT
    </button>

    <button class="upgradeButton"
            onclick="nextStage()">
        다음 스테이지
    </button>

</div>


<!-- 결과 화면 -->

<div id="result">

    <h1 id="resultTitle">
        GAME OVER
    </h1>

    <p id="resultText"></p>

    <button onclick="location.reload()">
        다시 시작
    </button>

</div>


<script>

/* =====================================================
   이미지
===================================================== */

const images = {};

const imageFiles = {
    player: "player.png",
    enemyNormal: "enemy_normal.png",
    enemyTank: "enemy_tank.png",
    boss: "boss.png",
    background: "background.png",
    bullet: "bullet.png",
    hitEffect: "hit_effect.png"
};


for (const key in imageFiles) {

    const img = new Image();

    img.src = imageFiles[key];

    images[key] = img;
}


/* =====================================================
   Canvas
===================================================== */

const canvas = document.getElementById("game");

const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;


/* =====================================================
   키보드 / 마우스
===================================================== */

const keys = {};

const mouse = {
    x: WIDTH / 2,
    y: HEIGHT / 2,
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

    mouse.x =
        (e.clientX - rect.left)
        * WIDTH / rect.width;

    mouse.y =
        (e.clientY - rect.top)
        * HEIGHT / rect.height;

});


canvas.addEventListener("mousedown", () => {

    mouse.down = true;

});


canvas.addEventListener("mouseup", () => {

    mouse.down = false;

});


/* =====================================================
   게임 변수
===================================================== */

let stage = 1;

let pt = 0;

let kills = 0;

let gameRunning = true;

let stageCleared = false;


/* =====================================================
   플레이어
===================================================== */

const player = {

    x: WIDTH / 2,
    y: HEIGHT / 2,

    width: 55,
    height: 55,

    hp: 100,
    maxHp: 100,

    atk: 10,

    attackSpeed: 1.0,

    crit: 5,

    critDamage: 150,

    moveSpeed: 4,

    cooldown: 0

};


/* =====================================================
   배열
===================================================== */

let enemies = [];

let bullets = [];

let effects = [];


/* =====================================================
   적 생성
===================================================== */

function spawnStage() {

    enemies = [];

    bullets = [];

    effects = [];

    stageCleared = false;

    if (stage === 6) {

        spawnBoss();

        return;

    }


    const enemyCount = 5 + stage * 3;


    for (let i = 0; i < enemyCount; i++) {

        let tank = Math.random() < 0.25;


        let enemy = {

            type: tank ? "tank" : "normal",

            x: Math.random() * (WIDTH - 100) + 50,

            y: Math.random() * (HEIGHT - 100) + 50,

            width: tank ? 65 : 45,

            height: tank ? 65 : 45,

            hp:
                tank
                ? 70 + stage * 15
                : 30 + stage * 10,

            maxHp:
                tank
                ? 70 + stage * 15
                : 30 + stage * 10,

            speed:
                tank
                ? 0.6 + stage * 0.05
                : 1.0 + stage * 0.1,

            damage:
                tank
                ? 12 + stage * 2
                : 5 + stage,

            attackCooldown: 0

        };


        enemies.push(enemy);

    }

}


/* =====================================================
   보스
===================================================== */

function spawnBoss() {

    enemies.push({

        type: "boss",

        x: WIDTH / 2,

        y: 130,

        width: 120,

        height: 120,

        hp: 1500,

        maxHp: 1500,

        speed: 0.7,

        damage: 20,

        attackCooldown: 0

    });

}


/* =====================================================
   플레이어 이동
===================================================== */

function updatePlayer() {

    let dx = 0;

    let dy = 0;


    if (keys["w"]) dy -= 1;

    if (keys["s"]) dy += 1;

    if (keys["a"]) dx -= 1;

    if (keys["d"]) dx += 1;


    if (dx !== 0 || dy !== 0) {

        const length =
            Math.sqrt(dx * dx + dy * dy);

        dx /= length;

        dy /= length;


        player.x +=
            dx * player.moveSpeed;

        player.y +=
            dy * player.moveSpeed;

    }


    player.x =
        Math.max(
            player.width / 2,
            Math.min(
                WIDTH - player.width / 2,
                player.x
            )
        );


    player.y =
        Math.max(
            player.height / 2,
            Math.min(
                HEIGHT - player.height / 2,
                player.y
            )
        );

}


/* =====================================================
   공격
===================================================== */

function shoot() {

    if (player.cooldown > 0) return;


    let dx = mouse.x - player.x;

    let dy = mouse.y - player.y;


    const distance =
        Math.sqrt(dx * dx + dy * dy);


    if (distance === 0) return;


    dx /= distance;

    dy /= distance;


    const critical =
        Math.random() * 100 < player.crit;


    let damage = player.atk;


    if (critical) {

        damage *=
            player.critDamage / 100;

    }


    bullets.push({

        x: player.x,

        y: player.y,

        vx: dx * 9,

        vy: dy * 9,

        damage: damage,

        critical: critical,

        width: 20,

        height: 20

    });


    player.cooldown =
        30 / player.attackSpeed;

}


/* =====================================================
   총알 업데이트
===================================================== */

function updateBullets() {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        const bullet = bullets[i];


        bullet.x += bullet.vx;

        bullet.y += bullet.vy;


        if (
            bullet.x < -30 ||
            bullet.x > WIDTH + 30 ||
            bullet.y < -30 ||
            bullet.y > HEIGHT + 30
        ) {

            bullets.splice(i, 1);

            continue;

        }


        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {

            const enemy = enemies[j];


            const dx =
                bullet.x - enemy.x;

            const dy =
                bullet.y - enemy.y;


            const distance =
                Math.sqrt(dx * dx + dy * dy);


            if (
                distance <
                enemy.width / 2 + 10
            ) {

                enemy.hp -= bullet.damage;


                effects.push({

                    x: enemy.x,

                    y: enemy.y,

                    timer: 10

                });


                bullets.splice(i, 1);


                if (enemy.hp <= 0) {

                    killEnemy(enemy, j);

                }


                break;

            }

        }

    }

}


/* =====================================================
   적 처치
===================================================== */

function killEnemy(enemy, index) {

    let reward;


    if (enemy.type === "boss") {

        reward = 500;

    }

    else if (enemy.type === "tank") {

        reward = 25 + stage * 3;

    }

    else {

        reward = 10 + stage * 2;

    }


    pt += reward;

    kills++;


    enemies.splice(index, 1);

}


/* =====================================================
   적 AI
===================================================== */

function updateEnemies() {

    for (const enemy of enemies) {

        const dx =
            player.x - enemy.x;

        const dy =
            player.y - enemy.y;


        const distance =
            Math.sqrt(dx * dx + dy * dy);


        if (
            distance >
            player.width / 2 +
            enemy.width / 2
        ) {

            enemy.x +=
                dx / distance *
                enemy.speed;

            enemy.y +=
                dy / distance *
                enemy.speed;

        }

        else {

            if (enemy.attackCooldown <= 0) {

                player.hp -= enemy.damage;

                enemy.attackCooldown = 60;

            }

        }


        if (enemy.attackCooldown > 0) {

            enemy.attackCooldown--;

        }

    }


    if (player.hp <= 0) {

        player.hp = 0;

        gameOver();

    }

}


/* =====================================================
   업그레이드
===================================================== */

function upgrade(stat) {

    let cost = 0;


    if (stat === "atk") {

        cost = 50;


        if (pt >= cost) {

            pt -= cost;

            player.atk += 5;

        }

    }


    if (stat === "attackSpeed") {

        cost = 70;


        if (pt >= cost) {

            pt -= cost;

            player.attackSpeed += 0.1;

        }

    }


    if (stat === "crit") {

        cost = 80;


        if (pt >= cost) {

            pt -= cost;

            player.crit += 5;

        }

    }


    if (stat === "critDamage") {

        cost = 100;


        if (pt >= cost) {

            pt -= cost;

            player.critDamage += 25;

        }

    }


    updateUI();

}


/* =====================================================
   다음 스테이지
===================================================== */

function nextStage() {

    stage++;


    player.hp = player.maxHp;


    gameRunning = true;

    stageCleared = false;


    document.getElementById("upgrade")
        .style.display = "none";


    document.getElementById("stageText")
        .textContent =
        `STAGE ${stage}`;


    spawnStage();

}


/* =====================================================
   스테이지 클리어
===================================================== */

function checkStageClear() {

    if (
        enemies.length === 0 &&
        !stageCleared
    ) {

        stageCleared = true;


        if (stage === 6) {

            victory();

        }

        else {

            gameRunning = false;

            document.getElementById("upgrade")
                .style.display = "flex";

            document.getElementById("upgradePT")
                .textContent = pt;

        }

    }

}


/* =====================================================
   게임 오버
===================================================== */

function gameOver() {

    gameRunning = false;


    document.getElementById("result")
        .style.display = "flex";


    document.getElementById("resultTitle")
        .textContent =
        "GAME OVER";


    document.getElementById("resultText")
        .innerHTML =
        `
        최종 PT: ${pt}<br>
        처치한 적: ${kills}<br>
        도달 스테이지: ${stage}
        `;

}


/* =====================================================
   게임 클리어
===================================================== */

function victory() {

    gameRunning = false;


    document.getElementById("result")
        .style.display = "flex";


    document.getElementById("resultTitle")
        .textContent =
        "🏆 ALL STAGES CLEAR!";


    document.getElementById("resultText")
        .innerHTML =
        `
        최종 점수: <strong>${pt} PT</strong><br>
        총 처치 수: ${kills}<br><br>

        공격력: ${player.atk}<br>
        공격속도: ${player.attackSpeed.toFixed(1)}<br>
        치명타 확률: ${player.crit}%<br>
        치명타 피해: ${player.critDamage}%
        `;

}


/* =====================================================
   UI
===================================================== */

function updateUI() {

    document.getElementById("hp")
        .textContent =
        Math.ceil(player.hp);


    document.getElementById("atk")
        .textContent =
        player.atk;


    document.getElementById("attackSpeed")
        .textContent =
        player.attackSpeed.toFixed(1);


    document.getElementById("crit")
        .textContent =
        player.crit;


    document.getElementById("critDamage")
        .textContent =
        player.critDamage;


    document.getElementById("pt")
        .textContent =
        pt;


    document.getElementById("enemyCount")
        .textContent =
        enemies.length;


    document.getElementById("upgradePT")
        .textContent =
        pt;

}


/* =====================================================
   이미지 그리기
===================================================== */

function drawImageCentered(
    image,
    x,
    y,
    width,
    height
) {

    if (!image.complete) return;


    ctx.drawImage(
        image,
        x - width / 2,
        y - height / 2,
        width,
        height
    );

}


/* =====================================================
   렌더링
===================================================== */

function draw() {

    ctx.clearRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    /* 배경 */

    if (images.background.complete) {

        ctx.drawImage(
            images.background,
            0,
            0,
            WIDTH,
            HEIGHT
        );

    }

    else {

        ctx.fillStyle = "#222";

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

    }


    /* 총알 */

    for (const bullet of bullets) {

        if (images.bullet.complete) {

            const angle =
                Math.atan2(
                    bullet.vy,
                    bullet.vx
                );


            ctx.save();


            ctx.translate(
                bullet.x,
                bullet.y
            );


            ctx.rotate(angle);


            ctx.drawImage(
                images.bullet,
                -bullet.width / 2,
                -bullet.height / 2,
                bullet.width,
                bullet.height
            );


            ctx.restore();

        }

    }


    /* 적 */

    for (const enemy of enemies) {

        let image;


        if (enemy.type === "boss") {

            image = images.boss;

        }

        else if (enemy.type === "tank") {

            image = images.enemyTank;

        }

        else {

            image = images.enemyNormal;

        }


        drawImageCentered(
            image,
            enemy.x,
            enemy.y,
            enemy.width,
            enemy.height
        );


        /* HP바 */

        const barWidth =
            enemy.width;


        ctx.fillStyle = "#333";


        ctx.fillRect(
            enemy.x - barWidth / 2,
            enemy.y - enemy.height / 2 - 10,
            barWidth,
            6
        );


        ctx.fillStyle = "#32d15b";


        ctx.fillRect(
            enemy.x - barWidth / 2,
            enemy.y - enemy.height / 2 - 10,
            barWidth *
            Math.max(
                0,
                enemy.hp / enemy.maxHp
            ),
            6
        );

    }


    /* 플레이어 */

    drawImageCentered(
        images.player,
        player.x,
        player.y,
        player.width,
        player.height
    );


    /* 공격 효과 */

    for (
        let i = effects.length - 1;
        i >= 0;
        i--
    ) {

        const effect = effects[i];


        if (images.hitEffect.complete) {

            ctx.globalAlpha =
                effect.timer / 10;


            ctx.drawImage(
                images.hitEffect,
                effect.x - 25,
                effect.y - 25,
                50,
                50
            );


            ctx.globalAlpha = 1;

        }


        effect.timer--;


        if (effect.timer <= 0) {

            effects.splice(i, 1);

        }

    }

}


/* =====================================================
   게임 업데이트
===================================================== */

function update() {

    if (!gameRunning) return;


    updatePlayer();


    if (mouse.down) {

        shoot();

    }


    if (player.cooldown > 0) {

        player.cooldown--;

    }


    updateBullets();

    updateEnemies();

    checkStageClear();

    updateUI();

}


/* =====================================================
   게임 루프
===================================================== */

function gameLoop() {

    update();

    draw();

    requestAnimationFrame(gameLoop);

}


/* =====================================================
   시작
===================================================== */

spawnStage();

updateUI();

gameLoop();

</script>

</body>
</html>#message {
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
