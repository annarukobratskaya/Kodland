import pygame
import random
import sys

# Инициализация PyGame
pygame.init()

# Размеры экрана
screen_width = 800
screen_height = 600

# Цвета
white = (255, 255, 255)  # Белый фон
red = (255, 0, 0)        # Красный (цвет астероидов)
dark_green = (0, 128, 0) # Темно-зеленый (цвет динозавра)
black = (0, 0, 0)       # Черный (цвет текста)

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Динозавр и астероиды")

# Параметры динозавра
dino_x = 50
dino_y = 300
dino_width = 40
dino_height = 60
dino_speed = 5

# Параметры астероидов
asteroid_x = 800
asteroid_width = 40
asteroid_height = 40
asteroid_speed = 5
asteroid_y = random.randint(50, 550)  # Генерация случайной позиции Y

# Очки
score = 0

# Инструкция
instruction_font = pygame.font.Font(None, 36)
instruction_text = instruction_font.render("Помоги квадратному динозавру уворачиваться от квадратных астероидов.", True, black)
instruction_text2 = instruction_font.render("Управление квадратным динозавром: стрелочки вверх и вниз.", True, black)
instruction_text3 = instruction_font.render("Для начала игры нажми Enter", True, black)

# Функция для разбиения текста по словам и переноса на новую строку
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = current_line + [word] if current_line else [word]
        test_size = font.size(' '.join(test_line))

        if test_size[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Флаг состояния игры
game_started = False

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            # Если игра не началась, ожидаем нажатия клавиши Enter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_started = True

    if game_started:
        # Управление динозавром
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dino_y -= dino_speed
        if keys[pygame.K_DOWN]:
            dino_y += dino_speed

        # Ограничение движения динозавра по оси Y
        if dino_y < 0:
            dino_y = 0
        elif dino_y > screen_height - dino_height:
            dino_y = screen_height - dino_height

        # Движение астероида
        asteroid_x -= asteroid_speed

        # Проверка, если астероид касается левой границы экрана, увеличиваем счет
        if asteroid_x <= 0:
            score += 1

        # Проверка, если астероид зашел за левую границу экрана, генерируем новый астероид
        if asteroid_x < 0:
            asteroid_x = 800
            asteroid_y = random.randint(50, 550)  # Генерация случайной позиции Y

        # Проверка столкновения
        if dino_x + dino_width > asteroid_x and dino_x < asteroid_x + asteroid_width:
            if dino_y + dino_height > asteroid_y and dino_y < asteroid_y + asteroid_height:
                score -= 1  # Уменьшить счет при столкновении

    # Отрисовка на экране
    screen.fill(white)

    if not game_started:
        # Если игра не началась, отображаем инструкцию
        instructions = wrap_text("Помоги квадратному динозавру уворачиваться от квадратных астероидов. Управление квадратным динозавром: стрелочки вверх и вниз. Для начала игры нажми Enter", instruction_font, screen_width - 20)
        for i, line in enumerate(instructions):
            text = instruction_font.render(line, True, black)
            screen.blit(text, (10, 100 + i * instruction_font.get_height()))
    else:
        # Если игра началась, отображаем игровые объекты
        pygame.draw.rect(screen, dark_green, (dino_x, dino_y, dino_width, dino_height))
        pygame.draw.rect(screen, red, (asteroid_x, asteroid_y, asteroid_width, asteroid_height))

        # Отображение счета
        font = pygame.font.Font(None, 36)
        text = font.render(f"Счет: {score}", True, black)
        screen.blit(text, (10, 10))

        # Завершение игры при достижении определенного счета
        if score < -1:
            running = False

    pygame.display.update()

# Завершение игры
pygame.quit()
sys.exit()
