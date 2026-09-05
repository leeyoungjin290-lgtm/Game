// =========================================================
// 보스 공격 속도
// =========================================================

// 보스 공격 속도 수치
// 250 → 325 → 400 → ... → 1200
let bossAttackSpeed = 250;

// 2초마다 공격속도 증가
let bossAttackSpeedTimer = 2;

// 실제 공격까지 남은 시간
let bossAttackTimer = 1.5;


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

        hp: 50000,
        maxHp: 50000,

        speed: 35,
        damage: 35,
        pt: 1000,
        attackFlash: 0
    });

    bossSpawned = true;

    // 보스 공격 관련 값 초기화
    bossAttackTimer = 1.5;
    bossAttackSpeed = 250;
    bossAttackSpeedTimer = 2;

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

    if (!boss) {
        return;
    }

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

            // 중요:
            // 탄환 속도는 공격속도와 별개
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
// 스테이지 진행
// =========================================================

function updateStage(dt) {

    stageTimer += dt;


    // =====================================================
    // 1~5 스테이지
    // =====================================================

    if (stage < 6) {

        spawnTimer -= dt;

        const setting =
            stages[stage];


        if (spawnTimer <= 0) {

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

    if (stage === 6) {

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

            // =============================================
            // 2초마다 보스 공격속도 증가
            // =============================================

            bossAttackSpeedTimer -= dt;


            if (
                bossAttackSpeedTimer <= 0
            ) {

                bossAttackSpeedTimer += 2;

                bossAttackSpeed =
                    Math.min(
                        1200,
                        bossAttackSpeed + 75
                    );
            }


            // =============================================
            // 공격속도를 실제 공격 간격으로 변환
            // =============================================

            // 공격속도 250일 때
            // 0.24초마다 공격
            //
            // 공격속도 1200일 때
            // 0.05초마다 공격

            const attackInterval =
                60 / bossAttackSpeed;


            bossAttackTimer -= dt;


            if (
                bossAttackTimer <= 0
            ) {

                bossShoot(boss);

                bossAttackTimer =
                    attackInterval;
            }
        }
    }
}
