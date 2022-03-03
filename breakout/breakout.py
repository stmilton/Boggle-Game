"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.graphics.gobjects import GOval, GRect, GLabel


FRAME_RATE = 1000 / 100  # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    # Add animation loop here!
    while True:
        if graphics.life == 0:
            graphics.window.clear()
            game_over = GLabel("Game Over")
            game_over.color = 'red'
            game_over.font = '-60'
            graphics.window.add(game_over, x=40, y=graphics.window.height/2)
            break
        if graphics.num_bricks == 0:
            graphics.window.clear()
            game_over = GLabel("You Win")
            game_over.color = 'red'
            game_over.font = '-60'
            graphics.window.add(game_over, x=60, y=graphics.window.height / 2)
        pause(FRAME_RATE)
        graphics.ball.move(graphics.move_dx(), graphics.move_dy())
        graphics.is_collision()

        if not graphics.ball_x_in_window():
            graphics.move_dx(-1)
        if not graphics.ball_y_in_window():
            graphics.move_dy(-1)
        graphics.is_die()






if __name__ == '__main__':
    main()
