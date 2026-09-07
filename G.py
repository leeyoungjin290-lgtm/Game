import streamlit as st
import streamlit.components.v1 as components
import base64
import os


                                                           
              
                                                           

st.set_page_config(
    page_title="PT Survival",
    page_icon="🎮",
    layout="wide"
)


                                                           
       
                                                           

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


                                                           
          
                                                           

def load_image(filename):

    path = os.path.join(
        BASE_DIR,
        filename
    )

    if not os.path.exists(path):
        return ""

    with open(path, "rb") as f:

        encoded = base64.b64encode(
            f.read()
        ).decode("utf-8")

    return (
        "data:image/png;base64,"
        + encoded
    )


                                                           
          
                                                           

def load_audio(filename):

    path = os.path.join(
        BASE_DIR,
        filename
    )

    if not os.path.exists(path):
        return ""

    with open(path, "rb") as f:

        encoded = base64.b64encode(
            f.read()
        ).decode("utf-8")

    return (
        "data:audio/mpeg;base64,"
        + encoded
    )


                                                           
     
                                                           

images = {

    "player":
        load_image("player.png"),

    "normal":
        load_image("enemy_normal.png"),

    "tank":
        load_image("enemy_tank.png"),

    "boss":
        load_image("boss.png"),

    "bossAttack":
        load_image("boss_attack.png"),

                  
    "bossShuriken":
        load_image("boss_shuriken.png"),

    "bossBlade":
        load_image("boss_blade.png"),

    "bossNova":
        load_image("boss_nova.png"),

    "bossSweep":
        load_image("boss_sweep.png"),

    "bossVortex":
        load_image("boss_vortex.png"),

    "background":
        load_image("background.png"),

    "bullet":
        load_image("bullet.png"),

    "hit":
        load_image("hit_effect.png")
}


                                                           
     
                                                           

bgm = load_audio("song.mp3")


                                                           
      
                                                           

html = """

<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">


<style>

/* ========================================================
   기본
======================================================== */

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


/* ========================================================
   게임 영역
======================================================== */

#gameWrapper {

    width: 100%;

    display: flex;

    justify-content: center;

}


#gameContainer {

    position: relative;

    width: 1000px;

    height: 650px;

}


/* ========================================================
   Canvas
======================================================== */

canvas {

    display: block;

    width: 1000px;

    height: 650px;

    background: #222;

    cursor: crosshair;

}


/* ========================================================
   UI
======================================================== */

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

    background:
        rgba(0, 0, 0, 0.68);

    padding: 10px 15px;

    border-radius: 10px;

    border:
        1px solid
        rgba(255,255,255,0.15);

}


/* ========================================================
   HP
======================================================== */

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


/* ========================================================
   보스 HP
======================================================== */

#bossBarOuter {

    position: absolute;

    top: 70px;

    left: 50%;

    transform:
        translateX(-50%);

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


#skillUI {
    position: absolute;
    left: 50%;
    bottom: 12px;
    transform: translateX(-50%);
    min-width: 150px;
    padding: 10px 14px;
    border: 2px solid rgba(255,255,255,0.35);
    border-radius: 10px;
    background: rgba(0,0,0,0.55);
    color: white;
    text-align: center;
    font-weight: bold;
    z-index: 10;
}

#skillUI.skill-ready {
    border-color: #ffffff;
}

#skillUI.skill-cooldown {
    opacity: 0.75;
}

#skillUI.skill-locked {
    opacity: 0.45;
}

.skill-name {
    font-size: 15px;
    margin-bottom: 4px;
}

#skillCooldownText {
    font-size: 13px;
}

#bossText {

    position: absolute;

    top: 48px;

    left: 50%;

    transform:
        translateX(-50%);

    font-weight: bold;

    display: none;

    z-index: 10;

}


/* ========================================================
   메뉴
======================================================== */

#menu {

    position: absolute;

    inset: 0;

    z-index: 20;

    display: flex;

    justify-content: center;

    align-items: center;

    background:
        rgba(0,0,0,0.82);

}


.menuBox {

    width: 520px;

    max-width: 90%;

    padding: 35px;

    background: #171b25;

    border-radius: 18px;

    text-align: center;

    border:
        1px solid #414858;

    box-shadow:
        0 0 40px
        rgba(0,0,0,0.7);

}


.menuBox h1 {

    font-size: 42px;

    margin:
        0 0 15px;

}


.menuBox p {

    color: #b9c0cc;

    line-height: 1.6;

}


/* ========================================================
   버튼
======================================================== */

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


/* ========================================================
   메시지
======================================================== */

#message {

    position: absolute;

    top: 45%;

    left: 50%;

    transform:
        translate(-50%, -50%);

    font-size: 36px;

    font-weight: bold;

    text-align: center;

    text-shadow:
        0 3px 10px black;

    pointer-events: none;

    z-index: 15;

}

</style>

</head>


<body>


<!-- ======================================================
     BGM
====================================================== -->

<audio
    id="gameBGM"
    src="__BGM__"
    loop
    preload="auto">
</audio>

<audio
    id="bossBGM"
    src="__BOSS_BGM__"
    loop
    preload="auto">
</audio>


<!-- ======================================================
     게임
====================================================== -->

<div id="gameWrapper">

<div id="gameContainer">


<canvas
    id="gameCanvas"
    width="1000"
    height="650">
</canvas>


<!-- ======================================================
     UI
====================================================== -->

<div id="ui">

<div class="topbar">


<div class="panel">

<div>

❤️ HP:

<span id="hpText">
100 / 100
</span>

</div>


<div id="hpBarOuter">

<div id="hpBar"></div>

</div>

</div>


<div class="panel">

<div>

🎯 Stage:

<span id="stageText">
1 / 6
</span>

</div>


<div>

⭐ PT:

<span id="ptText">
0
</span>

</div>


<div>

👾 Enemies:

<span id="enemyText">
0
</span>

</div>

</div>


</div>

<div id="skillUI" class="skill-locked">

    <div class="skill-name">마력폭주 [E]</div>

    <div id="skillCooldownText">LOCKED</div>

</div>

</div>


<!-- ======================================================
     보스 HP
====================================================== -->

<div id="bossText">
BOSS HP
</div>


<div id="bossBarOuter">

<div id="bossBar"></div>

</div>


<div id="message"></div>


<!-- ======================================================
     메뉴
====================================================== -->

<div id="menu">

<div
    class="menuBox"
    id="startMenu">


<h1>
🚀 PT SURVIVAL
</h1>


<p>

몰려오는 적들을 처치하고
PT를 획득하세요.

<br>

스테이지가 끝날 때마다
PT를 사용해 능력을 강화하세요.

<br>

6스테이지의 보스를
처치하면 게임 클리어입니다.

</p>


<p>

🖱️ 마우스 : 조준

<br>

🔫 자동 공격

<br>

⌨️ WASD / 방향키 : 이동

<br>

🎵 게임 시작 시 BGM 재생

</p>


<button
    id="startButton"
    type="button">

게임 시작

</button>


</div>

</div>


</div>

</div>


<script>


// ========================================================
// 이미지
// ========================================================

const IMG = {

    player:
        "__PLAYER__",

    normal:
        "__NORMAL__",

    tank:
        "__TANK__",

    boss:
        "__BOSS__",

    bossAttack:
        "__BOSS_ATTACK__",

    bossShuriken:
        "__BOSS_SHURIKEN__",

    bossBlade:
        "__BOSS_BLADE__",

    bossNova:
        "__BOSS_NOVA__",

    bossSweep:
        "__BOSS_SWEEP__",

    bossVortex:
        "__BOSS_VORTEX__",

    background:
        "__BACKGROUND__",

    bullet:
        "__BULLET__",

    hit:
        "__HIT__"

};


function makeImage(src) {

    const image =
        new Image();

    if (src) {

        image.src = src;

    }

    return image;

}


const playerImg =
    makeImage(IMG.player);

const normalImg =
    makeImage(IMG.normal);

const tankImg =
    makeImage(IMG.tank);

const bossImg =
    makeImage(IMG.boss);

const bossAttackImg =
    makeImage(IMG.bossAttack);

const bossShurikenImg =
    makeImage(IMG.bossShuriken);

const bossBladeImg =
    makeImage(IMG.bossBlade);

const bossNovaImg =
    makeImage(IMG.bossNova);

const bossSweepImg =
    makeImage(IMG.bossSweep);

const bossVortexImg =
    makeImage(IMG.bossVortex);

const backgroundImg =
    makeImage(IMG.background);

const bulletImg =
    makeImage(IMG.bullet);

const hitImg =
    makeImage(IMG.hit);


// ========================================================
// Canvas
// ========================================================

const canvas =
    document.getElementById(
        "gameCanvas"
    );


if (!canvas) {
    throw new Error("gameCanvas를 찾을 수 없습니다.");
}

const ctx =
    canvas.getContext("2d");


// ========================================================
// 게임 변수
// ========================================================

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

// ========================================================
// 마력폭주 스킬
// ========================================================

let magicBurstUnlocked = false;
let magicBurstCooldown = 0;
const magicBurstMaxCooldown = 2;


// ========================================================
// 게임 상태 / 입력 / 생성 / 시작
// ========================================================

const keys = {};
let mouseX = canvas.width / 2;
let mouseY = canvas.height / 2;

const player = {
    x: canvas.width / 2,
    y: canvas.height - 100,
    width: 60,
    height: 60,
    speed: 300,
    hp: 100,
    maxHp: 100,
    attack: 20,
    attackSpeed: 0.35,
    bulletSpeed: 650,
    critChance: 0.10,
    critDamage: 2.0,
    invincible: 0
};

const stages = {
    1: { duration: 20, spawnRate: 1.00, normalHp: 45, tankHp: 130 },
    2: { duration: 25, spawnRate: 0.90, normalHp: 65, tankHp: 180 },
    3: { duration: 30, spawnRate: 0.82, normalHp: 90, tankHp: 240 },
    // 4스테이지부터 체력 크게 증가
    4: { duration: 35, spawnRate: 0.72, normalHp: 180, tankHp: 520 },
    5: { duration: 40, spawnRate: 0.62, normalHp: 280, tankHp: 760 },
    6: { duration: 0, spawnRate: 0, normalHp: 0, tankHp: 0 }
};

let bossSpawned = false;
let bossAttackTimer = 1.5;
let bossAttackSpeed = 250;
let bossAttackSpeedTimer = 2;
let bossPatternIndex = 0;

// ========================================================
// 보스 공격 설정
// 기본 공격은 계속 발사하고, 스킬은 2초마다 1회 사용
// ========================================================
let bossBasicShotTimer = 0;
let bossSkillTimer = 2.0;
const bossBasicShotInterval = 0.36;
const bossSkillInterval = 5.0;

function rand(min, max) {
    return min + Math.random() * (max - min);
}

function spawnEnemy() {

    const setting = stages[stage];
    if (!setting || stage >= 6) return;

    const tankChance = Math.min(0.35, 0.12 + stage * 0.045);
    const isTank = Math.random() < tankChance;

    const type = isTank ? "tank" : "normal";

    const margin = 50;
    let x, y;

    const side = Math.floor(Math.random() * 4);

    if (side === 0) {
        x = rand(margin, canvas.width - margin);
        y = -40;
    } else if (side === 1) {
        x = canvas.width + 40;
        y = rand(margin, canvas.height - margin);
    } else if (side === 2) {
        x = rand(margin, canvas.width - margin);
        y = canvas.height + 40;
    } else {
        x = -40;
        y = rand(margin, canvas.height - margin);
    }

    const hp = isTank ? setting.tankHp : setting.normalHp;

    enemies.push({
        type,
        x,
        y,
        width: isTank ? 72 : 48,
        height: isTank ? 72 : 48,
        hp,
        maxHp: hp,
        speed: isTank ? 42 + stage * 3 : 72 + stage * 6,
        damage: isTank ? 18 + stage * 2 : 8 + stage,
        pt: isTank ? 35 + stage * 5 : 12 + stage * 2,
        attackFlash: 0
    });
}

function spawnBoss() {

    if (bossSpawned) return;

    bossSpawned = true;

    const hp = 300000;

    enemies.push({
        type: "boss",
        x: canvas.width / 2,
        y: 145,
        width: 145,
        height: 145,
        hp,
        maxHp: hp,
        speed: 0,
        moveSpeed: 30,
        targetX: canvas.width / 2,
        targetY: 145,
        moveTimer: 0.8,
        damage: 28,
        pt: 1000,
        attackFlash: 0
    });

    bossAttackTimer = 1.5;
    bossAttackSpeed = 250;
    bossAttackSpeedTimer = 2;
    bossBasicShotTimer = 0;
    bossSkillTimer = bossSkillInterval;

    document.getElementById("bossBarOuter").style.display = "block";
    document.getElementById("bossText").style.display = "block";
}

function resetGameState() {

    gameRunning = false;
    stage = 1;
    totalPT = 0;
    stagePT = 0;
    totalEarnedPT = 0;

    enemies = [];
    bullets = [];
    bossProjectiles = [];
    effects = [];

    spawnTimer = 0;
    stageTimer = 0;
    attackTimer = 0;

    magicBurstUnlocked = false;
    magicBurstCooldown = 0;

    bossSpawned = false;
    bossAttackTimer = 1.5;
    bossAttackSpeed = 250;
    bossAttackSpeedTimer = 2;
    bossBasicShotTimer = 0;
    bossSkillTimer = bossSkillInterval;
    bossPatternIndex = 0;

    player.x = canvas.width / 2;
    player.y = canvas.height - 100;
    player.hp = player.maxHp;
    player.invincible = 0;

    mouseX = canvas.width / 2;
    mouseY = canvas.height / 2;

    document.getElementById("bossBarOuter").style.display = "none";
    document.getElementById("bossText").style.display = "none";
}


function skipToBossUpgrade() {
    // 1스테이지에서 M을 누르면 5000 PT를 지급하고
    // 5스테이지 클리어 화면을 거친 뒤 직접 6스테이지로 갈 수 있게 합니다.
    if (!gameRunning || stage !== 1) {
        return;
    }

    totalPT = 5000;
    stagePT = 5000;
    totalEarnedPT = Math.max(totalEarnedPT, 5000);

    // M키 스킵 시 마력폭주 스킬도 바로 해금
    magicBurstUnlocked = true;
    magicBurstCooldown = 0;

    stage = 5;
    stageTimer = 0;

    // 일반 적/투사체를 모두 정리하고 5스테이지 클리어 화면 표시
    enemies = [];
    bullets = [];
    bossProjectiles = [];
    effects = [];

    finishStage();
}

function startGame() {

    resetGameState();

    const menu =
        document.getElementById("menu");

    if (menu) {
        menu.classList.add("hidden");
    }

    gameRunning = true;
    lastTime = performance.now();

    updateUI();
    requestAnimationFrame(gameLoop);

    // 브라우저 자동재생 정책상 사용자 클릭 안에서 재생을 시도합니다.
    const audio = document.getElementById("gameBGM");
    const bossAudio = document.getElementById("bossBGM");

    if (bossAudio) {
        bossAudio.pause();
        bossAudio.currentTime = 0;
    }

    if (audio) {
        audio.currentTime = 0;
        audio.volume = 0.45;
        audio.play().catch(() => {});
    }
}

const startButton =
    document.getElementById("startButton");

if (startButton) {
    startButton.addEventListener(
        "click",
        function(e) {
            e.preventDefault();
            startGame();
        }
    );
}

window.addEventListener("keydown", function(e) {

    const key = e.key.toLowerCase();

    if (key === "m" && !e.repeat && stage === 1 && gameRunning) {
        e.preventDefault();
        skipToBossUpgrade();
        return;
    }

    keys[key] = true;

    if (
        key === "e" &&
        !e.repeat
    ) {
        useMagicBurst();
    }

    if (
        [
            "arrowup",
            "arrowdown",
            "arrowleft",
            "arrowright",
            " "
        ].includes(key)
    ) {
        e.preventDefault();
    }

});

window.addEventListener("keyup", function(e) {
    keys[e.key.toLowerCase()] = false;
});

canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    mouseX =
        (e.clientX - rect.left) *
        canvas.width / rect.width;

    mouseY =
        (e.clientY - rect.top) *
        canvas.height / rect.height;
});

canvas.addEventListener("mouseleave", function() {
    mouseX = player.x;
    mouseY = player.y;
});


// ========================================================
// 보스 공격 패턴
// ========================================================
// 보스가 랜덤하게 여러 공격을 사용합니다.
//
// 1. VOID BOLT       : 조준 탄환
// 2. SHURIKEN BURST  : 표창 10방향
// 3. BLADE RAIN      : 위에서 검/창 낙하
// 4. VOID BEAM       : 긴 직선 레이저
// 5. VOID NOVA       : 보스 주변 원형 충격파
// 6. GROUND SPIKE    : 플레이어 위치에 지연 후 폭발
// 7. CRESCENT SWEEP  : 회전하는 대형 베기
// 8. VOID VORTEX     : 플레이어 위치에 소용돌이 생성
// ========================================================

function bossAimAngle(boss) {

    return Math.atan2(
        player.y - boss.y,
        player.x - boss.x
    );

}


function addBossProjectile(data) {

    bossProjectiles.push(data);

}


// ========================================================
// 보스 공격 패턴
// ========================================================
// 1. VOID BOLT      : 조준 보이드 탄환
// 2. SHURIKEN BURST : 10방향 표창
// 3. BLADE RAIN     : 검/창 낙하
// 4. VOID NOVA      : 보스 주변 원형 폭발
// 5. CRESCENT SWEEP : 대형 회전 베기
// 6. VOID VORTEX    : 소용돌이
//
// 레이저와 플레이어 위치 지연 폭발은 사용하지 않습니다.
// ========================================================

function bossBasicShoot(boss) {

    if (!boss) {
        return;
    }

    // 플레이어 방향을 중심으로 좌우 45도, 총 90도 범위에서 랜덤 발사
    const angle =
        bossAimAngle(boss) +
        (Math.random() - 0.5) * (Math.PI / 2);

    addBossProjectile({
        kind: "bolt",
        x: boss.x,
        y: boss.y,
        vx: Math.cos(angle) * 180,
        vy: Math.sin(angle) * 180,
        radius: 10,
        damage: 18,
        life: 5,
        angle: angle
    });

    boss.attackFlash = 0.08;
}


function bossShoot(boss) {

    if (!boss) {
        return;
    }

    const hpRatio = boss.hp / boss.maxHp;
    let pattern;

    // 기본 탄환은 별도 연사 페이즈에서 사용합니다.
    // 여기서는 스킬 패턴만 1개 선택합니다.
    if (hpRatio < 0.30) {

        pattern = [
            "shuriken",
            "shuriken",
            "blade",
            "nova",
            "sweep",
            "vortex",
            "vortex"
        ][Math.floor(Math.random() * 7)];

    } else {

        pattern = [
            "shuriken",
            "blade",
            "nova",
            "sweep",
            "vortex",
            "shuriken",
            "blade"
        ][Math.floor(Math.random() * 7)];

    }

    boss.attackFlash = 0.25;


    // ----------------------------------------------------
    // 1. 기본 조준 탄환
    // ----------------------------------------------------
    if (pattern === "bolt") {

        const angle =
            bossAimAngle(boss) +
            (Math.random() - 0.5) * 0.28;

        addBossProjectile({

            kind: "bolt",
            x: boss.x,
            y: boss.y,

            vx: Math.cos(angle) * 180,
            vy: Math.sin(angle) * 180,

            radius: 10,
            damage: 18,
            life: 5,
            angle: angle

        });

    }


    // ----------------------------------------------------
    // 2. 10방향 표창
    // ----------------------------------------------------
    else if (pattern === "shuriken") {

        const base = bossAimAngle(boss);
        const count = 10;

        for (let i = 0; i < count; i++) {

            const angle =
                base +
                (Math.PI * 2 / count) * i;

            addBossProjectile({

                kind: "shuriken",
                x: boss.x,
                y: boss.y,

                vx: Math.cos(angle) * 150,
                vy: Math.sin(angle) * 150,

                radius: 15,
                damage: 14,
                life: 5,
                angle: angle

            });

        }

    }


    // ----------------------------------------------------
    // 3. 검/창 낙하
    // ----------------------------------------------------
    else if (pattern === "blade") {

        const count = 7;

        for (let i = 0; i < count; i++) {

            addBossProjectile({

                kind: "blade",

                x: 70 + Math.random() * (canvas.width - 140),
                y: -90 - Math.random() * 100,

                vx: 0,
                vy: 0,

                radius: 28,
                damage: 28,
                life: 2.2,

                delay: 0.25 + i * 0.10,
                active: false,

                targetY:
                    120 +
                    Math.random() * 400,

                angle:
                    Math.PI / 2 +
                    (Math.random() - 0.5) * 0.18

            });

        }

    }


    // ----------------------------------------------------
    // 4. 원형 보이드 폭발
    // ----------------------------------------------------
    else if (pattern === "nova") {

        addBossProjectile({

            kind: "nova",

            x: boss.x,
            y: boss.y,

            radius: 55,
            maxRadius: 390,
            expandSpeed: 300,

            damage: 24,
            life: 1.0,
            hit: false

        });

    }


    // ----------------------------------------------------
    // 5. 대형 회전 베기
    // ----------------------------------------------------
    else if (pattern === "sweep") {

        addBossProjectile({

            kind: "sweep",

            x: boss.x,
            y: boss.y,

            angle:
                bossAimAngle(boss) - 0.8,

            angularSpeed: 1.8,
            radius: 260,
            arc: 0.48,
            width: 85,

            damage: 30,
            life: 1.1,
            hit: false

        });

    }


    // ----------------------------------------------------
    // 6. 보이드 소용돌이
    // ----------------------------------------------------
    else if (pattern === "vortex") {

        const targetX = Math.max(
            110,
            Math.min(canvas.width - 110, player.x)
        );

        const targetY = Math.max(
            140,
            Math.min(canvas.height - 110, player.y)
        );

        addBossProjectile({

            kind: "vortex",

            x: targetX,
            y: targetY,

            radius: 25,
            maxRadius: 110,

            damage: 26,
            life: 2.0,
            delay: 0.45,
            active: false

        });

    }

}


// ========================================================
// 마력폭주
// ========================================================
// E키로 발동
// 플레이어가 조준한 방향을 중심으로 총 90도 범위에
// 30발의 탄환을 무작위로 퍼뜨립니다.
// ========================================================

function useMagicBurst() {

    if (!gameRunning) {
        return;
    }

    if (!magicBurstUnlocked) {
        return;
    }

    if (magicBurstCooldown > 0) {
        return;
    }

    const dx = mouseX - player.x;
    const dy = mouseY - player.y;

    const distance = Math.sqrt(
        dx * dx +
        dy * dy
    );

    if (distance <= 0) {
        return;
    }

    // 마우스 조준 방향을 기준으로 -45도 ~ +45도
    // = 총 90도의 범위
    const baseAngle = Math.atan2(dy, dx);

    const projectileCount = 30;
    const damage = player.attack * 1.5;
    const speed = 700;

    for (let i = 0; i < projectileCount; i++) {

        const randomOffset =
            (Math.random() - 0.5) *
            (Math.PI / 2);

        const angle =
            baseAngle +
            randomOffset;

        bullets.push({

            x: player.x,

            y: player.y,

            vx: Math.cos(angle) * speed,

            vy: Math.sin(angle) * speed,

            width: 20,

            height: 20,

            radius: 10,

            size: 20,

            damage: damage,

            critical: false,

            life: 2.5,

            magicBurst: true

        });

    }

    effects.push({
        x: player.x,
        y: player.y,
        size: 140,
        life: 0.35,
        maxLife: 0.35,
        type: "magicBurst"
    });

    magicBurstCooldown = magicBurstMaxCooldown;

}


// ========================================================
// 플레이어 발사
// ========================================================

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


    if (
        distance <= 0
    ) {

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


// ========================================================
// 충돌
// ========================================================

function collision(a, b) {


    return (

        Math.abs(
            a.x - b.x
        )
        <
        (
            a.width +
            b.width
        ) / 2

        &&

        Math.abs(
            a.y - b.y
        )
        <
        (
            a.height +
            b.height
        ) / 2

    );

}


// ========================================================
// 이펙트
// ========================================================

function createEffect(
    x,
    y,
    size
) {


    effects.push({

        x: x,

        y: y,

        size:
            size || 80,

        life: 0.3,

        maxLife: 0.3

    });

}


// ========================================================
// 플레이어 이동
// ========================================================

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
            dx *
            player.speed *
            dt;


        player.y +=
            dy *
            player.speed *
            dt;

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


// ========================================================
// 플레이어 총알 업데이트
// ========================================================

function updateBullets(dt) {


    for (
        let i =
            bullets.length - 1;

        i >= 0;

        i--
    ) {


        const bullet =
            bullets[i];


        bullet.x +=
            bullet.vx *
            dt;


        bullet.y +=
            bullet.vy *
            dt;


        let removeBullet =
            false;


        for (
            let j =
                enemies.length - 1;

            j >= 0;

            j--
        ) {


            const enemy =
                enemies[j];


            const bulletBox = {

                x: bullet.x,

                y: bullet.y,

                width:
                    bullet.size,

                height:
                    bullet.size

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


                removeBullet =
                    true;


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


                        bossSpawned =
                            false;


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

            removeBullet =
                true;

        }


        if (
            removeBullet
        ) {

            bullets.splice(
                i,
                1
            );

        }

    }

}


// ========================================================
// 적 업데이트
// ========================================================

function updateEnemies(dt) {


    for (
        let i =
            enemies.length - 1;

        i >= 0;

        i--
    ) {


        const enemy =
            enemies[i];


        // 보스는 플레이어를 추적하지 않고 화면 안에서 조금씩 랜덤 이동합니다.
        if (enemy.type === "boss") {

            const marginX = enemy.width / 2 + 20;
            const marginY = enemy.height / 2 + 20;

            enemy.moveTimer -= dt;

            if (enemy.moveTimer <= 0) {
                enemy.targetX = rand(marginX, canvas.width - marginX);
                enemy.targetY = rand(marginY, canvas.height * 0.45);
                enemy.moveTimer = rand(0.8, 1.8);
            }

            const moveDx = enemy.targetX - enemy.x;
            const moveDy = enemy.targetY - enemy.y;
            const moveDistance = Math.sqrt(
                moveDx * moveDx + moveDy * moveDy
            );

            if (moveDistance > 2) {
                const moveAmount = Math.min(
                    enemy.moveSpeed * dt,
                    moveDistance
                );

                enemy.x += moveDx / moveDistance * moveAmount;
                enemy.y += moveDy / moveDistance * moveAmount;
            }

            enemy.x = Math.max(
                marginX,
                Math.min(canvas.width - marginX, enemy.x)
            );
            enemy.y = Math.max(
                marginY,
                Math.min(canvas.height * 0.45, enemy.y)
            );

        } else {

            const dx = player.x - enemy.x;
            const dy = player.y - enemy.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance > 1) {
                enemy.x += dx / distance * enemy.speed * dt;
                enemy.y += dy / distance * enemy.speed * dt;
            }
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


// ========================================================
// 보스 공격 업데이트
// ========================================================

function damagePlayerFromBoss(damage, x, y) {

    if (player.invincible > 0) {
        return false;
    }

    player.hp -= damage;

    player.invincible = 0.5;

    createEffect(
        x,
        y,
        110
    );

    return true;

}


function angleDifference(a, b) {

    let d = a - b;

    while (d > Math.PI) {
        d -= Math.PI * 2;
    }

    while (d < -Math.PI) {
        d += Math.PI * 2;
    }

    return Math.abs(d);

}


function updateBossProjectiles(dt) {

    for (
        let i = bossProjectiles.length - 1;
        i >= 0;
        i--
    ) {

        const projectile = bossProjectiles[i];

        // 기본 탄환 / 표창
        if (
            projectile.kind === "bolt" ||
            projectile.kind === "shuriken"
        ) {

            projectile.x += projectile.vx * dt;
            projectile.y += projectile.vy * dt;
            projectile.life -= dt;

            const dx = projectile.x - player.x;
            const dy = projectile.y - player.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < projectile.radius + 28) {

                if (damagePlayerFromBoss(
                    projectile.damage,
                    player.x,
                    player.y
                )) {
                    bossProjectiles.splice(i, 1);
                    continue;
                }

            }

        }

        // 검/창 낙하
        else if (projectile.kind === "blade") {

            projectile.delay -= dt;

            if (projectile.delay <= 0) {
                projectile.active = true;
            }

            if (projectile.active) {

                projectile.y = Math.min(
                    projectile.targetY,
                    projectile.y + 500 * dt
                );

                projectile.life -= dt;

                const dx = Math.abs(player.x - projectile.x);
                const dy = Math.abs(player.y - projectile.y);

                if (dx < 30 && dy < 45) {

                    if (damagePlayerFromBoss(
                        projectile.damage,
                        player.x,
                        player.y
                    )) {
                        projectile.life = 0;
                    }

                }

            }

        }

        // 원형 폭발
        else if (projectile.kind === "nova") {

            projectile.radius += projectile.expandSpeed * dt;
            projectile.life -= dt;

            const dx = player.x - projectile.x;
            const dy = player.y - projectile.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (
                !projectile.hit &&
                Math.abs(distance - projectile.radius) < 30
            ) {

                projectile.hit = true;

                damagePlayerFromBoss(
                    projectile.damage,
                    player.x,
                    player.y
                );

            }

        }

        // 회전 베기
        else if (projectile.kind === "sweep") {

            projectile.angle += projectile.angularSpeed * dt;
            projectile.life -= dt;

            const dx = player.x - projectile.x;
            const dy = player.y - projectile.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            const playerAngle = Math.atan2(dy, dx);
            const diff = angleDifference(
                playerAngle,
                projectile.angle
            );

            if (
                !projectile.hit &&
                distance < projectile.radius + projectile.width / 2 &&
                distance > projectile.radius - projectile.width / 2 &&
                diff < projectile.arc
            ) {

                projectile.hit = true;

                damagePlayerFromBoss(
                    projectile.damage,
                    player.x,
                    player.y
                );

            }

        }

        // 소용돌이
        else if (projectile.kind === "vortex") {

            projectile.delay -= dt;

            if (projectile.delay <= 0) {
                projectile.active = true;
            }

            if (projectile.active) {

                projectile.radius = Math.min(
                    projectile.maxRadius,
                    projectile.radius + 90 * dt
                );

                projectile.life -= dt;

                const dx = projectile.x - player.x;
                const dy = projectile.y - player.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < projectile.radius) {

                    player.x += dx * 0.8 * dt;
                    player.y += dy * 0.8 * dt;

                }

                if (distance < 55) {

                    damagePlayerFromBoss(
                        projectile.damage,
                        player.x,
                        player.y
                    );

                }

            }

        }

        // 제거
        if (
            projectile.life <= 0 ||
            projectile.x < -300 ||
            projectile.x > canvas.width + 300 ||
            projectile.y < -300 ||
            projectile.y > canvas.height + 300
        ) {

            bossProjectiles.splice(i, 1);

        }

    }

}


// ========================================================
// 이펙트 업데이트
// ========================================================

function updateEffects(dt) {


    for (
        let i =
            effects.length - 1;

        i >= 0;

        i--
    ) {


        effects[i].life -=
            dt;


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


// ========================================================
// 플레이어 공격
// ========================================================

function updateAttack(dt) {


    attackTimer -=
        dt;

    if (magicBurstCooldown > 0) {

        magicBurstCooldown -= dt;

        magicBurstCooldown = Math.max(
            0,
            magicBurstCooldown
        );

    }


    if (
        attackTimer <= 0
    ) {


        shoot();


        attackTimer =
            player.attackSpeed;

    }

}


// ========================================================
// 스테이지 진행
// ========================================================

function updateStage(dt) {


    stageTimer +=
        dt;


    // ====================================================
    // 1~5
    // ====================================================

    if (
        stage < 6
    ) {


        spawnTimer -=
            dt;


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


    // ====================================================
    // 6 보스
    // ====================================================

    if (
        stage === 6
    ) {


        const boss =
            enemies.find(
                e =>
                    e.type === "boss"
            );


        if (

            !bossSpawned &&

            !boss &&

            stageTimer >= 1

        ) {


            spawnBoss();

        }


        if (boss) {


            // --------------------------------------------
            // 보스 기본 공격
            // 기본 공격은 스킬 사용 여부와 관계없이 계속 발사
            // --------------------------------------------

            bossBasicShotTimer -= dt;

            if (bossBasicShotTimer <= 0) {
                bossBasicShoot(boss);
                bossBasicShotTimer += bossBasicShotInterval;
            }

            // --------------------------------------------
            // 보스 스킬
            // 2초마다 1회 사용
            // 기본 공격과 동시에 사용 가능
            // --------------------------------------------

            bossSkillTimer -= dt;

            if (bossSkillTimer <= 0) {
                bossShoot(boss);
                bossSkillTimer += bossSkillInterval;
            }

        }

    }

}


// ========================================================
// 스테이지 클리어
// ========================================================

function finishStage() {


    if (
        !gameRunning
    ) {

        return;

    }


    gameRunning =
        false;


    enemies = [];

    bullets = [];

    bossProjectiles = [];

    // 5스테이지가 끝나면 일반 BGM을 멈춥니다.
    if (stage === 5) {
        const audio = document.getElementById("gameBGM");
        if (audio) {
            audio.pause();
            audio.currentTime = 0;
        }
    }

    // 스테이지 3 클리어 시 마력폭주 해금
    if (stage === 3) {

        magicBurstUnlocked = true;
        magicBurstCooldown = 0;

    }


    showUpgradeMenu();

}


// ========================================================
// 강화 메뉴
// ========================================================

function showUpgradeMenu() {


    const menu =
        document.getElementById(
            "menu"
        );


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


        ${stage === 3 ? `
            <div style="margin: 12px 0; padding: 10px; border: 2px solid rgba(255,255,255,0.5); border-radius: 8px;">
                🔮 <b>마력폭주 해금!</b><br>
                E키를 누르면 조준 방향 기준 90도 범위로 30발을 발사합니다.<br>
                공격력의 1.5배 피해 · 재사용 대기시간 2초
            </div>
        ` : ""}


        <button
            class="upgrade"
            onclick="upgradeAttack()">

            ⚔️ 공격력 강화

            <span>
                100 PT
            </span>

        </button>


        <button
            class="upgrade"
            onclick="upgradeSpeed()">

            🔫 공격 속도 강화

            <span>
                150 PT
            </span>

        </button>


        <button
            class="upgrade"
            onclick="upgradeCrit()">

            💥 치명타 확률 강화

            <span>
                200 PT
            </span>

        </button>


        <br>


        <button
            onclick="nextStage()">

            다음 스테이지 →

        </button>

    `;

}


// ========================================================
// 공격력 강화
// ========================================================

function upgradeAttack() {


    if (
        totalPT >= 100
    ) {


        totalPT -=
            100;


        player.attack +=
            10;


        showUpgradeMenu();

    }

}


// ========================================================
// 공격속도 강화
// ========================================================

function upgradeSpeed() {


    if (
        totalPT >= 150
    ) {


        totalPT -=
            150;


        player.attackSpeed =
            Math.max(
                0.08,
                player.attackSpeed - 0.04
            );


        showUpgradeMenu();

    }

}


// ========================================================
// 치명타 강화
// ========================================================

function upgradeCrit() {


    if (
        totalPT >= 200
    ) {


        totalPT -=
            200;


        player.critChance =
            Math.min(
                0.75,
                player.critChance + 0.05
            );


        showUpgradeMenu();

    }

}


// ========================================================
// 다음 스테이지
// ========================================================

function nextStage() {


    if (
        stage >= 6
    ) {

        return;

    }


    stage++;

    // 6스테이지 시작 시 업로드한 보스 전용 BGM을 재생합니다.
    if (stage === 6) {
        const audio = document.getElementById("gameBGM");
        const bossAudio = document.getElementById("bossBGM");

        if (audio) {
            audio.pause();
            audio.currentTime = 0;
        }

        if (bossAudio) {
            bossAudio.currentTime = 0;
            bossAudio.volume = 0.55;
            bossAudio.play().catch(() => {});
        }
    }


    stagePT = 0;

    stageTimer = 0;

    spawnTimer = 0;

    attackTimer = 0;


    bossAttackTimer = 1.5;

    bossAttackSpeed = 250;

    bossAttackSpeedTimer = 2;

    bossBasicShotTimer = 0;

    bossSkillTimer = bossSkillInterval;

    bossPatternIndex = 0;


    enemies = [];

    bullets = [];

    bossProjectiles = [];

    effects = [];


    bossSpawned =
        false;


    player.hp =
        player.maxHp;


    player.x =
        canvas.width / 2;


    player.y =
        canvas.height - 100;


    document
        .getElementById(
            "menu"
        )
        .classList.add(
            "hidden"
        );


    document
        .getElementById(
            "bossBarOuter"
        )
        .style.display =
        "none";


    document
        .getElementById(
            "bossText"
        )
        .style.display =
        "none";


    gameRunning =
        true;


    lastTime =
        performance.now();


    requestAnimationFrame(
        gameLoop
    );

}


// ========================================================
// 게임 클리어
// ========================================================

function finalGame() {


    gameRunning =
        false;


    enemies = [];

    bullets = [];

    bossProjectiles = [];

    const audio = document.getElementById("gameBGM");
    const bossAudio = document.getElementById("bossBGM");
    if (audio) audio.pause();
    if (bossAudio) bossAudio.pause();


    document
        .getElementById(
            "bossBarOuter"
        )
        .style.display =
        "none";


    document
        .getElementById(
            "bossText"
        )
        .style.display =
        "none";


    document
        .getElementById(
            "menu"
        )
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
            style="
                font-size:55px;
            ">

            ${totalEarnedPT} PT

        </h1>


        <p>
            게임에서 획득한
            전체 PT입니다.
        </p>


        <button
            onclick="location.reload()">

            다시 시작

        </button>

    `;

}


// ========================================================
// 게임 오버
// ========================================================

function gameOver() {


    gameRunning =
        false;


    document
        .getElementById(
            "menu"
        )
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
            Stage ${stage}에서
            쓰러졌습니다.
        </p>


        <h2>
            획득 PT:
            ${totalEarnedPT}
        </h2>


        <button
            onclick="location.reload()">

            다시 시작

        </button>

    `;

}


// ========================================================
// 배경
// ========================================================

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


// ========================================================
// 플레이어
// ========================================================

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


// ========================================================
// 적
// ========================================================

function drawEnemy(enemy) {


    let image;


    if (
        enemy.type === "normal"
    ) {

        image =
            normalImg;

    }

    else if (
        enemy.type === "tank"
    ) {

        image =
            tankImg;

    }

    else {

        image =
            bossImg;

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


    // ----------------------------------------------------
    // 일반 적 HP
    // ----------------------------------------------------

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

            barWidth *
                hpRatio,

            6

        );

    }

}


// ========================================================
// 보스 공격 그래픽
// ========================================================

function drawImageCentered(
    image,
    x,
    y,
    w,
    h,
    rotation
) {

    if (
        !image ||
        !image.complete ||
        image.naturalWidth <= 0
    ) {
        return false;
    }

    ctx.save();

    ctx.translate(x, y);

    if (rotation !== undefined) {
        ctx.rotate(rotation);
    }

    ctx.drawImage(
        image,
        -w / 2,
        -h / 2,
        w,
        h
    );

    ctx.restore();

    return true;

}


function drawBossProjectiles() {

    for (const projectile of bossProjectiles) {

        // 기본 조준 탄환은 기존 boss_attack.png 사용
        if (projectile.kind === "bolt") {

            const drawn = drawImageCentered(
                bossAttackImg,
                projectile.x,
                projectile.y,
                50,
                50,
                projectile.angle
            );

            if (!drawn) {

                ctx.fillStyle = "#ff28e8";
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

        // 표창
        else if (projectile.kind === "shuriken") {

            const drawn = drawImageCentered(
                bossShurikenImg,
                projectile.x,
                projectile.y,
                62,
                62,
                projectile.angle + performance.now() / 500
            );

            if (!drawn) {

                ctx.strokeStyle = "#d83cff";
                ctx.lineWidth = 7;
                ctx.beginPath();
                ctx.moveTo(projectile.x - 18, projectile.y);
                ctx.lineTo(projectile.x + 18, projectile.y);
                ctx.moveTo(projectile.x, projectile.y - 18);
                ctx.lineTo(projectile.x, projectile.y + 18);
                ctx.stroke();

            }

        }

        // 검/창
        else if (projectile.kind === "blade") {

            ctx.globalAlpha = projectile.active ? 1 : 0.35;

            const drawn = drawImageCentered(
                bossBladeImg,
                projectile.x,
                projectile.y,
                55,
                115,
                projectile.angle
            );

            if (!drawn) {

                ctx.fillStyle = "#a83cff";
                ctx.fillRect(
                    projectile.x - 8,
                    projectile.y - 45,
                    16,
                    90
                );

            }

            ctx.globalAlpha = 1;

        }

        // 원형 보이드 폭발
        else if (projectile.kind === "nova") {

            const size = Math.max(
                100,
                projectile.radius * 2
            );

            const drawn = drawImageCentered(
                bossNovaImg,
                projectile.x,
                projectile.y,
                size,
                size,
                0
            );

            if (!drawn) {

                ctx.strokeStyle = "#d83cff";
                ctx.lineWidth = 18;
                ctx.beginPath();
                ctx.arc(
                    projectile.x,
                    projectile.y,
                    projectile.radius,
                    0,
                    Math.PI * 2
                );
                ctx.stroke();

            }

        }

        // 대형 회전 베기
        else if (projectile.kind === "sweep") {

            const drawn = drawImageCentered(
                bossSweepImg,
                projectile.x,
                projectile.y,
                360,
                210,
                projectile.angle
            );

            if (!drawn) {

                ctx.strokeStyle = "#e84cff";
                ctx.lineWidth = 30;
                ctx.beginPath();
                ctx.arc(
                    projectile.x,
                    projectile.y,
                    projectile.radius,
                    projectile.angle - projectile.arc,
                    projectile.angle + projectile.arc
                );
                ctx.stroke();

            }

        }

        // 보이드 소용돌이
        else if (projectile.kind === "vortex") {

            const size = Math.max(
                100,
                projectile.radius * 2.4
            );

            const drawn = drawImageCentered(
                bossVortexImg,
                projectile.x,
                projectile.y,
                size,
                size,
                performance.now() / 700
            );

            if (!drawn) {

                ctx.strokeStyle = "#9d35ff";
                ctx.lineWidth = 14;
                ctx.beginPath();
                ctx.arc(
                    projectile.x,
                    projectile.y,
                    projectile.radius,
                    0,
                    Math.PI * 1.6
                );
                ctx.stroke();

            }

        }

    }

}


// ========================================================
// 플레이어 총알
// ========================================================

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


// ========================================================
// 이펙트
// ========================================================

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


        ctx.globalAlpha =
            1;

    }

}


// ========================================================
// UI
// ========================================================

function updateUI() {


    document.getElementById(
        "hpText"
    ).textContent =

        Math.max(
            0,
            Math.floor(
                player.hp
            )
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

        stage +
        " / 6";


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
            e =>
                e.type === "boss"
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


    const skillUI =
        document.getElementById("skillUI");

    const skillCooldownText =
        document.getElementById("skillCooldownText");

    if (skillUI && skillCooldownText) {

        if (!magicBurstUnlocked) {

            skillUI.className = "skill-locked";
            skillCooldownText.textContent = "STAGE 3 CLEAR";

        } else if (magicBurstCooldown > 0) {

            skillUI.className = "skill-cooldown";
            skillCooldownText.textContent =
                magicBurstCooldown.toFixed(1) + "s";

        } else {

            skillUI.className = "skill-ready";
            skillCooldownText.textContent = "READY";

        }

    }

}


// ========================================================
// 게임 루프
// ========================================================

function gameLoop(time) {


    if (
        !gameRunning
    ) {

        return;

    }


    let dt =
        (
            time -
            lastTime
        ) / 1000;


    dt =
        Math.min(
            dt,
            0.05
        );


    lastTime =
        time;


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


    for (const enemy of enemies) {

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


// ========================================================
// 초기 UI
// ========================================================

updateUI();

</script>

</body>

</html>

"""


                                                           
        
                                                           

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
    "__BOSS_SHURIKEN__",
    images["bossShuriken"]
)

html = html.replace(
    "__BOSS_BLADE__",
    images["bossBlade"]
)

html = html.replace(
    "__BOSS_NOVA__",
    images["bossNova"]
)

html = html.replace(
    "__BOSS_SWEEP__",
    images["bossSweep"]
)

html = html.replace(
    "__BOSS_VORTEX__",
    images["bossVortex"]
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


                                                           
        
                                                           

html = html.replace(
    "__BGM__",
    bgm
)

                 
boss_bgm_data = load_audio("boss_music.mp3")
html = html.replace(
    "__BOSS_BGM__",
    boss_bgm_data
)


                                                           
              
                                                           

components.html(
    html,
    height=700,
    scrolling=False
)
