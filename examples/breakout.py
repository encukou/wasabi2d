import random
import colorsys
from collections import deque
from math import copysign
from wasabi2d import event, run, Scene


WIDTH = 600
HEIGHT = 800
scene = Scene(WIDTH, HEIGHT)


BALL_SIZE = 6
MARGIN = 50

BRICKS_X = 10
BRICKS_Y = 5
BRICK_W = (WIDTH - 2 * MARGIN) / BRICKS_X
BRICK_H = 25


ball = scene.layers[0].add_circle(
    pos=(WIDTH / 2, HEIGHT / 2),
    radius=BALL_SIZE,
    color='#cccccc',
    fill=False,
)
bat = scene.layers[0].add_rect(
    pos=(WIDTH / 2, HEIGHT - 50),
    width=120,
    height=12,
    color='pink',
    fill=True,
)


bricks = []


def reset():
    """Reset bricks and ball."""
    # First, let's do bricks
    for b in bricks:
        b.delete()
    del bricks[:]
    for x in range(BRICKS_X):
        for y in range(BRICKS_Y):
            hue = (x + y) / BRICKS_X
            saturation = (y / BRICKS_Y) * 0.5 + 0.5
            brick = scene.layers[0].add_rect(
                pos=((x + 0.5) * BRICK_W + MARGIN,
                     (y + 0.5) * BRICK_H + MARGIN),
                color=colorsys.hsv_to_rgb(hue, saturation, 0.8),
                width=BRICK_W,
                height=BRICK_H,
                fill=True,
            )
            #brick.highlight = hsv_color(hue, saturation * 0.7, 1.0)
            bricks.append(brick)

    # Now reset the ball
    ball.pos = (WIDTH / 2, HEIGHT / 3)
    ball.vel = (random.uniform(-200, 200), 400)


# Reset bricks and ball at start
reset()


@event
def update():
    # When you have fast moving objects, like the ball, a good trick
    # is to run the update step several times per frame with tiny time steps.
    # This makes it more likely that collisions will be handled correctly.
    for _ in range(3):
        update_step(1 / 180)
    update_bat_vx()


def update_step(dt):
    x, y = ball.pos
    vx, vy = ball.vel

    if ball.top > HEIGHT:
        reset()
        return

    # Update ball based on previous velocity
    x += vx * dt
    y += vy * dt
    ball.pos = (x, y)

    # Check for and resolve collisions
    if ball.left < 0:
        vx = abs(vx)
        ball.left = -ball.left
    elif ball.right > WIDTH:
        vx = -abs(vx)
        ball.right -= 2 * (ball.right - WIDTH)

    if ball.top < 0:
        vy = abs(vy)
        ball.top *= -1

    if ball.colliderect(bat):
        vy = -abs(vy)
        # Add some spin off the paddle
        vx += -30 * bat.vx
    else:
        # Find first collision
        idx = ball.collidelist(bricks)
        if idx != -1:
            brick = bricks[idx]
            # Work out what side we collided on
            dx = (ball.centerx - brick.centerx) / BRICK_W
            dy = (ball.centery - brick.centery) / BRICK_H
            if abs(dx) > abs(dy):
                vx = copysign(abs(vx), dx)
            else:
                vy = copysign(abs(vy), dy)
            brick.delete()
            del bricks[idx]

    ball.vel = (vx, vy)


# Keep bat vx history over 5 frames
bat.recent_vxs = deque(maxlen=5)
bat.vx = 0
bat.prev_centerx = bat.pos[0]


def update_bat_vx():
    """Recalculate average bat vx."""
    x = bat.pos[0]
    dx = x - bat.prev_centerx
    bat.prev_centerx = x

    history = bat.recent_vxs
    history.append(dx)
    vx = sum(history) / len(history)
    bat.vx = min(10, max(-10, vx))


@event
def on_mouse_move(pos):
    x, y = pos
    bat.pos = x, bat.pos[1]
    if bat.left < 0:
        bat.left = 0
    elif bat.right > WIDTH:
        bat.right = WIDTH


run()
