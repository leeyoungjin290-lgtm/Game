import streamlit as st
import streamlit.components.v1 as components
import base64
import os


# =========================================================
# Streamlit 설정
# =========================================================

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
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return "data:image/png;base64," + encoded


images = {
    "player": load_image("player.png"),
    "normal": load_image("enemy_normal.png"),
    "tank": load_image("enemy_tank.png"),
    "boss": load_image("boss.png"),
    "bossAttack": load_image("boss_attack.png"),
    "background": load_image("background.png"),
    "bullet": load_image("bullet.png"),
    "hit": load_image("hit_effect.png")
}


# =========================================================
# HTML
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

html,
body {
    margin: 0;
    padding: 0;
    background: #10131a;
    overflow: hidden;
    font-family: Arial, sans-serif;
    color: white;
}

#gameWrapper {
    width: 100%;
    display: flex;
    justify-content: center;
}

#gameContainer {
    position: relative;
    width: 1000px;
    max-width: 100%;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    background: #222;
    cursor: crosshair;
}

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    z-index: 10;
    pointer-events: none;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.panel {
    background: rgba(0, 0, 0, 0.68);
    padding: 10px 15px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}

#hpBarOuter {
    width: 250px;
    height: 18px;
    margin-top: 5px;
    background: #333;
    border-radius: 10px;
    overflow: hidden;
}

#hpBar {
    width: 100%;
    height: 100%;
    background: #39d353;
}

#bossBarOuter {
    position: absolute;
    top: 70px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 22px;
    background: #222;
    border: 2px solid white;
    display: none;
    z-index: 9;
}

#bossBar {
    width: 100%;
    height: 100%;
    background: #c43cff;
}

#bossText {
    position: absolute;
    top: 48px;
    left: 50%;
    transform: translateX(-50%);
    font-weight: bold;
    display: none;
    z-index: 10;
}

#menu {
    position: absolute;
    inset: 0;
    z-index: 20;

    display: flex;
    justify-content: center;
    align-items: center;

    background: rgba(0,0,0,0.82);
}

.menuBox {
    width: 520px;
    max-width: 90%;
    padding: 35px;
    background: #171b25;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #414858;
    box-shadow: 0 0 40px rgba(0,0,0,0.7);
}

.menuBox h1 {
    font-size: 42px;
    margin: 0 0 15px;
}

.menuBox p {
    color: #b9c0cc;
    line-height: 1.6;
}

button {
    border: none;
    padding: 13px 20px;
    margin: 7px;
    border-radius: 9px;
    background: #5865f2;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    filter: brightness(1.2);
}

.upgrade {
    width: 90%;
    margin: 8px auto;
    display: block;
    text-align: left;
    background: #252b38;
}

.upgrade span {
    float: right;
}

.hidden {
    display: none !important;
}

#message {
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 3px 10px black;
    pointer-events: none;
    z-index: 15;
}

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


<!-- UI -->

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


<div id="bossText">
    BOSS HP
</div>

<div id="bossBarOuter">
    <div id="bossBar"></div>
</div>


<div id="message"></div>


<!-- 메뉴 -->

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


// =========================================================
// 이미지
// =========================================================

const IMG = {

    player: "__PLAYER__",
    normal: "__NORMAL__",
    tank: "__TANK__",
    boss: "__BOSS__",
    bossAttack: "__BOSS_ATTACK__",
    background: "__BACKGROUND__",
    bullet: "__BULLET__",
    hit: "__HIT__"

};


function makeImage(src) {

    const image = new Image();

    if (src) {
        image.src = src;
    }

    return image;

}


const playerImg = makeImage(IMG.player);
const normalImg = makeImage(IMG.normal);
const tankImg = makeImage(IMG.tank);
const bossImg = makeImage(IMG.boss);
const bossAttackImg = makeImage(IMG.bossAttack);
const backgroundImg = makeImage(IMG.background);
const bulletImg = makeImage(IMG.bullet);
const hitImg = makeImage(IMG.hit);


// =========================================================
// Canvas
// =========================================================

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");


// =========================================================
// 게임 변수
// =========================================================

let gameRunning = false;

let stage = 1;

let totalPT = 0;

let stagePT = 0;

let totalEarnedPT = 0;

let enemies = [];

let bullets = [];

let bossProjectiles = [];

let effects = [];

let lastTime = 0;

let spawnTimer = 0;

let stageTimer = 0;

let attackTimer = 0;

let bossAttackTimer = 1;

let bossAttackRotation = 0;

let bossSpawned = false;

let mouseX = 500;

let mouseY = 300;

let keys = {};


// =========================================================
// 플레이어
// =========================================================

let player = {

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

    critDamage: 2,

    bulletSpeed: 700,

    invincible: 0

};


// =========================================================
// 스테이지 설정
// =========================================================

const stages = {

    1: {
        duration: 20,
        spawnRate: 0.9,
        normalHp: 40,
        normalSpeed: 80,
        tankHp: 120,
        tankSpeed: 45
    },

    2: {
        duration: 22,
        spawnRate: 0.8,
        normalHp: 55,
        normalSpeed: 95,
        tankHp: 160,
        tankSpeed: 50
    },

    3: {
        duration: 24,
        spawnRate: 0.7,
        normalHp: 75,
        normalSpeed: 110,
        tankHp: 220,
        tankSpeed: 55
    },

    4: {
        duration: 27,
        spawnRate: 0.6,
        normalHp: 100,
        normalSpeed: 120,
        tankHp: 300,
        tankSpeed: 60
    },

    5: {
        duration: 30,
        spawnRate: 0.5,
        normalHp: 130,
        normalSpeed: 135,
        tankHp: 400,
        tankSpeed: 65
    }

};


// =========================================================
// 마우스
// =========================================================

canvas.addEventListener(
    "mousemove",
    function(e) {

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

    }
);


// =========================================================
// 키보드
// =========================================================

window.addEventListener(
    "keydown",
    function(e) {

        keys[e.key.toLowerCase()] = true;

    }
);


window.addEventListener(
    "keyup",
    function(e) {

        keys[e.key.toLowerCase()] = false;

    }
);


// =========================================================
// 게임 시작
// =========================================================

function startGame() {

    stage = 1;

    totalPT = 0;

    stagePT = 0;

    totalEarnedPT = 0;

    enemies = [];

    bullets = [];

    bossProjectiles = [];

    effects = [];

    player.maxHp = 100;

    player.hp = 100;

    player.attack = 20;

    player.attackSpeed = 0.35;

    player.critChance = 0.10;

    player.critDamage = 2;

    player.x = canvas.width / 2;

    player.y = canvas.height - 100;

    player.invincible = 0;

    stageTimer = 0;

    spawnTimer = 0;

    attackTimer = 0;

    bossAttackTimer = 1;

    bossAttackRotation = 0;

    bossSpawned = false;

    gameRunning = true;

    document
        .getElementById("menu")
        .classList.add("hidden");

    document
        .getElementById("bossBarOuter")
        .style.display = "none";

    document
        .getElementById("bossText")
        .style.display = "none";

    lastTime = performance.now();

    requestAnimationFrame(gameLoop);

}


// =========================================================
// 일반 적 생성
// =========================================================

function spawnEnemy() {

    const setting = stages[stage];

    const tankChance =
        Math.min(
            0.10 + stage * 0.04,
            0.30
        );

    const type =
        Math.random() < tankChance
        ? "tank"
        : "normal";

    const x =
        Math.random()
        * (canvas.width - 100)
        + 50;


    if (type === "normal") {

        enemies.push({

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

        });

    }

    else {

        enemies.push({

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

        });

    }

}


// =========================================================
// 보스 생성
// =========================================================

function spawnBoss() {

    enemies.push({

        type: "boss",

        x: canvas.width / 2,

        y: 130,

        width: 150,

        height: 150,

        hp: 5000,

        maxHp: 5000,

        speed: 35,

        damage: 35,

        pt: 1000,

        attackFlash: 0

    });

    bossSpawned = true;

    bossAttackTimer = 1;

    bossAttackRotation = 0;

    document
        .getElementById("bossBarOuter")
        .style.display = "block";

    document
        .getElementById("bossText")
        .style.display = "block";

}


// =========================================================
// 보스 공격
// =========================================================

function bossShoot(boss) {

    if (!boss) return;


    // 처음에는 위/오른쪽/아래/왼쪽
    // 이후 공격마다 45도씩 시계 방향 회전

    const directions = [

        { x: 0, y: -1 },

        { x: 1, y: 0 },

        { x: 0, y: 1 },

        { x: -1, y: 0 }

    ];


    for (const direction of directions) {

        const angle =
            Math.atan2(
                direction.y,
                direction.x
            )
            + bossAttackRotation;


        bossProjectiles.push({

            x: boss.x,

            y: boss.y,

            vx:
                Math.cos(angle) * 250,

            vy:
                Math.sin(angle) * 250,

            width: 48,

            height: 48,

            radius: 22,

            damage: 18,

            life: 5

        });

    }


    bossAttackRotation +=
        Math.PI / 4;


    if (
        bossAttackRotation >=
        Math.PI * 2
    ) {

        bossAttackRotation -=
            Math.PI * 2;

    }


    boss.attackFlash = 0.25;

}


// =========================================================
// 총알 발사
// =========================================================

function shoot() {

    const dx =
        mouseX - player.x;

    const dy =
        mouseY - player.y;

    const distance =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (distance <= 0) {
        return;
    }


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
    ) {

        damage *=
            player.critDamage;

        critical = true;

    }


    bullets.push({

        x: player.x,

        y: player.y,

        vx: vx,

        vy: vy,

        damage: damage,

        critical: critical,

        size: 20

    });

}


// =========================================================
// 충돌
// =========================================================

function collision(a, b) {

    return (

        Math.abs(a.x - b.x)
        <
        (a.width + b.width) / 2

        &&

        Math.abs(a.y - b.y)
        <
        (a.height + b.height) / 2

    );

}


// =========================================================
// 이펙트
// =========================================================

function createEffect(x, y, size) {

    effects.push({

        x: x,

        y: y,

        size: size || 80,

        life: 0.3,

        maxLife: 0.3

    });

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


    if (
        dx !== 0 ||
        dy !== 0
    ) {

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        dx /= length;

        dy /= length;


        player.x +=
            dx * player.speed * dt;

        player.y +=
            dy * player.speed * dt;

    }


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


    if (
        player.invincible > 0
    ) {

        player.invincible -= dt;

    }

}


// =========================================================
// 총알 업데이트
// =========================================================

function updateBullets(dt) {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

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
        ) {

            const enemy =
                enemies[j];


            const bulletBox = {

                x: bullet.x,

                y: bullet.y,

                width: bullet.size,

                height: bullet.size

            };


            if (
                collision(
                    bulletBox,
                    enemy
                )
            ) {

                enemy.hp -=
                    bullet.damage;


                createEffect(
                    bullet.x,
                    bullet.y,
                    enemy.type === "boss"
                    ? 100
                    : 60
                );


                removeBullet = true;


                if (
                    enemy.hp <= 0
                ) {

                    totalPT +=
                        enemy.pt;

                    stagePT +=
                        enemy.pt;

                    totalEarnedPT +=
                        enemy.pt;


                    createEffect(
                        enemy.x,
                        enemy.y,
                        enemy.type === "boss"
                        ? 180
                        : 80
                    );


                    if (
                        enemy.type === "boss"
                    ) {

                        bossSpawned = false;

                        finalGame();

                        return;

                    }


                    enemies.splice(
                        j,
                        1
                    );

                }


                break;

            }

        }


        if (
            bullet.x < -50 ||
            bullet.x >
                canvas.width + 50 ||
            bullet.y < -50 ||
            bullet.y >
                canvas.height + 50
        ) {

            removeBullet = true;

        }


        if (removeBullet) {

            bullets.splice(
                i,
                1
            );

        }

    }

}


// =========================================================
// 적 업데이트
// =========================================================

function updateEnemies(dt) {

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {

        const enemy =
            enemies[i];


        const dx =
            player.x - enemy.x;

        const dy =
            player.y - enemy.y;


        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        if (
            distance > 1
        ) {

            enemy.x +=
                dx / distance
                * enemy.speed
                * dt;

            enemy.y +=
                dy / distance
                * enemy.speed
                * dt;

        }


        if (
            collision(
                enemy,
                player
            )
        ) {

            if (
                player.invincible <= 0
            ) {

                player.hp -=
                    enemy.damage;

                player.invincible =
                    0.5;


                createEffect(
                    player.x,
                    player.y,
                    80
                );


                if (
                    enemy.type !== "boss"
                ) {

                    enemies.splice(
                        i,
                        1
                    );

                }


                if (
                    player.hp <= 0
                ) {

                    gameOver();

                    return;

                }

            }

        }


        // 보스 공격 타이머

        if (
            enemy.type === "boss"
        ) {

            enemy.attackFlash =
                Math.max(
                    0,
                    enemy.attackFlash - dt
                );

        }

    }

}


// =========================================================
// 보스 탄환 업데이트
// =========================================================

function updateBossProjectiles(dt) {

    for (
        let i =
            bossProjectiles.length - 1;
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


        const dx =
            projectile.x - player.x;

        const dy =
            projectile.y - player.y;


        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );


        if (
            distance <
            projectile.radius + 32
        ) {

            if (
                player.invincible <= 0
            ) {

                player.hp -=
                    projectile.damage;

                player.invincible =
                    0.5;

                createEffect(
                    player.x,
                    player.y,
                    90
                );

                bossProjectiles.splice(
                    i,
                    1
                );

                continue;

            }

        }


        if (
            projectile.life <= 0 ||
            projectile.x < -100 ||
            projectile.x >
                canvas.width + 100 ||
            projectile.y < -100 ||
            projectile.y >
                canvas.height + 100
        ) {

            bossProjectiles.splice(
                i,
                1
            );

        }

    }

}


// =========================================================
// 이펙트 업데이트
// =========================================================

function updateEffects(dt) {

    for (
        let i = effects.length - 1;
        i >= 0;
        i--
    ) {

        effects[i].life -= dt;


        if (
            effects[i].life <= 0
        ) {

            effects.splice(
                i,
                1
            );

        }

    }

}


// =========================================================
// 공격
// =========================================================

function updateAttack(dt) {

    attackTimer -= dt;


    if (
        attackTimer <= 0
    ) {

        shoot();

        attackTimer =
            player.attackSpeed;

    }

}


// =========================================================
// 스테이지 진행
// =========================================================

function updateStage(dt) {

    stageTimer += dt;


    // =====================================================
    // 1~5 스테이지
    // =====================================================

    if (
        stage < 6
    ) {

        spawnTimer -= dt;


        const setting =
            stages[stage];


        if (
            spawnTimer <= 0
        ) {

            spawnEnemy();

            spawnTimer =
                setting.spawnRate;

        }


        if (
            stageTimer >=
            setting.duration
        ) {

            finishStage();

        }


        return;

    }


    // =====================================================
    // 6 스테이지
    // =====================================================

    if (
        stage === 6
    ) {

        const boss =
            enemies.find(
                e => e.type === "boss"
            );


        if (
            !bossSpawned &&
            !boss &&
            stageTimer >= 1
        ) {

            spawnBoss();

        }


        if (boss) {

            bossAttackTimer -= dt;


            if (
                bossAttackTimer <= 0
            ) {

                bossShoot(boss);

                bossAttackTimer =
                    1.5;

            }

        }

    }

}


// =========================================================
// 스테이지 종료
// =========================================================

function finishStage() {

    if (
        !gameRunning
    ) {

        return;

    }


    gameRunning = false;

    enemies = [];

    bullets = [];

    bossProjectiles = [];

    showUpgradeMenu();

}


// =========================================================
// 강화 메뉴
// =========================================================

function showUpgradeMenu() {

    const menu =
        document.getElementById("menu");


    menu.classList.remove(
        "hidden"
    );


    document.getElementById(
        "startMenu"
    ).innerHTML = `

        <h1>
            STAGE ${stage} CLEAR!
        </h1>

        <p>
            이번 스테이지 획득 PT:
            <b>${stagePT}</b>
        </p>

        <p>
            사용 가능한 PT:
            <b>${totalPT}</b>
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


        <br>


        <button
            onclick="nextStage()"
        >
            다음 스테이지 →
        </button>

    `;

}


// =========================================================
// 공격력 강화
// =========================================================

function upgradeAttack() {

    if (
        totalPT >= 100
    ) {

        totalPT -= 100;

        player.attack += 10;

        showUpgradeMenu();

    }

}


// =========================================================
// 공격속도 강화
// =========================================================

function upgradeSpeed() {

    if (
        totalPT >= 150
    ) {

        totalPT -= 150;

        player.attackSpeed =
            Math.max(
                0.08,
                player.attackSpeed - 0.04
            );

        showUpgradeMenu();

    }

}


// =========================================================
// 치명타 강화
// =========================================================

function upgradeCrit() {

    if (
        totalPT >= 200
    ) {

        totalPT -= 200;

        player.critChance =
            Math.min(
                0.75,
                player.critChance + 0.05
            );

        showUpgradeMenu();

    }

}


// =========================================================
// 다음 스테이지
// =========================================================

function nextStage() {

    if (
        stage >= 6
    ) {

        return;

    }


    stage++;

    stagePT = 0;

    stageTimer = 0;

    spawnTimer = 0;

    attackTimer = 0;

    bossAttackTimer = 1;

    bossAttackRotation = 0;

    enemies = [];

    bullets = [];

    bossProjectiles = [];

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


    document
        .getElementById("bossBarOuter")
        .style.display =
        "none";

    document
        .getElementById("bossText")
        .style.display =
        "none";


    gameRunning = true;

    lastTime =
        performance.now();


    requestAnimationFrame(
        gameLoop
    );

}


// =========================================================
// 최종 클리어
// =========================================================

function finalGame() {

    gameRunning = false;

    enemies = [];

    bullets = [];

    bossProjectiles = [];


    document
        .getElementById("bossBarOuter")
        .style.display =
        "none";

    document
        .getElementById("bossText")
        .style.display =
        "none";


    document
        .getElementById("menu")
        .classList.remove(
            "hidden"
        );


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
            ${totalEarnedPT} PT
        </h1>

        <p>
            게임에서 획득한 전체 PT를
            기준으로 최종 점수가 계산되었습니다.
        </p>

        <button
            onclick="location.reload()"
        >
            다시 시작
        </button>

    `;

}


// =========================================================
// 게임 오버
// =========================================================

function gameOver() {

    gameRunning = false;


    document
        .getElementById("menu")
        .classList.remove(
            "hidden"
        );


    document.getElementById(
        "startMenu"
    ).innerHTML = `

        <h1>
            GAME OVER
        </h1>

        <p>
            Stage ${stage}에서 쓰러졌습니다.
        </p>

        <h2>
            획득 PT:
            ${totalEarnedPT}
        </h2>

        <button
            onclick="location.reload()"
        >
            다시 시작
        </button>

    `;

}


// =========================================================
// 배경 그리기
// =========================================================

function drawBackground() {

    if (
        backgroundImg.complete &&
        backgroundImg.naturalWidth > 0
    ) {

        ctx.drawImage(
            backgroundImg,
            0,
            0,
            canvas.width,
            canvas.height
        );

    }

    else {

        ctx.fillStyle =
            "#17202b";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

    }

}


// =========================================================
// 플레이어 그리기
// =========================================================

function drawPlayer() {

    if (
        player.invincible > 0 &&
        Math.floor(
            player.invincible * 20
        ) % 2 === 0
    ) {

        return;

    }


    if (
        playerImg.complete &&
        playerImg.naturalWidth > 0
    ) {

        ctx.drawImage(

            playerImg,

            player.x -
                player.width / 2,

            player.y -
                player.height / 2,

            player.width,

            player.height

        );

    }

    else {

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

    }

}


// =========================================================
// 적 그리기
// =========================================================

function drawEnemy(enemy) {

    let image;


    if (
        enemy.type === "normal"
    ) {

        image = normalImg;

    }

    else if (
        enemy.type === "tank"
    ) {

        image = tankImg;

    }

    else {

        image = bossImg;

    }


    if (
        image.complete &&
        image.naturalWidth > 0
    ) {

        ctx.drawImage(

            image,

            enemy.x -
                enemy.width / 2,

            enemy.y -
                enemy.height / 2,

            enemy.width,

            enemy.height

        );

    }

    else {

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

    }


    // 일반 적 HP 바

    if (
        enemy.type !== "boss"
    ) {

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

    }

}


// =========================================================
// 보스 탄환 그리기
// =========================================================

function drawBossProjectiles() {

    for (
        const projectile
        of bossProjectiles
    ) {

        if (
            bossAttackImg.complete &&
            bossAttackImg.naturalWidth > 0
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

                bossAttackImg,

                -24,
                -24,
                48,
                48

            );


            ctx.restore();

        }

        else {

            ctx.fillStyle =
                "#c43cff";

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


// =========================================================
// 총알 그리기
// =========================================================

function drawBullets() {

    for (
        const bullet
        of bullets
    ) {

        if (
            bulletImg.complete &&
            bulletImg.naturalWidth > 0
        ) {

            ctx.drawImage(

                bulletImg,

                bullet.x - 10,

                bullet.y - 10,

                20,

                20

            );

        }

        else {

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

        }

    }

}


// =========================================================
// 이펙트 그리기
// =========================================================

function drawEffects() {

    for (
        const effect
        of effects
    ) {

        const alpha =
            effect.life /
            effect.maxLife;


        ctx.globalAlpha =
            alpha;


        if (
            hitImg.complete &&
            hitImg.naturalWidth > 0
        ) {

            const size =
                effect.size *
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

        }

        else {

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

        }


        ctx.globalAlpha = 1;

    }

}


// =========================================================
// UI 업데이트
// =========================================================

function updateUI() {

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


    const boss =
        enemies.find(
            e => e.type === "boss"
        );


    if (boss) {

        document.getElementById(
            "bossBar"
        ).style.width =

            Math.max(
                0,
                boss.hp /
                boss.maxHp *
                100
            )

            + "%";

    }

}


// =========================================================
// 게임 루프
// =========================================================

function gameLoop(time) {

    if (
        !gameRunning
    ) {

        return;

    }


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

    updateBossProjectiles(dt);

    updateEffects(dt);

    updateStage(dt);


    if (
        player.hp <= 0
    ) {

        gameOver();

        return;

    }


    drawBackground();

    drawBullets();


    for (
        const enemy
        of enemies
    ) {

        drawEnemy(enemy);

    }


    drawBossProjectiles();

    drawEffects();

    drawPlayer();

    updateUI();


    requestAnimationFrame(
        gameLoop
    );

}


// =========================================================
// 시작
// =========================================================

updateUI();

resizeCanvas();


function resizeCanvas() {

    const width =
        Math.min(
            1000,
            window.innerWidth - 20
        );


    canvas.style.width =
        width + "px";

}


window.addEventListener(
    "resize",
    resizeCanvas
);


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
    "__NORMAL__",
    images["normal"]
)

html = html.replace(
    "__TANK__",
    images["tank"]
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
    "__HIT__",
    images["hit"]
)


# =========================================================
# Streamlit 실행
# =========================================================

components.html(
    html,
    height=700,
    scrolling=False
)
