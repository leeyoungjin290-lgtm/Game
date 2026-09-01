```python
import pygame
import random
import math
import sys

# =========================================================
# 초기 설정
# =========================================================

pygame.init()

WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("6 Stage Battle")

clock = pygame.time.Clock()

FPS = 60


# =========================================================
# 이미지 로드
# =========================================================

def load_image(filename):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return image
    except:
        print(f"[경고] {filename} 을(를) 찾을 수 없습니다.")
        return None


player_img = load_image("player.png")
enemy_normal_img = load_image("enemy_normal.png")
enemy_tank_img = load_image("enemy_tank.png")
boss_img = load_image("boss.png")
background_img = load_image("background.png")
bullet_img = load_image("bullet.png")
hit_effect_img = load_image("hit_effect.png")


# =========================================================
# 폰트
# =========================================================

font_small = pygame.font.SysFont("malgungothic", 20)
font = pygame.font.SysFont("malgungothic", 26)
font_big = pygame.font.SysFont("malgungothic", 45)
font_huge = pygame.font.SysFont("malgungothic", 65)


# =========================================================
# 색상
# =========================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 60, 60)
GREEN = (60, 220, 100)
BLUE = (70, 150, 255)
YELLOW = (255, 220, 50)
PURPLE = (180, 70, 255)
GRAY = (80, 80, 80)


# =========================================================
# 이미지 크기 조정
# =========================================================

def resize_image(image, size):

    if image is None:
        return None

    return pygame.transform.smoothscale(image, size)


player_img = resize_image(player_img, (60, 60))
enemy_normal_img = resize_image(enemy_normal_img, (50, 50))
enemy_tank_img = resize_image(enemy_tank_img, (70, 70))
boss_img = resize_image(boss_img, (140, 140))
bullet_img = resize_image(bullet_img, (22, 22))
hit_effect_img = resize_image(hit_effect_img, (60, 60))
background_img = resize_image(background_img, (WIDTH, HEIGHT))


# =========================================================
# 플레이어
# =========================================================

player = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,

    "width": 60,
    "height": 60,

    "hp": 100,
    "max_hp": 100,

    "atk": 10,

    "attack_speed": 1.0,

    "crit": 5,

    "crit_damage": 150,

    "move_speed": 4,

    "cooldown": 0
}


# =========================================================
# 게임 변수
# =========================================================

stage = 1

pt = 0

kills = 0

game_running = True

upgrade_screen = False

result_screen = False

stage_clear_processed = False


enemies = []

bullets = []

effects = []


# =========================================================
# 적 생성
# =========================================================

def spawn_stage():

    global enemies
    global bullets
    global effects
    global stage_clear_processed

    enemies = []
    bullets = []
    effects = []

    stage_clear_processed = False

    # -----------------------------------------------------
    # 6스테이지 보스
    # -----------------------------------------------------

    if stage == 6:

        enemies.append({
            "type": "boss",

            "x": WIDTH // 2,
            "y": 130,

            "width": 140,
            "height": 140,

            "hp": 1500,
            "max_hp": 1500,

            "speed": 0.8,

            "damage": 20,

            "attack_cooldown": 0
        })

        return


    # -----------------------------------------------------
    # 일반 스테이지
    # -----------------------------------------------------

    enemy_count = 5 + stage * 3

    for _ in range(enemy_count):

        is_tank = random.random() < 0.25

        if is_tank:

            width = 70
            height = 70

            hp = 70 + stage * 15

            speed = 0.6 + stage * 0.05

            damage = 12 + stage * 2

            enemy_type = "tank"

        else:

            width = 50
            height = 50

            hp = 30 + stage * 10

            speed = 1.0 + stage * 0.1

            damage = 5 + stage

            enemy_type = "normal"


        enemies.append({
            "type": enemy_type,

            "x": random.randint(70, WIDTH - 70),
            "y": random.randint(100, HEIGHT - 70),

            "width": width,
            "height": height,

            "hp": hp,
            "max_hp": hp,

            "speed": speed,

            "damage": damage,

            "attack_cooldown": 0
        })


# =========================================================
# 이미지 중앙 배치
# =========================================================

def draw_center(image, x, y):

    if image is None:
        return

    rect = image.get_rect(center=(int(x), int(y)))

    screen.blit(image, rect)


# =========================================================
# 플레이어 이동
# =========================================================

def update_player():

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w]:
        dy -= 1

    if keys[pygame.K_s]:
        dy += 1

    if keys[pygame.K_a]:
        dx -= 1

    if keys[pygame.K_d]:
        dx += 1


    if dx != 0 or dy != 0:

        length = math.sqrt(dx * dx + dy * dy)

        dx /= length
        dy /= length

        player["x"] += dx * player["move_speed"]
        player["y"] += dy * player["move_speed"]


    # 화면 밖으로 못 나가게

    half_w = player["width"] // 2
    half_h = player["height"] // 2

    player["x"] = max(
        half_w,
        min(WIDTH - half_w, player["x"])
    )

    player["y"] = max(
        half_h,
        min(HEIGHT - half_h, player["y"])
    )


# =========================================================
# 공격
# =========================================================

def shoot():

    if player["cooldown"] > 0:
        return


    mouse_x, mouse_y = pygame.mouse.get_pos()


    dx = mouse_x - player["x"]
    dy = mouse_y - player["y"]


    distance = math.sqrt(dx * dx + dy * dy)


    if distance == 0:
        return


    dx /= distance
    dy /= distance


    # 치명타 판정

    critical = random.random() * 100 < player["crit"]


    damage = player["atk"]


    if critical:

        damage *= player["crit_damage"] / 100


    bullets.append({

        "x": player["x"],
        "y": player["y"],

        "vx": dx * 10,
        "vy": dy * 10,

        "damage": damage,

        "critical": critical
    })


    # 공격속도
    # 값이 높을수록 공격 간격이 짧아짐

    player["cooldown"] = 30 / player["attack_speed"]


# =========================================================
# 총알 업데이트
# =========================================================

def update_bullets():

    for bullet in bullets[:]:

        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]


        # 화면 밖

        if (
            bullet["x"] < -30 or
            bullet["x"] > WIDTH + 30 or
            bullet["y"] < -30 or
            bullet["y"] > HEIGHT + 30
        ):

            bullets.remove(bullet)

            continue


        # 적과 충돌

        for enemy in enemies[:]:

            dx = bullet["x"] - enemy["x"]
            dy = bullet["y"] - enemy["y"]

            distance = math.sqrt(dx * dx + dy * dy)


            if distance < enemy["width"] / 2 + 10:

                enemy["hp"] -= bullet["damage"]


                # 공격 효과

                effects.append({
                    "x": enemy["x"],
                    "y": enemy["y"],
                    "timer": 12
                })


                if bullet in bullets:
                    bullets.remove(bullet)


                # 적 사망

                if enemy["hp"] <= 0:

                    kill_enemy(enemy)


                break


# =========================================================
# 적 처치
# =========================================================

def kill_enemy(enemy):

    global pt
    global kills


    if enemy["type"] == "boss":

        reward = 500

    elif enemy["type"] == "tank":

        reward = 25 + stage * 3

    else:

        reward = 10 + stage * 2


    pt += reward

    kills += 1


    if enemy in enemies:
        enemies.remove(enemy)


# =========================================================
# 적 AI
# =========================================================

def update_enemies():

    global game_running


    for enemy in enemies:

        dx = player["x"] - enemy["x"]
        dy = player["y"] - enemy["y"]


        distance = math.sqrt(dx * dx + dy * dy)


        if distance == 0:
            continue


        collision_distance = (
            player["width"] / 2 +
            enemy["width"] / 2
        )


        # 플레이어에게 이동

        if distance > collision_distance:

            enemy["x"] += (
                dx / distance *
                enemy["speed"]
            )

            enemy["y"] += (
                dy / distance *
                enemy["speed"]
            )


        # 공격

        else:

            if enemy["attack_cooldown"] <= 0:

                player["hp"] -= enemy["damage"]

                enemy["attack_cooldown"] = 60


        if enemy["attack_cooldown"] > 0:

            enemy["attack_cooldown"] -= 1


    # 플레이어 사망

    if player["hp"] <= 0:

        player["hp"] = 0

        game_over()


# =========================================================
# 업그레이드
# =========================================================

def upgrade_attack():

    global pt

    cost = 50

    if pt >= cost:

        pt -= cost

        player["atk"] += 5


def upgrade_speed():

    global pt

    cost = 70

    if pt >= cost:

        pt -= cost

        player["attack_speed"] += 0.1


def upgrade_crit():

    global pt

    cost = 80

    if pt >= cost:

        pt -= cost

        player["crit"] += 5


def upgrade_crit_damage():

    global pt

    cost = 100

    if pt >= cost:

        pt -= cost

        player["crit_damage"] += 25


# =========================================================
# 다음 스테이지
# =========================================================

def next_stage():

    global stage
    global upgrade_screen
    global game_running


    stage += 1


    player["hp"] = player["max_hp"]


    upgrade_screen = False

    game_running = True


    spawn_stage()


# =========================================================
# 게임 오버
# =========================================================

def game_over():

    global game_running
    global result_screen


    game_running = False

    result_screen = True


# =========================================================
# 게임 클리어
# =========================================================

def victory():

    global game_running
    global result_screen


    game_running = False

    result_screen = True


# =========================================================
# 스테이지 클리어 확인
# =========================================================

def check_stage_clear():

    global upgrade_screen
    global game_running
    global stage_clear_processed


    if len(enemies) != 0:
        return


    if stage_clear_processed:
        return


    stage_clear_processed = True


    # 6스테이지 클리어

    if stage == 6:

        victory()

        return


    # 업그레이드 화면

    game_running = False

    upgrade_screen = True


# =========================================================
# 버튼
# =========================================================

def draw_button(rect, text):

    pygame.draw.rect(
        screen,
        (55, 55, 65),
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (130, 130, 140),
        rect,
        2,
        border_radius=8
    )


    text_surface = font_small.render(
        text,
        True,
        WHITE
    )


    text_rect = text_surface.get_rect(
        center=rect.center
    )


    screen.blit(
        text_surface,
        text_rect
    )


# =========================================================
# 게임 화면
# =========================================================

def draw_game():

    # 배경

    if background_img is not None:

        screen.blit(
            background_img,
            (0, 0)
        )

    else:

        screen.fill((15, 15, 25))


    # 총알

    for bullet in bullets:

        if bullet_img is not None:

            draw_center(
                bullet_img,
                bullet["x"],
                bullet["y"]
            )

        else:

            pygame.draw.circle(
                screen,
                YELLOW if bullet["critical"] else WHITE,
                (
                    int(bullet["x"]),
                    int(bullet["y"])
                ),
                5
            )


    # 적

    for enemy in enemies:

        if enemy["type"] == "boss":

            image = boss_img

        elif enemy["type"] == "tank":

            image = enemy_tank_img

        else:

            image = enemy_normal_img


        if image is not None:

            draw_center(
                image,
                enemy["x"],
                enemy["y"]
            )

        else:

            color = (
                PURPLE
                if enemy["type"] == "boss"
                else RED
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    int(enemy["x"]),
                    int(enemy["y"])
                ),
                enemy["width"] // 2
            )


        # HP 바

        bar_width = enemy["width"]

        bar_x = enemy["x"] - bar_width / 2

        bar_y = (
            enemy["y"]
            - enemy["height"] / 2
            - 10
        )


        pygame.draw.rect(
            screen,
            (40, 40, 40),
            (
                bar_x,
                bar_y,
                bar_width,
                6
            )
        )


        hp_ratio = max(
            0,
            enemy["hp"] / enemy["max_hp"]
        )


        pygame.draw.rect(
            screen,
            GREEN,
            (
                bar_x,
                bar_y,
                bar_width * hp_ratio,
                6
            )
        )


    # 공격 효과

    for effect in effects:

        if hit_effect_img is not None:

            alpha = int(
                255 *
                effect["timer"] / 12
            )

            temp = hit_effect_img.copy()

            temp.set_alpha(alpha)

            rect = temp.get_rect(
                center=(
                    int(effect["x"]),
                    int(effect["y"])
                )
            )

            screen.blit(temp, rect)


    # 플레이어

    if player_img is not None:

        draw_center(
            player_img,
            player["x"],
            player["y"]
        )

    else:

        pygame.draw.circle(
            screen,
            BLUE,
            (
                int(player["x"]),
                int(player["y"])
            ),
            25
        )


    # UI

    draw_ui()


# =========================================================
# UI
# =========================================================

def draw_ui():

    texts = [

        f"HP: {int(player['hp'])} / {player['max_hp']}",

        f"ATK: {player['atk']}",

        f"공격속도: {player['attack_speed']:.1f}",

        f"치명타 확률: {player['crit']}%",

        f"치명타 피해: {player['crit_damage']}%",

        f"PT: {pt}",

        f"남은 적: {len(enemies)}"
    ]


    y = 10


    for text in texts:

        surface = font_small.render(
            text,
            True,
            WHITE
        )

        screen.blit(
            surface,
            (10, y)
        )

        y += 25


    # 스테이지

    stage_surface = font.render(
        f"STAGE {stage} / 6",
        True,
        WHITE
    )


    stage_rect = stage_surface.get_rect(
        center=(WIDTH // 2, 30)
    )


    screen.blit(
        stage_surface,
        stage_rect
    )


# =========================================================
# 업그레이드 화면
# =========================================================

def draw_upgrade():

    screen.fill((12, 12, 20))


    title = font_huge.render(
        "STAGE CLEAR!",
        True,
        WHITE
    )


    title_rect = title.get_rect(
        center=(WIDTH // 2, 100)
    )


    screen.blit(title, title_rect)


    pt_text = font.render(
        f"현재 PT: {pt}",
        True,
        YELLOW
    )


    pt_rect = pt_text.get_rect(
        center=(WIDTH // 2, 160)
    )


    screen.blit(pt_text, pt_rect)


    buttons = [

        (
            pygame.Rect(
                WIDTH // 2 - 160,
                220,
                320,
                55
            ),
            "공격력 +5     50 PT"
        ),

        (
            pygame.Rect(
                WIDTH // 2 - 160,
                290,
                320,
                55
            ),
            "공격속도 +10%     70 PT"
        ),

        (
            pygame.Rect(
                WIDTH // 2 - 160,
                360,
                320,
                55
            ),
            "치명타 확률 +5%     80 PT"
        ),

        (
            pygame.Rect(
                WIDTH // 2 - 160,
                430,
                320,
                55
            ),
            "치명타 피해 +25%     100 PT"
        ),

        (
            pygame.Rect(
                WIDTH // 2 - 160,
                510,
                320,
                55
            ),
            "다음 스테이지"
        )
    ]


    for rect, text in buttons:

        draw_button(
            rect,
            text
        )


# =========================================================
# 결과 화면
# =========================================================

def draw_result():

    screen.fill((8, 8, 15))


    if stage == 6 and len(enemies) == 0:

        title_text = "ALL STAGES CLEAR!"

        title_color = YELLOW

    else:

        title_text = "GAME OVER"

        title_color = RED


    title = font_huge.render(
        title_text,
        True,
        title_color
    )


    title_rect = title.get_rect(
        center=(WIDTH // 2, 120)
    )


    screen.blit(
        title,
        title_rect
    )


    results = [

        f"최종 점수: {pt} PT",

        f"총 처치 수: {kills}",

        f"도달 스테이지: {stage}",

        "",

        f"공격력: {player['atk']}",

        f"공격속도: {player['attack_speed']:.1f}",

        f"치명타 확률: {player['crit']}%",

        f"치명타 피해: {player['crit_damage']}%"
    ]


    y = 210


    for text in results:

        surface = font.render(
            text,
            True,
            WHITE
        )


        rect = surface.get_rect(
            center=(WIDTH // 2, y)
        )


        screen.blit(
            surface,
            rect
        )


        y += 42


    restart_button = pygame.Rect(
        WIDTH // 2 - 120,
        550,
        240,
        55
    )


    draw_button(
        restart_button,
        "다시 시작"
    )


# =========================================================
# 효과 업데이트
# =========================================================

def update_effects():

    for effect in effects[:]:

        effect["timer"] -= 1


        if effect["timer"] <= 0:

            effects.remove(effect)


# =========================================================
# 마우스 클릭 처리
# =========================================================

def handle_mouse_click(pos):

    global upgrade_screen


    # 업그레이드 화면

    if upgrade_screen:

        buttons = [

            (
                pygame.Rect(
                    WIDTH // 2 - 160,
                    220,
                    320,
                    55
                ),
                upgrade_attack
            ),

            (
                pygame.Rect(
                    WIDTH // 2 - 160,
                    290,
                    320,
                    55
                ),
                upgrade_speed
            ),

            (
                pygame.Rect(
                    WIDTH // 2 - 160,
                    360,
                    320,
                    55
                ),
                upgrade_crit
            ),

            (
                pygame.Rect(
                    WIDTH // 2 - 160,
                    430,
                    320,
                    55
                ),
                upgrade_crit_damage
            ),

            (
                pygame.Rect(
                    WIDTH // 2 - 160,
                    510,
                    320,
                    55
                ),
                next_stage
            )
        ]


        for rect, function in buttons:

            if rect.collidepoint(pos):

                function()

                return


    # 결과 화면

    if result_screen:

        restart_button = pygame.Rect(
            WIDTH // 2 - 120,
            550,
            240,
            55
        )


        if restart_button.collidepoint(pos):

            pygame.quit()

            # 같은 프로그램 다시 실행

            import os

            os.execl(
                sys.executable,
                sys.executable,
                *sys.argv
            )


# =========================================================
# 메인 루프
# =========================================================

spawn_stage()


running = True


while running:

    clock.tick(FPS)


    # -----------------------------------------------------
    # 이벤트
    # -----------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                handle_mouse_click(
                    event.pos
                )


        # ESC = 종료

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False


    # -----------------------------------------------------
    # 게임 플레이
    # -----------------------------------------------------

    if game_running:

        update_player()


        # 마우스 누르고 있으면 자동 공격

        if pygame.mouse.get_pressed()[0]:

            shoot()


        if player["cooldown"] > 0:

            player["cooldown"] -= 1


        update_bullets()

        update_enemies()

        update_effects()

        check_stage_clear()


    # -----------------------------------------------------
    # 화면
    # -----------------------------------------------------

    if result_screen:

        draw_result()

    elif upgrade_screen:

        draw_upgrade()

    else:

        draw_game()


    pygame.display.flip()


pygame.quit()

sys.exit()
```
