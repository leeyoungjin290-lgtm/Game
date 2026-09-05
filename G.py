import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="PT Survival",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 이미지 -> Base64
# --------------------------------------------------

IMAGE_FILES = [
    "player.png",
    "enemy_normal.png",
    "enemy_tank.png",
    "boss.png",
    "background.png",
    "bullet.png",
    "hit_effect.png"
]

def load_image(filename):
    if not os.path.exists(filename):
        return ""

    with open(filename, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    return f"data:image/png;base64,{data}"


images = {}

for filename in IMAGE_FILES:
    images[filename] = load_image(filename)


# --------------------------------------------------
# HTML / CSS / JavaScript
# --------------------------------------------------

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    background: #10131a;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}}

#gameWrapper {{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

#gameContainer {{
    position: relative;
    width: 1000px;
    max-width: 100%;
}}

canvas {{
    width: 100%;
    display: block;
    background: #222;
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0,0,0,0.5);
}}

#ui {{
    position: absolute;
    top: 15px;
    left: 15px;
    right: 15px;
    pointer-events: none;
    z-index: 10;
}}

.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.panel {{
    background: rgba(0,0,0,0.65);
    padding: 10px 15px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}}

#hpBarOuter {{
    width: 250px;
    height: 18px;
    background: #333;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 5px;
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
    background: rgba(0,0,0,0.82);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 20;
}}

.menuBox {{
    width: 520px;
    max-width: 90%;
    background: #171b25;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #414858;
    box-shadow: 0 0 40px rgba(0,0,0,0.7);
}}

.menuBox h1 {{
    font-size: 42px;
    margin: 0 0 10px;
}}

.menuBox p {{
    color: #b9c0cc;
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
    margin: 10px auto;
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

<canvas id="gameCanvas" width="1000" height="650"></canvas>

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
            <div>🎯 Stage: <span id="stageText">1 / 6</span></div>
            <div>⭐ PT: <span id="ptText">0</span></div>
            <div>👾 Enemies: <span id="enemyText">0</span></div>
        </div>

    </div>

</div>

<div id="message"></div>

<div id="menu">

    <div class="menuBox" id="startMenu">

        <h1>PT SURVIVAL</h1>

        <p>
            몰려오는 적들을 처치하고 PT를 획득하세요.
            <br>
            6스테이지의 보스를 쓰러뜨리면 최종 점수가 결정됩니다.
        </p>

        <p>
            🖱️ 마우스: 조준<br>
            🔫 자동 공격<br>
            ❤️ 적에게 닿으면 피해
        </p>

        <button onclick="startGame()">게임 시작</button>

    </div>

</div>

</div>

</div>


<script>

// ==================================================
// 이미지
// ==================================================

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


const playerImg = makeImage(IMG.player);
const normalImg = makeImage(IMG.normal);
const tankImg = makeImage(IMG.tank);
const bossImg = makeImage(IMG.boss);
const backgroundImg = makeImage(IMG.background);
const bulletImg = makeImage(IMG.bullet);
const hitImg = makeImage(IMG.hit);


// ==================================================
// Canvas
// ==================================================

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");


// ==================================================
// 게임 변수
// ==================================================

let gameRunning = false;

let stage = 1;

let totalPT = 0;

let stagePT = 0;

let enemies = [];

let bullets = [];

let effects = [];

let lastTime = 0;

let spawnTimer = 0;

let stageTimer = 0;

let attackTimer = 0;

let mouseX = 500;

let mouseY = 325;

let keys = {{}};


// ==================================================
// 플레이어
// ==================================================

let player = {{

    x: 500,
    y: 520,

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


// ==================================================
// 스테이지 설정
// ==================================================

const stages = {{

    1: {{
        duration: 25,
        spawnRate: 1.1,
        normalHp: 40,
        normalSpeed: 80,
        tankHp: 120,
        tankSpeed: 45
    }},

    2: {{
        duration: 30,
        spawnRate: 0.9,
        normalHp: 55,
        normalSpeed: 95,
        tankHp: 160,
        tankSpeed: 50
    }},

    3: {{
        duration: 35,
        spawnRate: 0.75,
        normalHp: 75,
        normalSpeed: 110,
        tankHp: 220,
        tankSpeed: 55
    }},

    4: {{
        duration: 40,
        spawnRate: 0.65,
        normalHp: 100,
        normalSpeed: 120,
        tankHp: 300,
        tankSpeed: 60
    }},

    5: {{
        duration: 45,
        spawnRate: 0.55,
        normalHp: 130,
        normalSpeed: 135,
        tankHp: 400,
        tankSpeed: 65
    }},

    6: {{
        duration: 999999,
        spawnRate: 0.8,
        normalHp: 180,
        normalSpeed: 140,
        tankHp: 500,
        tankSpeed: 70
    }}

}};


// ==================================================
// 마우스
// ==================================================

canvas.addEventListener("mousemove", function(e) {{

    const rect = canvas.getBoundingClientRect();

    mouseX = (e.clientX - rect.left) * canvas.width / rect.width;

    mouseY = (e.clientY - rect.top) * canvas.height / rect.height;

}});


// ==================================================
// 키보드
// ==================================================

window.addEventListener("keydown", function(e) {{

    keys[e.key.toLowerCase()] = true;

}});

window.addEventListener("keyup", function(e) {{

    keys[e.key.toLowerCase()] = false;

}});


// ==================================================
// 게임 시작
// ==================================================

function startGame() {{

    document.getElementById("menu").classList.add("hidden");

    stage = 1;

    totalPT = 0;

    stagePT = 0;

    enemies = [];

    bullets = [];

    effects = [];

    player.hp = player.maxHp;

    player.x = canvas.width / 2;

    player.y = canvas.height - 100;

    gameRunning = true;

    stageTimer = 0;

    spawnTimer = 0;

    attackTimer = 0;

    lastTime = performance.now();

    requestAnimationFrame(gameLoop);

}}


// ==================================================
// 적 생성
// ==================================================

function spawnEnemy() {{

    const setting = stages[stage];

    let type;

    const tankChance = Math.min(0.15 + stage * 0.04, 0.35);

    if (Math.random() < tankChance) {{
        type = "tank";
    }} else {{
        type = "normal";
    }}

    let x = Math.random() * (canvas.width - 80) + 40;

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

    }} else {{

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


// ==================================================
// 보스 생성
// ==================================================

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

}}


// ==================================================
// 총알 발사
// ==================================================

function shoot() {{

    const dx = mouseX - player.x;

    const dy = mouseY - player.y;

    const length = Math.sqrt(dx * dx + dy * dy);

    if (length === 0) return;

    const vx = dx / length * player.bulletSpeed;

    const vy = dy / length * player.bulletSpeed;

    let damage = player.attack;

    let critical = false;

    if (Math.random() < player.critChance) {{

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


// ==================================================
// 충돌
// ==================================================

function collision(a, b) {{

    return (

        Math.abs(a.x - b.x) < (a.width + b.width) / 2 &&

        Math.abs(a.y - b.y) < (a.height + b.height) / 2

    );

}}


// ==================================================
// 피격 효과
// ==================================================

function createEffect(x, y) {{

    effects.push({{

        x: x,

        y: y,

        life: 0.3,

        maxLife: 0.3

    }});

}}


// ==================================================
// 플레이어 이동
// ==================================================

function updatePlayer(dt) {{

    let dx = 0;
    let dy = 0;

    if (keys["w"] || keys["arrowup"]) dy -= 1;

    if (keys["s"] || keys["arrowdown"]) dy += 1;

    if (keys["a"] || keys["arrowleft"]) dx -= 1;

    if (keys["d"] || keys["arrowright"]) dx += 1;

    if (dx !== 0 || dy !== 0) {{

        const len = Math.sqrt(dx * dx + dy * dy);

        dx /= len;
        dy /= len;

        player.x += dx * player.speed * dt;

        player.y += dy * player.speed * dt;

    }}

    player.x = Math.max(35, Math.min(canvas.width - 35, player.x));

    player.y = Math.max(35, Math.min(canvas.height - 35, player.y));

    if (player.invincible > 0) {{
        player.invincible -= dt;
    }}

}}


// ==================================================
// 총알 업데이트
// ==================================================

function updateBullets(dt) {{

    for (let i = bullets.length - 1; i >= 0; i--) {{

        const b = bullets[i];

        b.x += b.vx * dt;

        b.y += b.vy * dt;

        let removeBullet = false;

        for (let j = enemies.length - 1; j >= 0; j--) {{

            const e = enemies[j];

            if (collision(

                {{

                    x: b.x,
                    y: b.y,
                    width: b.size,
                    height: b.size

                }},

                e

            )) {{

                e.hp -= b.damage;

                createEffect(b.x, b.y);

                removeBullet = true;

                if (e.hp <= 0) {{

                    totalPT += e.pt;

                    stagePT += e.pt;

                    createEffect(e.x, e.y);

                    enemies.splice(j, 1);

                }}

                break;

            }}

        }}

        if (

            b.x < -50 ||

            b.x > canvas.width + 50 ||

            b.y < -50 ||

            b.y > canvas.height + 50

        ) {{

            removeBullet = true;

        }}

        if (removeBullet) {{
            bullets.splice(i, 1);
        }}

    }}

}}


// ==================================================
// 적 업데이트
// ==================================================

function updateEnemies(dt) {{

    for (let i = enemies.length - 1; i >= 0; i--) {{

        const e = enemies[i];

        const dx = player.x - e.x;

        const dy = player.y - e.y;

        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > 1) {{

            e.x += dx / distance * e.speed * dt;

            e.y += dy / distance * e.speed * dt;

        }}

        if (collision(e, player)) {{

            if (player.invincible <= 0) {{

                player.hp -= e.damage;

                player.invincible = 0.5;

                createEffect(player.x, player.y);

                if (e.type !== "boss") {{
                    enemies.splice(i, 1);
                }}

                if (player.hp <= 0) {{
                    gameOver();
                }}

            }}

        }}

    }}

}}


// ==================================================
// 이펙트
// ==================================================

function updateEffects(dt) {{

    for (let i = effects.length - 1; i >= 0; i--) {{

        effects[i].life -= dt;

        if (effects[i].life <= 0) {{
            effects.splice(i, 1);
        }}

    }}

}}


// ==================================================
// 공격
// ==================================================

function updateAttack(dt) {{

    attackTimer -= dt;

    if (attackTimer <= 0) {{

        shoot();

        attackTimer = player.attackSpeed;

    }}

}}


// ==================================================
// 스테이지 진행
// ==================================================

function updateStage(dt) {{

    stageTimer += dt;

    spawnTimer -= dt;

    const setting = stages[stage];

    if (stage < 6) {{

        if (spawnTimer <= 0) {{

            spawnEnemy();

            spawnTimer = setting.spawnRate;

        }}

        if (stageTimer >= setting.duration) {{

            if (enemies.length === 0) {{

                finishStage();

            }}

        }}

    }}

    else {{

        // 6스테이지 시작 시 보스가 없으면 생성

        const bossExists = enemies.some(e => e.type === "boss");

        if (!bossExists) {{

            const normalEnemies = enemies.filter(e => e.type !== "boss");

            if (stageTimer > 2 && normalEnemies.length < 5) {{
                spawnBoss();
            }}

        }}

    }}

}}


// ==================================================
// 스테이지 종료
// ==================================================

function finishStage() {{

    gameRunning = false;

    showUpgradeMenu();

}}


// ==================================================
// 강화 메뉴
// ==================================================

function showUpgradeMenu() {{

    const menu = document.getElementById("menu");

    menu.classList.remove("hidden");

    document.getElementById("startMenu").innerHTML = `

        <h1>STAGE ${{stage}} CLEAR!</h1>

        <p>이번 스테이지 획득 PT: <b>${{stagePT}}</b></p>

        <p>현재 총 PT: <b>${{totalPT}}</b></p>

        <hr>

        <button class="upgrade" onclick="upgradeAttack()">
            ⚔️ 공격력 강화
            <span>100 PT</span>
        </button>

        <button class="upgrade" onclick="upgradeSpeed()">
            🔫 공격 속도 강화
            <span>150 PT</span>
        </button>

        <button class="upgrade" onclick="upgradeCrit()">
            💥 치명타 확률 강화
            <span>200 PT</span>
        </button>

        <button class="upgrade" onclick="upgradeHp()">
            ❤️ 최대 체력 강화
            <span>250 PT</span>
        </button>

        <br>

        <button onclick="nextStage()">
            다음 스테이지 →
        </button>

    `;

}}


// ==================================================
// 공격력 강화
// ==================================================

function upgradeAttack() {{

    if (totalPT >= 100) {{

        totalPT -= 100;

        player.attack += 10;

        showUpgradeMenu();

    }}

}}


// ==================================================
// 공격 속도 강화
// ==================================================

function upgradeSpeed() {{

    if (totalPT >= 150) {{

        totalPT -= 150;

        player.attackSpeed = Math.max(
            0.08,
            player.attackSpeed - 0.04
        );

        showUpgradeMenu();

    }}

}}


// ==================================================
// 치명타 강화
// ==================================================

function upgradeCrit() {{

    if (totalPT >= 200) {{

        totalPT -= 200;

        player.critChance = Math.min(
            0.75,
            player.critChance + 0.05
        );

        showUpgradeMenu();

    }}

}}


// ==================================================
// 체력 강화
// ==================================================

function upgradeHp() {{

    if (totalPT >= 250) {{

        totalPT -= 250;

        player.maxHp += 25;

        player.hp = player.maxHp;

        showUpgradeMenu();

    }}

}}


// ==================================================
// 다음 스테이지
// ==================================================

function nextStage() {{

    stage++;

    stagePT = 0;

    stageTimer = 0;

    spawnTimer = 0;

    enemies = [];

    bullets = [];

    player.hp = player.maxHp;

    player.x = canvas.width / 2;

    player.y = canvas.height - 100;

    document.getElementById("menu").classList.add("hidden");

    gameRunning = true;

    lastTime = performance.now();

    requestAnimationFrame(gameLoop);

}}


// ==================================================
// 보스 사망 확인
// ==================================================

function checkBossDeath() {{

    if (stage !== 6) return;

    const boss = enemies.find(e => e.type === "boss");

    if (!boss) {{

        finalGame();

    }}

}}


// ==================================================
// 최종 게임 클리어
// ==================================================

function finalGame() {{

    gameRunning = false;

    enemies = [];

    bullets = [];

    document.getElementById("menu").classList.remove("hidden");

    document.getElementById("startMenu").innerHTML = `

        <h1>🏆 GAME CLEAR!</h1>

        <p>
            최종 보스를 처치했습니다!
        </p>

        <hr>

        <h2>
            FINAL SCORE
        </h2>

        <h1 style="font-size:55px;">
            ${{totalPT}} PT
        </h1>

        <p>
            지금까지 획득한 PT를 기준으로 계산된 최종 점수입니다.
        </p>

        <button onclick="location.reload()">
            다시 시작
        </button>

    `;

}}


// ==================================================
// 게임 오버
// ==================================================

function gameOver() {{

    gameRunning = false;

    document.getElementById("menu").classList.remove("hidden");

    document.getElementById("startMenu").innerHTML = `

        <h1>GAME OVER</h1>

        <p>
            Stage ${{stage}}에서 쓰러졌습니다.
        </p>

        <h2>
            획득 PT: ${{totalPT}}
        </h2>

        <button onclick="location.reload()">
            다시 시작
        </button>

    `;

}}


// ==================================================
// 화면 그리기
// ==================================================

function drawBackground() {{

    if (backgroundImg.complete && backgroundImg.naturalWidth > 0) {{

        ctx.drawImage(
            backgroundImg,
            0,
            0,
            canvas.width,
            canvas.height
        );

    }}
    else {{

        ctx.fillStyle = "#17202b";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

    }}

}}


// ==================================================
// 플레이어 그리기
// ==================================================

function drawPlayer() {{

    if (
        playerImg.complete &&
        playerImg.naturalWidth > 0
    ) {{

        if (
            player.invincible > 0 &&
            Math.floor(player.invincible * 20) % 2 === 0
        ) {{
            return;
        }}

        ctx.drawImage(

            playerImg,

            player.x - player.width / 2,

            player.y - player.height / 2,

            player.width,

            player.height

        );

    }}
    else {{

        ctx.fillStyle = "#4da6ff";

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


// ==================================================
// 적 그리기
// ==================================================

function drawEnemy(e) {{

    let img;

    if (e.type === "normal") {{
        img = normalImg;
    }}
    else if (e.type === "tank") {{
        img = tankImg;
    }}
    else {{
        img = bossImg;
    }}

    if (img.complete && img.naturalWidth > 0) {{

        ctx.drawImage(

            img,

            e.x - e.width / 2,

            e.y - e.height / 2,

            e.width,

            e.height

        );

    }}
    else {{

        ctx.fillStyle =
            e.type === "boss"
            ? "#b000ff"
            : e.type === "tank"
            ? "#777"
            : "#ff4444";

        ctx.beginPath();

        ctx.arc(
            e.x,
            e.y,
            e.width / 2,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }}

    // HP 바

    if (e.type !== "boss") {{

        const barWidth = e.width;

        const hpRatio = Math.max(
            0,
            e.hp / e.maxHp
        );

        ctx.fillStyle = "#222";

        ctx.fillRect(
            e.x - barWidth / 2,
            e.y - e.height / 2 - 10,
            barWidth,
            6
        );

        ctx.fillStyle = "#39d353";

        ctx.fillRect(
            e.x - barWidth / 2,
            e.y - e.height / 2 - 10,
            barWidth * hpRatio,
            6
        );

    }}

}}


// ==================================================
// 보스 HP
// ==================================================

function drawBossHP() {{

    const boss = enemies.find(e => e.type === "boss");

    if (!boss) return;

    const width = 600;

    const height = 22;

    const x = canvas.width / 2 - width / 2;

    const y = 70;

    ctx.fillStyle = "#222";

    ctx.fillRect(
        x,
        y,
        width,
        height
    );

    ctx.fillStyle = "#c43cff";

    ctx.fillRect(
        x,
        y,
        width * Math.max(0, boss.hp / boss.maxHp),
        height
    );

    ctx.strokeStyle = "white";

    ctx.strokeRect(
        x,
        y,
        width,
        height
    );

    ctx.fillStyle = "white";

    ctx.font = "bold 16px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "BOSS HP",
        canvas.width / 2,
        y - 7
    );

}}


// ==================================================
// 총알 그리기
// ==================================================

function drawBullets() {{

    for (const b of bullets) {{

        if (
            bulletImg.complete &&
            bulletImg.naturalWidth > 0
        ) {{

            ctx.drawImage(

                bulletImg,

                b.x - 10,

                b.y - 10,

                20,

                20

            );

        }}
        else {{

            ctx.fillStyle =
                b.critical
                ? "#ffd700"
                : "#ffffff";

            ctx.beginPath();

            ctx.arc(
                b.x,
                b.y,
                7,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }}

    }}

}}


// ==================================================
// 이펙트 그리기
// ==================================================

function drawEffects() {{

    for (const e of effects) {{

        const alpha =
            e.life / e.maxLife;

        ctx.globalAlpha = alpha;

        if (
            hitImg.complete &&
            hitImg.naturalWidth > 0
        ) {{

            const size = 80 * (1 - alpha * 0.3);

            ctx.drawImage(

                hitImg,

                e.x - size / 2,

                e.y - size / 2,

                size,
                size

            );

        }}
        else {{

            ctx.fillStyle = "#ffffff";

            ctx.beginPath();

            ctx.arc(
                e.x,
                e.y,
                35 * (1 - alpha),
                0,
                Math.PI * 2
            );

            ctx.fill();

        }}

        ctx.globalAlpha = 1;

    }}

}}


// ==================================================
// UI
// ==================================================

function updateUI() {{

    document.getElementById("hpText").textContent =
        Math.max(0, Math.floor(player.hp))
        + " / "
        + player.maxHp;

    document.getElementById("hpBar").style.width =
        Math.max(
            0,
            player.hp / player.maxHp * 100
        )
        + "%";

    document.getElementById("stageText").textContent =
        stage + " / 6";

    document.getElementById("ptText").textContent =
        totalPT;

    document.getElementById("enemyText").textContent =
        enemies.length;

}}


// ==================================================
// 게임 루프
// ==================================================

function gameLoop(time) {{

    if (!gameRunning) return;

    let dt = (time - lastTime) / 1000;

    dt = Math.min(dt, 0.05);

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

    for (const e of enemies) {{
        drawEnemy(e);
    }}

    drawEffects();

    drawPlayer();

    drawBossHP();

    updateUI();

    requestAnimationFrame(gameLoop);

}}


// ==================================================
// 화면 크기 대응
// ==================================================

function resizeCanvas() {{

    const container =
        document.getElementById("gameContainer");

    const width =
        Math.min(
            1000,
            window.innerWidth - 20
        );

    canvas.style.width = width + "px";

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


# --------------------------------------------------
# Streamlit에 게임 표시
# --------------------------------------------------

components.html(
    html,
    height=700,
    scrolling=False
)
