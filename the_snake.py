from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка! Для прекращения игры нажмите ESC.')


# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс всех игровых объектов."""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw_a_cell(self, position):
        """Метод, отрисовывающий ячейку."""
        rect = pg.Rect(
            (self.position),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод, определяющий отрисовку объекта на экране.
        Будет переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий игровой объект - яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = (
            randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
        )

    def randomize_position(self, snake_positions):
        """Метод, задающий рандомные координаты яблока после поедания."""

        self.position = (
            randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
        )

        if self.position in snake_positions.positions:
            self.randomize_position()

        return self.position

    def draw(self):
        """Метод отрисовки яблока на экране."""
        self.draw_a_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий игровой объект - змейку."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.directions = (LEFT, RIGHT, UP, DOWN)
        self.length = self.reset()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод, определяющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод, отвечающий за расчет позиции змейки
        с учётом игровых событий.
        """
        current_head_position = self.get_head_position()
        new_head_position = (
            (current_head_position[0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (current_head_position[1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )

        if new_head_position in self.positions:
            self.reset()
        
        else: 
            self.positions.insert(0, new_head_position)

        self.last = self.positions[len(self.positions) - 1]

        if len(self.positions) > self.length:
            self.positions.pop()
        
    def reset(self):
        """Метод, обрабатывающий столкновение змейки с собой же."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(self.directions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        return self.length
    
    def draw(self, screen):
        """Метод отрисовки змейки на экране."""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Функция, обрабатывающая нажатия клавиш игроком и
    закрытие игрового окна.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Функция, реализующая основную логику игры."""
    apple = Apple()
    snake = Snake()
    
    

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake)
        
        
        snake.move()
        
        
        apple.draw()
        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
