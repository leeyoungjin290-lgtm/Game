import streamlit as st
import streamlit.components.v1 as components
import base64
import os


st.set_page_config(
    page_title="PT Survival",
    page_icon="🎮",
    layout="wide"
)


# =========================================================
# 이미지 불러오기
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_image(filename):
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return ""

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    return "data:image/png;base64," + data


images = {
    "player": load_image("player.png"),
    "enemyNormal": load_image("enemy_normal.png"),
    "enemyTank": load_image("enemy_tank.png"),
    "boss": load_image("boss.png"),
    "bossAttack": load_image("boss_attack.png"),
    "background": load_image("background.png"),
    "bullet": load_image("bullet.png"),
    "hitEffect": load_image("hit_effect.png")
}


# =========================================================
# HTML / CSS / JavaScript
# =========================================================

html = """
<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #111;
    font-family: Arial, sans-serif;
}

#gameContainer {
    position: relative;
    width: 1000px;
    height: 700px;
    margin: 0 auto;
    overflow: hidden;
    background: #111;
}

canvas {
    display: block;
    width: 1000px;
    height: 700px;
    background: #222;
    cursor: crosshair;
}

#ui {
    position: absolute;
    left: 20px;
    top: 15px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    z-index: 10;
    pointer-events: none;
    text-shadow: 2px 2px 4px black;
}

#stageText {
    position: absolute;
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 26px;
    font-weight: bold;
    z-index: 10;
    pointer-events: none;
    text-shadow: 2px 2px 4px black;
}

#bossBarContainer {
    position: absolute;
    top: 55px;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 24px;
    border: 2px solid white;
    background: #222;
    display: none;
    z-index: 10;
}

#bossBar {
    width: 100%;
    height: 100%;
    background: red;
}

#message {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    z-index: 20;
    display: none;
    text-shadow: 3px 3px 5px black;
}

#upgradeScreen {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.85);
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 30;
    color: white;
}

#upgradeScreen h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

#upgradePT {
    font-size: 24px;
    margin-bottom: 25px;
}

.upgradeButton {
    width: 330px;
    padding: 15px;
    margin: 7px;
    border: 2px solid white;
    background: #222;
    color: white;
    font-size: 19px;
    cursor: pointer;
}

.upgradeButton:hover {
    background: #444;
}

#startScreen {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.85);
    z-index: 40;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

#startScreen h1 {
    font-size: 60px;
    margin: 0 0 20px 0;
}

#startScreen p {
    font-size: 20px;
}

#startButton {
    margin-top: 25px;
    padding: 15px 50px;
    font-size: 25px;
    background: white;
    border: none;
    cursor: pointer;
}

#gameOverScreen {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.88);
    z-index: 50;
    color: white;
    display: none;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

#gameOverScreen h1 {
    font-size: 50px;
}

#restartButton {
    padding: 15px 45px;
    font-size: 22px;
    cursor: pointer;
}

</style>

</head>


<body>

<div id="gameContainer">

<canvas id="gameCanvas" width="1000" height="700"></canvas>

<div id="ui">
    HP: <span id="hp">100</span><br>
    PT: <span id="pt">0</span><br>
    공격력: <span id="attack">10</span><br>
    치명타: <span id="crit">10</span>%
</div>

<div id="stageText">
    STAGE <span id="stage">1</span>
</div>

<div id="bossBarContainer">
    <div id="bossBar"></div>
</div>

<div id="message"></div>


<div id="startScreen">

    <h1>PT SURVIVAL</h1>

    <p>WASD / 방향키로 이동</p>
    <p>마우스 방향으로 자동 공격</p>

    <button id="startButton">
        GAME START
    </button>

</div>


<div id="upgradeScreen">

    <h1>STAGE CLEAR</h1>

    <div id="upgradePT">
        보유 PT: <span id="upgradePTValue">0</span>
    </div>

    <button class="upgradeButton" id="attackUpgrade">
        공격력 +5
    </button>

    <button class="upgradeButton" id="speedUpgrade">
        공격속도 증가
    </button>

    <button class="upgradeButton" id="critUpgrade">
        치명타 +5%
    </button>

    <button class="upgradeButton" id="hpUpgrade">
        최대 HP +20
    </button>

    <button class="upgradeButton" id="nextStageButton">
        다음 스테이지
    </button>

</div>


<div id="gameOverScreen">

    <h1 id="gameOverTitle">
        GAME OVER
    </h1>

    <p style="font-size:25px;">
        총 획득 PT: <span id="finalPT">0</span>
    </p>

    <button id="restartButton">
        다시 시작
    </button>

</div>


</div>


<script>


// =========================================================
// 이미지
// =========================================================

const images = {

    player: "__PLAYER__",
    enemyNormal: "__ENEMY_NORMAL__",
    enemyTank: "__ENEMY_TANK__",
    boss: "__BOSS__",
    bossAttack: "__BOSS_ATTACK__",
    background: "__BACKGROUND__",
    bullet: "__BULLET__",
    hitEffect: "__HIT_EFFECT__"

};


function createImage(src) {

    const img = new Image();

    if (src) {
        img.src = src;
    }

    return img;

}


const img = {

    player: createImage(images.player),
    enemyNormal: createImage(images.enemyNormal),
    enemyTank: createImage(images.enemyTank),
    boss: createImage(images.boss),
    bossAttack: createImage(images.bossAttack),
    background: createImage(images.background),
    bullet: createImage(images.bullet),
    hitEffect: createImage(images.hitEffect)

};


// =========================================================
// Canvas
// =========================================================

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;


// =========================================================
// 게임 변수
// =========================================================

let gameRunning = false;

let stage = 1;

let stageTime = 0;

const stageLimits = [
    20,
    22,
    24,
    27,
    30
];


let stagePT = 0;

let totalEarnedPT = 0;


// =========================================================
// 플레이어
// =========================================================

const player = {

    x: WIDTH / 2,
    y: HEIGHT / 2,

    radius: 28,

    speed: 260,

    hp: 100,
    maxHp: 100,

    attack: 10,

    attackSpeed: 0.35,

    crit: 0.10,

    shootTimer: 0

};


// =========================================================
// 게임 객체
// =========================================================

let enemies = [];

let bullets = [];

let bossProjectiles = [];

let hitEffects = [];

let boss = null;

let bossSpawned = false;

let bossAttackTimer = 1.0;

let bossAttackRotation = 0;


// =========================================================
// 키 입력
// =========================================================

const keys = {};

document.addEventListener("keydown", function(e) {

    keys[e.key.toLowerCase()] = true;

});


document.addEventListener("keyup", function(e) {

    keys[e.key.toLowerCase()] = false;

});


// =========================================================
// 마우스
// =========================================================

let mouse = {

    x: WIDTH / 2,
    y: HEIGHT / 2

};


canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    mouse.x =
        (e.clientX - rect.left)
        * WIDTH / rect.width;

    mouse.y =
        (e.clientY - rect.top)
        * HEIGHT / rect.height;

});


// =========================================================
// 유틸
// =========================================================

function distance(a, b) {

    return Math.hypot(
        a.x - b.x,
        a.y - b.y
    );

}


function random(min, max) {

    return Math.random() * (max - min) + min;

}


// =========================================================
// 적 생성
// =========================================================

function spawnEnemy() {

    const side = Math.floor(Math.random() * 4);

    let x;
    let y;


    if (side === 0) {

        x = random(0, WIDTH);
        y = -50;

    }

    else if (side === 1) {

        x = WIDTH + 50;
        y = random(0, HEIGHT);

    }

    else if (side === 2) {

        x = random(0, WIDTH);
        y = HEIGHT + 50;

    }

    else {

        x = -50;
        y = random(0, HEIGHT);

    }


    const tankChance = Math.min(0.1 + stage * 0.04, 0.35);

    const isTank = Math.random() < tankChance;


    if (isTank) {

        enemies.push({

            type: "tank",

            x: x,
            y: y,

            radius: 32,

            hp: 50 + stage * 15,

            maxHp: 50 + stage * 15,

            speed: 45 + stage * 4,

            damage: 15

        });

    }

    else {

        enemies.push({

            type: "normal",

            x: x,
            y: y,

            radius: 25,

            hp: 20 + stage * 5,

            maxHp: 20 + stage * 5,

            speed: 80 + stage * 5,

            damage: 8

        });

    }

}


// =========================================================
// 총알 발사
// =========================================================

function shoot() {

    const dx = mouse.x - player.x;
    const dy = mouse.y - player.y;

    const len = Math.hypot(dx, dy) || 1;


    let damage = player.attack;

    let critical = false;


    if (Math.random() < player.crit) {

        damage *= 2;

        critical = true;

    }


    bullets.push({

        x: player.x,
        y: player.y,

        vx: dx / len * 650,
        vy: dy / len * 650,

        radius: 8,

        damage: damage,

        critical: critical,

        life: 2

    });

}


// =========================================================
// 보스 공격
// =========================================================

function bossShoot() {

    if (!boss) return;


    /*
        동서남북 4방향

        처음:
              ↑

           ←  B  →

              ↓


        다음 공격부터 시계 방향으로 회전
    */


    const directions = [

        { x: 0, y: -1 },

        { x: 1, y: 0 },

        { x: 0, y: 1 },

        { x: -1, y: 0 }

    ];


    for (const direction of directions) {

        const angle =
            Math.atan2(direction.y, direction.x)
            + bossAttackRotation;


        bossProjectiles.push({

            x: boss.x,
            y: boss.y,

            vx: Math.cos(angle) * 240,
            vy: Math.sin(angle) * 240,

            radius: 20,

            damage: boss.damage,

            life: 5

        });

    }


    /*
        다음 공격에서는
        시계 방향으로 45도 회전
    */

    bossAttackRotation += Math.PI / 4;


    if (bossAttackRotation >= Math.PI * 2) {

        bossAttackRotation -= Math.PI * 2;

    }


    boss.attackFlash = 0.2;

}


// =========================================================
// 적 업데이트
// =========================================================

function updateEnemies(dt) {


    for (let i = enemies.length - 1; i >= 0; i--) {

        const enemy = enemies[i];


        const dx = player.x - enemy.x;
        const dy = player.y - enemy.y;

        const len = Math.hypot(dx, dy) || 1;


        enemy.x += dx / len * enemy.speed * dt;
        enemy.y += dy / len * enemy.speed * dt;


        if (
            distance(enemy, player)
            < enemy.radius + player.radius
        ) {

            player.hp -= enemy.damage * dt;

            addHitEffect(
                player.x,
                player.y,
                50
            );

        }

    }


    // 보스 이동
    if (boss) {

        const dx = player.x - boss.x;
        const dy = player.y - boss.y;

        const len = Math.hypot(dx, dy) || 1;


        boss.x += dx / len * boss.speed * dt;
        boss.y += dy / len * boss.speed * dt;


        if (
            distance(boss, player)
            < boss.radius + player.radius
        ) {

            player.hp -= boss.damage * dt;

            addHitEffect(
                player.x,
                player.y,
                70
            );

        }

    }

}


// =========================================================
// 총알 업데이트
// =========================================================

function updateBullets(dt) {


    for (let i = bullets.length - 1; i >= 0; i--) {

        const bullet = bullets[i];


        bullet.x += bullet.vx * dt;
        bullet.y += bullet.vy * dt;

        bullet.life -= dt;


        let removed = false;


        // 적 충돌

        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {

            const enemy = enemies[j];


            if (
                distance(bullet, enemy)
                < bullet.radius + enemy.radius
            ) {

                enemy.hp -= bullet.damage;


                addHitEffect(
                    enemy.x,
                    enemy.y,
                    50
                );


                bullets.splice(i, 1);

                removed = true;


                if (enemy.hp <= 0) {

                    killEnemy(j);

                }


                break;

            }

        }


        if (removed) continue;


        // 보스 충돌

        if (boss) {

            if (
                distance(bullet, boss)
                < bullet.radius + boss.radius
            ) {

                boss.hp -= bullet.damage;


                addHitEffect(
                    boss.x,
                    boss.y,
                    80
                );


                bullets.splice(i, 1);


                if (boss.hp <= 0) {

                    killBoss();

                }


                continue;

            }

        }


        if (
            bullet.life <= 0 ||
            bullet.x < -100 ||
            bullet.x > WIDTH + 100 ||
            bullet.y < -100 ||
            bullet.y > HEIGHT + 100
        ) {

            bullets.splice(i, 1);

        }

    }

}


// =========================================================
// 보스 탄환 업데이트
// =========================================================

function updateBossProjectiles(dt) {


    for (
        let i = bossProjectiles.length - 1;
        i >= 0;
        i--
    ) {

        const projectile =
            bossProjectiles[i];


        projectile.x +=
            projectile.vx * dt;

        projectile.y +=
            projectile.vy * dt;


        projectile.life -= dt;


        // 플레이어 충돌

        if (
            distance(projectile, player)
            <
            projectile.radius + player.radius
        ) {

            player.hp -= projectile.damage;


            addHitEffect(
                player.x,
                player.y,
                80
            );


            bossProjectiles.splice(i, 1);

            continue;

        }


        if (
            projectile.life <= 0 ||
            projectile.x < -100 ||
            projectile.x > WIDTH + 100 ||
            projectile.y < -100 ||
            projectile.y > HEIGHT + 100
        ) {

            bossProjectiles.splice(i, 1);

        }

    }

}


// =========================================================
// 적 처치
// =========================================================

function killEnemy(index) {

    const enemy = enemies[index];


    let reward;


    if (enemy.type === "tank") {

        reward = 5;

    }

    else {

        reward = 2;

    }


    stagePT += reward;

    totalEarnedPT += reward;


    enemies.splice(index, 1);

}


// =========================================================
// 보스 처치
// =========================================================

function killBoss() {

    if (!boss) return;


    addHitEffect(
        boss.x,
        boss.y,
        150
    );


    boss = null;

    bossSpawned = false;

    bossProjectiles = [];


    setTimeout(function() {

        finalGame();

    }, 1000);

}


// =========================================================
// 히트 이펙트
// =========================================================

function addHitEffect(x, y, size) {

    hitEffects.push({

        x: x,
        y: y,

        size: size,

        life: 0.3,

        maxLife: 0.3

    });

}


// =========================================================
// 히트 이펙트 업데이트
// =========================================================

function updateHitEffects(dt) {

    for (
        let i = hitEffects.length - 1;
        i >= 0;
        i--
    ) {

        hitEffects[i].life -= dt;


        if (hitEffects[i].life <= 0) {

            hitEffects.splice(i, 1);

        }

    }

}


// =========================================================
// 플레이어 이동
// =========================================================

function updatePlayer(dt) {

    let dx = 0;
    let dy = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {

        dy -= 1;

    }


    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {

        dy += 1;

    }


    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {

        dx -= 1;

    }


    if (
        keys["d"] ||
        keys["arrowright"]
    ) {

        dx += 1;

    }


    const len = Math.hypot(dx, dy);


    if (len > 0) {

        dx /= len;
        dy /= len;


        player.x +=
            dx * player.speed * dt;

        player.y +=
            dy * player.speed * dt;

    }


    player.x = Math.max(
        player.radius,
        Math.min(
            WIDTH - player.radius,
            player.x
        )
    );


    player.y = Math.max(
        player.radius,
        Math.min(
            HEIGHT - player.radius,
            player.y
        )
    );


    // 자동 공격

    player.shootTimer -= dt;


    if (player.shootTimer <= 0) {

        shoot();

        player.shootTimer =
            player.attackSpeed;

    }

}


// =========================================================
// 보스 생성
// =========================================================

function spawnBoss() {

    boss = {

        x: WIDTH / 2,

        y: 130,

        radius: 65,

        hp: 1500,

        maxHp: 1500,

        speed: 35,

        damage: 20,

        attackFlash: 0

    };


    bossSpawned = true;


    // 보스 등장 직후 공격
    bossAttackTimer = 0.5;

    bossAttackRotation = 0;


    document
        .getElementById("bossBarContainer")
        .style.display = "block";

}


// =========================================================
// 스테이지 업데이트
// =========================================================

function updateStage(dt) {


    // 1~5 스테이지

    if (stage <= 5) {

        stageTime += dt;


        if (
            stageTime >=
            stageLimits[stage - 1]
        ) {

            finishStage();

            return;

        }


        // 적 생성
        const spawnInterval =
            Math.max(
                0.35,
                1.1 - stage * 0.1
            );


        if (
            Math.random()
            <
            dt / spawnInterval
        ) {

            spawnEnemy();

        }

    }


    // 보스 스테이지

    else {

        if (!bossSpawned) {

            spawnBoss();

        }


        bossAttackTimer -= dt;


        if (bossAttackTimer <= 0) {

            bossShoot();

            /*
                공격 간격

                1.5초마다 공격
            */

            bossAttackTimer = 1.5;

        }


        if (boss) {

            boss.attackFlash =
                Math.max(
                    0,
                    boss.attackFlash - dt
                );

        }

    }

}


// =========================================================
// 스테이지 클리어
// =========================================================

function finishStage() {

    gameRunning = false;


    // 남은 적 제거

    enemies = [];


    bullets = [];


    stageTime = 0;


    document
        .getElementById("upgradePTValue")
        .textContent = stagePT;


    document
        .getElementById("upgradeScreen")
        .style.display = "flex";

}


// =========================================================
// 다음 스테이지
// =========================================================

function nextStage() {

    stage++;


    stagePT = 0;


    enemies = [];

    bullets = [];

    bossProjectiles = [];


    if (stage <= 5) {

        stageTime = 0;

    }


    if (stage === 6) {

        boss = null;

        bossSpawned = false;

        bossAttackRotation = 0;

        bossAttackTimer = 0.5;

    }


    gameRunning = true;

}


// =========================================================
// 게임 종료
// =========================================================

function finalGame() {

    gameRunning = false;


    document
        .getElementById("finalPT")
        .textContent = totalEarnedPT;


    document
        .getElementById("gameOverTitle")
        .textContent =
        "BOSS DEFEATED!";


    document
        .getElementById("gameOverScreen")
        .style.display = "flex";

}


// =========================================================
// 게임 오버
// =========================================================

function gameOver() {

    gameRunning = false;


    document
        .getElementById("finalPT")
        .textContent = totalEarnedPT;


    document
        .getElementById("gameOverTitle")
        .textContent =
        "GAME OVER";


    document
        .getElementById("gameOverScreen")
        .style.display = "flex";

}


// =========================================================
// 업그레이드
// =========================================================

document
    .getElementById("attackUpgrade")
    .onclick = function() {

        if (stagePT >= 5) {

            stagePT -= 5;

            player.attack += 5;

        }

        updateUI();

    };


document
    .getElementById("speedUpgrade")
    .onclick = function() {

        if (stagePT >= 5) {

            stagePT -= 5;

            player.attackSpeed =
                Math.max(
                    0.08,
                    player.attackSpeed - 0.05
                );

        }

        updateUI();

    };


document
    .getElementById("critUpgrade")
    .onclick = function() {

        if (stagePT >= 5) {

            stagePT -= 5;

            player.crit =
                Math.min(
                    1,
                    player.crit + 0.05
                );

        }

        updateUI();

    };


document
    .getElementById("hpUpgrade")
    .onclick = function() {

        if (stagePT >= 5) {

            stagePT -= 5;

            player.maxHp += 20;

            player.hp += 20;

        }

        updateUI();

    };


document
    .getElementById("nextStageButton")
    .onclick = function() {

        document
            .getElementById("upgradeScreen")
            .style.display = "none";


        nextStage();

    };


// =========================================================
// 게임 시작
// =========================================================

function startGame() {

    stage = 1;

    stageTime = 0;

    stagePT = 0;

    totalEarnedPT = 0;


    enemies = [];

    bullets = [];

    bossProjectiles = [];

    hitEffects = [];


    boss = null;

    bossSpawned = false;


    player.x = WIDTH / 2;

    player.y = HEIGHT / 2;

    player.hp = player.maxHp;

    player.attack = 10;

    player.attackSpeed = 0.35;

    player.crit = 0.10;


    bossAttackRotation = 0;

    bossAttackTimer = 0.5;


    document
        .getElementById("startScreen")
        .style.display = "none";


    document
        .getElementById("gameOverScreen")
        .style.display = "none";


    document
        .getElementById("upgradeScreen")
        .style.display = "none";


    document
        .getElementById("bossBarContainer")
        .style.display = "none";


    gameRunning = true;


    updateUI();

}


document
    .getElementById("startButton")
    .onclick = startGame;


document
    .getElementById("restartButton")
    .onclick = startGame;


// =========================================================
// UI
// =========================================================

function updateUI() {

    document
        .getElementById("hp")
        .textContent =
        Math.max(
            0,
            Math.ceil(player.hp)
        );


    document
        .getElementById("pt")
        .textContent = stagePT;


    document
        .getElementById("attack")
        .textContent =
        player.attack;


    document
        .getElementById("crit")
        .textContent =
        Math.round(
            player.crit * 100
        );


    document
        .getElementById("stage")
        .textContent =
        stage;


    document
        .getElementById("upgradePTValue")
        .textContent =
        stagePT;


    if (boss) {

        document
            .getElementById("bossBar")
            .style.width =
            Math.max(
                0,
                boss.hp / boss.maxHp * 100
            ) + "%";

    }

}


// =========================================================
// 그리기
// =========================================================

function drawImageOrCircle(
    image,
    x,
    y,
    width,
    height
) {

    if (
        image &&
        image.complete &&
        image.naturalWidth > 0
    ) {

        ctx.drawImage(
            image,
            x - width / 2,
            y - height / 2,
            width,
            height
        );

    }

    else {

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            width / 2,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }

}


function drawBackground() {

    if (
        img.background &&
        img.background.complete &&
        img.background.naturalWidth > 0
    ) {

        ctx.drawImage(
            img.background,
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

}


function drawPlayer() {

    drawImageOrCircle(
        img.player,
        player.x,
        player.y,
        60,
        60
    );

}


function drawEnemies() {

    for (const enemy of enemies) {

        if (enemy.type === "tank") {

            drawImageOrCircle(
                img.enemyTank,
                enemy.x,
                enemy.y,
                65,
                65
            );

        }

        else {

            drawImageOrCircle(
                img.enemyNormal,
                enemy.x,
                enemy.y,
                50,
                50
            );

        }

    }

}


function drawBoss() {

    if (!boss) return;


    let size = 130;


    if (boss.attackFlash > 0) {

        ctx.save();

        ctx.globalAlpha = 0.35;

        ctx.beginPath();

        ctx.arc(
            boss.x,
            boss.y,
            100,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.restore();

    }


    drawImageOrCircle(
        img.boss,
        boss.x,
        boss.y,
        size,
        size
    );

}


function drawBullets() {

    for (const bullet of bullets) {

        if (
            img.bullet &&
            img.bullet.complete &&
            img.bullet.naturalWidth > 0
        ) {

            ctx.drawImage(
                img.bullet,
                bullet.x - 12,
                bullet.y - 12,
                24,
                24
            );

        }

        else {

            ctx.beginPath();

            ctx.arc(
                bullet.x,
                bullet.y,
                bullet.radius,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }

    }

}


function drawBossProjectiles() {

    for (
        const projectile
        of bossProjectiles
    ) {

        if (
            img.bossAttack &&
            img.bossAttack.complete &&
            img.bossAttack.naturalWidth > 0
        ) {

            ctx.save();


            const angle =
                Math.atan2(
                    projectile.vy,
                    projectile.vx
                );


            ctx.translate(
                projectile.x,
                projectile.y
            );


            ctx.rotate(angle);


            ctx.drawImage(
                img.bossAttack,
                -24,
                -24,
                48,
                48
            );


            ctx.restore();

        }

        else {

            ctx.beginPath();

            ctx.arc(
                projectile.x,
                projectile.y,
                projectile.radius,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }

    }

}


function drawHitEffects() {

    for (const effect of hitEffects) {

        const alpha =
            effect.life /
            effect.maxLife;


        if (
            img.hitEffect &&
            img.hitEffect.complete &&
            img.hitEffect.naturalWidth > 0
        ) {

            ctx.save();

            ctx.globalAlpha = alpha;

            ctx.drawImage(
                img.hitEffect,
                effect.x - effect.size / 2,
                effect.y - effect.size / 2,
                effect.size,
                effect.size
            );

            ctx.restore();

        }

        else {

            ctx.save();

            ctx.globalAlpha = alpha;

            ctx.beginPath();

            ctx.arc(
                effect.x,
                effect.y,
                effect.size * (1 - alpha),
                0,
                Math.PI * 2
            );

            ctx.stroke();

            ctx.restore();

        }

    }

}


// =========================================================
// 메인 게임 루프
// =========================================================

let lastTime = performance.now();


function gameLoop(now) {

    const dt =
        Math.min(
            (now - lastTime) / 1000,
            0.05
        );


    lastTime = now;


    if (gameRunning) {

        updateStage(dt);

        updatePlayer(dt);

        updateEnemies(dt);

        updateBullets(dt);

        updateBossProjectiles(dt);

        updateHitEffects(dt);


        if (player.hp <= 0) {

            player.hp = 0;

            gameOver();

        }


        updateUI();

    }


    // 그리기

    drawBackground();

    drawEnemies();

    drawBoss();

    drawBullets();

    drawBossProjectiles();

    drawPlayer();

    drawHitEffects();


    requestAnimationFrame(gameLoop);

}


requestAnimationFrame(gameLoop);


</script>

</body>

</html>
"""


# =========================================================
# 이미지 삽입
# =========================================================

html = html.replace(
    "__PLAYER__",
    images["player"]
)

html = html.replace(
    "__ENEMY_NORMAL__",
    images["enemyNormal"]
)

html = html.replace(
    "__ENEMY_TANK__",
    images["enemyTank"]
)

html = html.replace(
    "__BOSS__",
    images["boss"]
)

html = html.replace(
    "__BOSS_ATTACK__",
    images["bossAttack"]
)

html = html.replace(
    "__BACKGROUND__",
    images["background"]
)

html = html.replace(
    "__BULLET__",
    images["bullet"]
)

html = html.replace(
    "__HIT_EFFECT__",
    images["hitEffect"]
)


# =========================================================
# Streamlit 실행
# =========================================================

components.html(
    html,
    height=720,
    scrolling=False
)
<style>

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: #10131a;
    overflow: hidden;
    font-family: Arial, sans-serif;
    color: white;
}}

#gameWrapper {{
    width: 100%;
    display: flex;
    justify-content: center;
}}

#gameContainer {{
    position: relative;
    width: 1000px;
    max-width: 100%;
}}

canvas {{
    display: block;
    width: 100%;
    height: auto;
    background: #222;
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0,0,0,0.6);
}}

#ui {{
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    z-index: 10;
    pointer-events: none;
}}

.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.panel {{
    background: rgba(0,0,0,0.68);
    padding: 10px 15px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}}

#hpBarOuter {{
    width: 250px;
    height: 18px;
    margin-top: 5px;
    background: #333;
    border-radius: 10px;
    overflow: hidden;
}}

#hpBar {{
    width: 100%;
    height: 100%;
    background: #39d353;
    transition: width 0.15s;
}}

#menu {{
    position: absolute;
    inset: 0;
    z-index: 20;

    display: flex;
    justify-content: center;
    align-items: center;

    background: rgba(0,0,0,0.82);
}}

.menuBox {{
    width: 520px;
    max-width: 90%;

    padding: 35px;

    background: #171b25;

    border-radius: 18px;

    text-align: center;

    border: 1px solid #414858;

    box-shadow: 0 0 40px rgba(0,0,0,0.7);
}}

.menuBox h1 {{
    font-size: 42px;
    margin: 0 0 15px;
}}

.menuBox p {{
    color: #b9c0cc;
    line-height: 1.6;
}}

button {{
    border: none;
    padding: 13px 20px;
    margin: 7px;

    border-radius: 9px;

    background: #5865f2;

    color: white;

    font-size: 16px;

    cursor: pointer;
}}

button:hover {{
    filter: brightness(1.2);
}}

.upgrade {{
    width: 90%;
    margin: 8px auto;

    display: block;

    text-align: left;

    background: #252b38;
}}

.upgrade span {{
    float: right;
}}

.hidden {{
    display: none !important;
}}

#message {{
    position: absolute;

    top: 45%;
    left: 50%;

    transform: translate(-50%, -50%);

    font-size: 34px;

    font-weight: bold;

    text-align: center;

    text-shadow: 0 3px 10px black;

    pointer-events: none;

    z-index: 15;
}}

</style>

</head>


<body>


<div id="gameWrapper">

<div id="gameContainer">


<canvas
    id="gameCanvas"
    width="1000"
    height="650">
</canvas>


<!-- ====================================================== -->
<!-- UI -->
<!-- ====================================================== -->

<div id="ui">

<div class="topbar">


<div class="panel">

    <div>
        ❤️ HP:
        <span id="hpText">100 / 100</span>
    </div>

    <div id="hpBarOuter">

        <div id="hpBar"></div>

    </div>

</div>


<div class="panel">

    <div>
        🎯 Stage:
        <span id="stageText">1 / 6</span>
    </div>

    <div>
        ⭐ PT:
        <span id="ptText">0</span>
    </div>

    <div>
        👾 Enemies:
        <span id="enemyText">0</span>
    </div>

</div>


</div>

</div>


<div id="message"></div>


<!-- ====================================================== -->
<!-- 메뉴 -->
<!-- ====================================================== -->

<div id="menu">

<div class="menuBox" id="startMenu">

<h1>PT SURVIVAL</h1>

<p>
몰려오는 적들을 처치하고 PT를 획득하세요.
<br>
스테이지가 끝날 때마다 PT를 사용해 능력을 강화할 수 있습니다.
<br>
6스테이지의 보스를 처치하면 게임이 종료됩니다.
</p>

<p>

🖱️ 마우스 : 조준
<br>
🔫 자동 공격
<br>
⌨️ WASD / 방향키 : 이동

</p>

<button onclick="startGame()">
게임 시작
</button>

</div>

</div>


</div>

</div>


<script>


// ============================================================
// 이미지
// ============================================================

const IMG = {{

    player: "{images["player.png"]}",
    normal: "{images["enemy_normal.png"]}",
    tank: "{images["enemy_tank.png"]}",
    boss: "{images["boss.png"]}",
    background: "{images["background.png"]}",
    bullet: "{images["bullet.png"]}",
    hit: "{images["hit_effect.png"]}"

}};


function makeImage(src) {{

    const img = new Image();

    if (src) {{
        img.src = src;
    }}

    return img;

}}


const playerImg =
    makeImage(IMG.player);

const normalImg =
    makeImage(IMG.normal);

const tankImg =
    makeImage(IMG.tank);

const bossImg =
    makeImage(IMG.boss);

const backgroundImg =
    makeImage(IMG.background);

const bulletImg =
    makeImage(IMG.bullet);

const hitImg =
    makeImage(IMG.hit);


// ============================================================
// Canvas
// ============================================================

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");


// ============================================================
// 게임 상태
// ============================================================

let gameRunning = false;

let stage = 1;

let totalPT = 0;

let stagePT = 0;

let totalEarnedPT = 0;

let enemies = [];

let bullets = [];

let effects = [];

let lastTime = 0;

let spawnTimer = 0;

let stageTimer = 0;

let attackTimer = 0;

let bossSpawned = false;

let mouseX = 500;

let mouseY = 300;

let keys = {{}};


// ============================================================
// 플레이어
// ============================================================

let player = {{

    x: 500,

    y: 550,

    width: 65,

    height: 65,

    speed: 300,

    maxHp: 100,

    hp: 100,

    attack: 20,

    attackSpeed: 0.35,

    critChance: 0.10,

    critDamage: 2.0,

    bulletSpeed: 700,

    invincible: 0

}};


// ============================================================
// 스테이지 설정
// ============================================================

const stages = {{

    1: {{

        duration: 20,

        spawnRate: 0.9,

        normalHp: 40,

        normalSpeed: 80,

        tankHp: 120,

        tankSpeed: 45

    }},

    2: {{

        duration: 22,

        spawnRate: 0.8,

        normalHp: 55,

        normalSpeed: 95,

        tankHp: 160,

        tankSpeed: 50

    }},

    3: {{

        duration: 24,

        spawnRate: 0.7,

        normalHp: 75,

        normalSpeed: 110,

        tankHp: 220,

        tankSpeed: 55

    }},

    4: {{

        duration: 27,

        spawnRate: 0.6,

        normalHp: 100,

        normalSpeed: 120,

        tankHp: 300,

        tankSpeed: 60

    }},

    5: {{

        duration: 30,

        spawnRate: 0.5,

        normalHp: 130,

        normalSpeed: 135,

        tankHp: 400,

        tankSpeed: 65

    }},

    6: {{

        duration: 999999,

        spawnRate: 1.0,

        normalHp: 180,

        normalSpeed: 140,

        tankHp: 500,

        tankSpeed: 70

    }}

}};


// ============================================================
// 마우스
// ============================================================

canvas.addEventListener(
    "mousemove",
    function(e) {{

        const rect =
            canvas.getBoundingClientRect();

        mouseX =
            (e.clientX - rect.left)
            * canvas.width
            / rect.width;

        mouseY =
            (e.clientY - rect.top)
            * canvas.height
            / rect.height;

    }}
);


// ============================================================
// 키보드
// ============================================================

window.addEventListener(
    "keydown",
    function(e) {{

        keys[e.key.toLowerCase()] = true;

    }}
);


window.addEventListener(
    "keyup",
    function(e) {{

        keys[e.key.toLowerCase()] = false;

    }}
);


// ============================================================
// 게임 시작
// ============================================================

function startGame() {{

    stage = 1;

    totalPT = 0;

    stagePT = 0;

    totalEarnedPT = 0;

    enemies = [];

    bullets = [];

    effects = [];

    player.maxHp = 100;

    player.hp = 100;

    player.attack = 20;

    player.attackSpeed = 0.35;

    player.critChance = 0.10;

    player.critDamage = 2.0;

    player.x = canvas.width / 2;

    player.y = canvas.height - 100;

    stageTimer = 0;

    spawnTimer = 0;

    attackTimer = 0;

    bossSpawned = false;

    gameRunning = true;

    document
        .getElementById("menu")
        .classList.add("hidden");

    lastTime = performance.now();

    requestAnimationFrame(gameLoop);

}}


// ============================================================
// 일반 적 생성
// ============================================================

function spawnEnemy() {{

    const setting = stages[stage];

    let type;

    const tankChance =
        Math.min(
            0.10 + stage * 0.04,
            0.30
        );

    if (Math.random() < tankChance) {{

        type = "tank";

    }} else {{

        type = "normal";

    }}


    const x =
        Math.random()
        * (canvas.width - 100)
        + 50;


    if (type === "normal") {{

        enemies.push({{

            type: "normal",

            x: x,

            y: -60,

            width: 55,

            height: 55,

            hp: setting.normalHp,

            maxHp: setting.normalHp,

            speed: setting.normalSpeed,

            damage: 10,

            pt: 10

        }});

    }}

    else {{

        enemies.push({{

            type: "tank",

            x: x,

            y: -80,

            width: 75,

            height: 75,

            hp: setting.tankHp,

            maxHp: setting.tankHp,

            speed: setting.tankSpeed,

            damage: 20,

            pt: 30

        }});

    }}

}}


// ============================================================
// 보스 생성
// ============================================================

function spawnBoss() {{

    enemies.push({{

        type: "boss",

        x: canvas.width / 2,

        y: -160,

        width: 150,

        height: 150,

        hp: 5000,

        maxHp: 5000,

        speed: 35,

        damage: 35,

        pt: 1000

    }});

    bossSpawned = true;

}}


// ============================================================
// 총알 발사
// ============================================================

function shoot() {{

    const dx =
        mouseX - player.x;

    const dy =
        mouseY - player.y;

    const distance =
        Math.sqrt(
            dx * dx + dy * dy
        );

    if (distance <= 0) return;


    const vx =
        dx / distance
        * player.bulletSpeed;

    const vy =
        dy / distance
        * player.bulletSpeed;


    let damage =
        player.attack;

    let critical = false;


    if (
        Math.random()
        < player.critChance
    ) {{

        damage *= player.critDamage;

        critical = true;

    }}


    bullets.push({{

        x: player.x,

        y: player.y,

        vx: vx,

        vy: vy,

        damage: damage,

        critical: critical,

        size: 20

    }});

}}


// ============================================================
// 충돌
// ============================================================

function collision(a, b) {{

    return (

        Math.abs(a.x - b.x)
        <
        (a.width + b.width) / 2

        &&

        Math.abs(a.y - b.y)
        <
        (a.height + b.height) / 2

    );

}}


// ============================================================
// 이펙트
// ============================================================

function createEffect(x, y) {{

    effects.push({{

        x: x,

        y: y,

        life: 0.3,

        maxLife: 0.3

    }});

}}


// ============================================================
// 플레이어 이동
// ============================================================

function updatePlayer(dt) {{

    let dx = 0;

    let dy = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {{
        dy -= 1;
    }}


    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {{
        dy += 1;
    }}


    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {{
        dx -= 1;
    }}


    if (
        keys["d"] ||
        keys["arrowright"]
    ) {{
        dx += 1;
    }}


    if (dx !== 0 || dy !== 0) {{

        const length =
            Math.sqrt(
                dx * dx + dy * dy
            );

        dx /= length;

        dy /= length;


        player.x +=
            dx * player.speed * dt;

        player.y +=
            dy * player.speed * dt;

    }}


    player.x =
        Math.max(
            35,
            Math.min(
                canvas.width - 35,
                player.x
            )
        );


    player.y =
        Math.max(
            35,
            Math.min(
                canvas.height - 35,
                player.y
            )
        );


    if (player.invincible > 0) {{

        player.invincible -= dt;

    }}

}}


// ============================================================
// 총알 업데이트
// ============================================================

function updateBullets(dt) {{

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {{

        const bullet =
            bullets[i];


        bullet.x +=
            bullet.vx * dt;

        bullet.y +=
            bullet.vy * dt;


        let removeBullet = false;


        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {{

            const enemy =
                enemies[j];


            const bulletBox = {{

                x: bullet.x,

                y: bullet.y,

                width: bullet.size,

                height: bullet.size

            }};


            if (
                collision(
                    bulletBox,
                    enemy
                )
            ) {{

                enemy.hp -=
                    bullet.damage;


                createEffect(
                    bullet.x,
                    bullet.y
                );


                removeBullet = true;


                if (enemy.hp <= 0) {{

                    totalPT += enemy.pt;

                    stagePT += enemy.pt;

                    totalEarnedPT += enemy.pt;


                    createEffect(
                        enemy.x,
                        enemy.y
                    );


                    enemies.splice(
                        j,
                        1
                    );

                }}


                break;

            }}

        }}


        if (
            bullet.x < -50 ||
            bullet.x > canvas.width + 50 ||
            bullet.y < -50 ||
            bullet.y > canvas.height + 50
        ) {{

            removeBullet = true;

        }}


        if (removeBullet) {{

            bullets.splice(i, 1);

        }}

    }}

}}


// ============================================================
// 적 업데이트
// ============================================================

function updateEnemies(dt) {{

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {{

        const enemy =
            enemies[i];


        const dx =
            player.x - enemy.x;

        const dy =
            player.y - enemy.y;


        const distance =
            Math.sqrt(
                dx * dx + dy * dy
            );


        if (distance > 1) {{

            enemy.x +=
                dx / distance
                * enemy.speed
                * dt;

            enemy.y +=
                dy / distance
                * enemy.speed
                * dt;

        }}


        if (
            collision(
                enemy,
                player
            )
        ) {{

            if (
                player.invincible <= 0
            ) {{

                player.hp -=
                    enemy.damage;


                player.invincible =
                    0.5;


                createEffect(
                    player.x,
                    player.y
                );


                if (
                    enemy.type !== "boss"
                ) {{

                    enemies.splice(
                        i,
                        1
                    );

                }}


                if (player.hp <= 0) {{

                    gameOver();

                    return;

                }}

            }}

        }}

    }}

}}


// ============================================================
// 이펙트 업데이트
// ============================================================

function updateEffects(dt) {{

    for (
        let i = effects.length - 1;
        i >= 0;
        i--
    ) {{

        effects[i].life -= dt;


        if (
            effects[i].life <= 0
        ) {{

            effects.splice(
                i,
                1
            );

        }}

    }}

}}


// ============================================================
// 공격
// ============================================================

function updateAttack(dt) {{

    attackTimer -= dt;


    if (attackTimer <= 0) {{

        shoot();

        attackTimer =
            player.attackSpeed;

    }}

}}


// ============================================================
// 스테이지 진행
// ============================================================

function updateStage(dt) {{

    stageTimer += dt;

    spawnTimer -= dt;


    const setting =
        stages[stage];


    // --------------------------------------------------------
    // 1~5 스테이지
    // --------------------------------------------------------

    if (stage < 6) {{

        if (spawnTimer <= 0) {{

            spawnEnemy();

            spawnTimer =
                setting.spawnRate;

        }}


        // 시간이 지나면 즉시 종료
        if (
            stageTimer >=
            setting.duration
        ) {{

            finishStage();

        }}

        return;

    }}


    // --------------------------------------------------------
    // 6 스테이지
    // --------------------------------------------------------

    if (stage === 6) {{

        // 보스가 아직 없다면 생성
        if (
            !bossSpawned &&
            stageTimer >= 2
        ) {{

            spawnBoss();

        }}

    }}

}}


// ============================================================
// 스테이지 종료
// ============================================================

function finishStage() {{

    if (!gameRunning) return;

    gameRunning = false;

    showUpgradeMenu();

}}


// ============================================================
// 강화 메뉴
// ============================================================

function showUpgradeMenu() {{

    const menu =
        document.getElementById("menu");

    menu.classList.remove("hidden");


    document.getElementById(
        "startMenu"
    ).innerHTML = `

        <h1>
            STAGE ${{stage}} CLEAR!
        </h1>

        <p>
            이번 스테이지 획득 PT:
            <b>${{stagePT}}</b>
        </p>

        <p>
            사용 가능한 PT:
            <b>${{totalPT}}</b>
        </p>

        <hr>

        <button
            class="upgrade"
            onclick="upgradeAttack()"
        >
            ⚔️ 공격력 강화
            <span>100 PT</span>
        </button>


        <button
            class="upgrade"
            onclick="upgradeSpeed()"
        >
            🔫 공격 속도 강화
            <span>150 PT</span>
        </button>


        <button
            class="upgrade"
            onclick="upgradeCrit()"
        >
            💥 치명타 확률 강화
            <span>200 PT</span>
        </button>


        <button
            class="upgrade"
            onclick="upgradeHp()"
        >
            ❤️ 최대 체력 강화
            <span>250 PT</span>
        </button>


        <br>


        <button onclick="nextStage()">

            다음 스테이지 →

        </button>

    `;

}}


// ============================================================
// 공격력 강화
// ============================================================

function upgradeAttack() {{

    if (totalPT >= 100) {{

        totalPT -= 100;

        player.attack += 10;

        showUpgradeMenu();

    }}

}}


// ============================================================
// 공격 속도 강화
// ============================================================

function upgradeSpeed() {{

    if (totalPT >= 150) {{

        totalPT -= 150;

        player.attackSpeed =
            Math.max(
                0.08,
                player.attackSpeed - 0.04
            );

        showUpgradeMenu();

    }}

}}


// ============================================================
// 치명타 강화
// ============================================================

function upgradeCrit() {{

    if (totalPT >= 200) {{

        totalPT -= 200;

        player.critChance =
            Math.min(
                0.75,
                player.critChance + 0.05
            );

        showUpgradeMenu();

    }}

}}


// ============================================================
// 체력 강화
// ============================================================

function upgradeHp() {{

    if (totalPT >= 250) {{

        totalPT -= 250;

        player.maxHp += 25;

        player.hp =
            player.maxHp;

        showUpgradeMenu();

    }}

}}


// ============================================================
// 다음 스테이지
// ============================================================

function nextStage() {{

    if (stage >= 6) return;


    stage++;

    stagePT = 0;

    stageTimer = 0;

    spawnTimer = 0;

    enemies = [];

    bullets = [];

    effects = [];

    bossSpawned = false;


    player.hp =
        player.maxHp;


    player.x =
        canvas.width / 2;

    player.y =
        canvas.height - 100;


    document
        .getElementById("menu")
        .classList.add("hidden");


    gameRunning = true;

    lastTime =
        performance.now();


    requestAnimationFrame(
        gameLoop
    );

}}


// ============================================================
// 보스 사망 확인
// ============================================================

function checkBossDeath() {{

    if (stage !== 6) return;

    if (!bossSpawned) return;


    const boss =
        enemies.find(
            e => e.type === "boss"
        );


    if (!boss) {{

        finalGame();

    }}

}}


// ============================================================
// 최종 클리어
// ============================================================

function finalGame() {{

    gameRunning = false;

    enemies = [];

    bullets = [];


    document
        .getElementById("menu")
        .classList.remove("hidden");


    document.getElementById(
        "startMenu"
    ).innerHTML = `

        <h1>
            🏆 GAME CLEAR!
        </h1>

        <p>
            최종 보스를 처치했습니다!
        </p>

        <hr>

        <h2>
            FINAL SCORE
        </h2>

        <h1
            style="font-size:55px;"
        >
            ${{totalEarnedPT}} PT
        </h1>

        <p>
            게임에서 획득한 전체 PT를 기준으로
            최종 점수가 계산되었습니다.
        </p>

        <button
            onclick="location.reload()"
        >
            다시 시작
        </button>

    `;

}}


// ============================================================
// 게임 오버
// ============================================================

function gameOver() {{

    gameRunning = false;


    document
        .getElementById("menu")
        .classList.remove("hidden");


    document.getElementById(
        "startMenu"
    ).innerHTML = `

        <h1>
            GAME OVER
        </h1>

        <p>
            Stage ${{stage}}에서 쓰러졌습니다.
        </p>

        <h2>
            획득 PT:
            ${{totalEarnedPT}}
        </h2>

        <button
            onclick="location.reload()"
        >
            다시 시작
        </button>

    `;

}}


// ============================================================
// 배경 그리기
// ============================================================

function drawBackground() {{

    if (
        backgroundImg.complete &&
        backgroundImg.naturalWidth > 0
    ) {{

        ctx.drawImage(
            backgroundImg,
            0,
            0,
            canvas.width,
            canvas.height
        );

    }}

    else {{

        ctx.fillStyle =
            "#17202b";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

    }}

}}


// ============================================================
// 플레이어 그리기
// ============================================================

function drawPlayer() {{

    if (
        player.invincible > 0 &&
        Math.floor(
            player.invincible * 20
        ) % 2 === 0
    ) {{

        return;

    }}


    if (
        playerImg.complete &&
        playerImg.naturalWidth > 0
    ) {{

        ctx.drawImage(

            playerImg,

            player.x -
                player.width / 2,

            player.y -
                player.height / 2,

            player.width,

            player.height

        );

    }}

    else {{

        ctx.fillStyle =
            "#4da6ff";

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            30,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }}

}}


// ============================================================
// 적 그리기
// ============================================================

function drawEnemy(enemy) {{

    let img;


    if (
        enemy.type === "normal"
    ) {{

        img = normalImg;

    }}

    else if (
        enemy.type === "tank"
    ) {{

        img = tankImg;

    }}

    else {{

        img = bossImg;

    }}


    if (
        img.complete &&
        img.naturalWidth > 0
    ) {{

        ctx.drawImage(

            img,

            enemy.x -
                enemy.width / 2,

            enemy.y -
                enemy.height / 2,

            enemy.width,
            enemy.height

        );

    }}

    else {{

        ctx.fillStyle =
            enemy.type === "boss"
            ? "#b000ff"
            : enemy.type === "tank"
            ? "#777"
            : "#ff4444";


        ctx.beginPath();

        ctx.arc(

            enemy.x,
            enemy.y,

            enemy.width / 2,

            0,
            Math.PI * 2

        );

        ctx.fill();

    }}


    // 적 HP 바

    if (
        enemy.type !== "boss"
    ) {{

        const barWidth =
            enemy.width;


        const hpRatio =
            Math.max(
                0,
                enemy.hp /
                enemy.maxHp
            );


        ctx.fillStyle =
            "#222";


        ctx.fillRect(

            enemy.x -
                barWidth / 2,

            enemy.y -
                enemy.height / 2 -
                10,

            barWidth,

            6

        );


        ctx.fillStyle =
            "#39d353";


        ctx.fillRect(

            enemy.x -
                barWidth / 2,

            enemy.y -
                enemy.height / 2 -
                10,

            barWidth * hpRatio,

            6

        );

    }}

}}


// ============================================================
// 보스 HP
// ============================================================

function drawBossHP() {{

    const boss =
        enemies.find(
            e => e.type === "boss"
        );


    if (!boss) return;


    const width = 600;

    const height = 22;

    const x =
        canvas.width / 2 -
        width / 2;

    const y = 70;


    ctx.fillStyle =
        "#222";


    ctx.fillRect(
        x,
        y,
        width,
        height
    );


    ctx.fillStyle =
        "#c43cff";


    ctx.fillRect(

        x,
        y,

        width *
        Math.max(
            0,
            boss.hp /
            boss.maxHp
        ),

        height

    );


    ctx.strokeStyle =
        "white";


    ctx.strokeRect(
        x,
        y,
        width,
        height
    );


    ctx.fillStyle =
        "white";


    ctx.font =
        "bold 16px Arial";


    ctx.textAlign =
        "center";


    ctx.fillText(
        "BOSS HP",
        canvas.width / 2,
        y - 7
    );

}}


// ============================================================
// 총알 그리기
// ============================================================

function drawBullets() {{

    for (
        const bullet of bullets
    ) {{

        if (
            bulletImg.complete &&
            bulletImg.naturalWidth > 0
        ) {{

            ctx.drawImage(

                bulletImg,

                bullet.x - 10,

                bullet.y - 10,

                20,

                20

            );

        }}

        else {{

            ctx.fillStyle =
                bullet.critical
                ? "#ffd700"
                : "#ffffff";


            ctx.beginPath();


            ctx.arc(

                bullet.x,
                bullet.y,

                7,

                0,
                Math.PI * 2

            );


            ctx.fill();

        }}

    }}

}}


// ============================================================
// 이펙트 그리기
// ============================================================

function drawEffects() {{

    for (
        const effect of effects
    ) {{

        const alpha =
            effect.life /
            effect.maxLife;


        ctx.globalAlpha =
            alpha;


        if (
            hitImg.complete &&
            hitImg.naturalWidth > 0
        ) {{

            const size =
                80 *
                (1 - alpha * 0.3);


            ctx.drawImage(

                hitImg,

                effect.x -
                    size / 2,

                effect.y -
                    size / 2,

                size,
                size

            );

        }}

        else {{

            ctx.fillStyle =
                "#ffffff";


            ctx.beginPath();


            ctx.arc(

                effect.x,
                effect.y,

                35 *
                (1 - alpha),

                0,
                Math.PI * 2

            );


            ctx.fill();

        }}


        ctx.globalAlpha = 1;

    }}

}}


// ============================================================
// UI 업데이트
// ============================================================

function updateUI() {{

    document.getElementById(
        "hpText"
    ).textContent =

        Math.max(
            0,
            Math.floor(player.hp)
        )

        + " / "

        + player.maxHp;


    document.getElementById(
        "hpBar"
    ).style.width =

        Math.max(
            0,
            player.hp /
            player.maxHp *
            100
        )

        + "%";


    document.getElementById(
        "stageText"
    ).textContent =

        stage + " / 6";


    document.getElementById(
        "ptText"
    ).textContent =

        totalPT;


    document.getElementById(
        "enemyText"
    ).textContent =

        enemies.length;

}}


// ============================================================
// 게임 루프
// ============================================================

function gameLoop(time) {{

    if (!gameRunning) return;


    let dt =
        (time - lastTime) /
        1000;


    dt =
        Math.min(
            dt,
            0.05
        );


    lastTime = time;


    updatePlayer(dt);

    updateAttack(dt);

    updateBullets(dt);

    updateEnemies(dt);

    updateEffects(dt);

    updateStage(dt);

    checkBossDeath();


    drawBackground();

    drawBullets();


    for (
        const enemy of enemies
    ) {{

        drawEnemy(enemy);

    }}


    drawEffects();

    drawPlayer();

    drawBossHP();

    updateUI();


    requestAnimationFrame(
        gameLoop
    );

}}


// ============================================================
// 화면 크기
// ============================================================

function resizeCanvas() {{

    const width =
        Math.min(
            1000,
            window.innerWidth - 20
        );


    canvas.style.width =
        width + "px";

}}


window.addEventListener(
    "resize",
    resizeCanvas
);


resizeCanvas();

</script>


</body>

</html>
"""


# ============================================================
# Streamlit 실행
# ============================================================

components.html(
    html,
    height=700,
    scrolling=False
)
