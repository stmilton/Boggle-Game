"""
Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 3  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.__paddle = GRect(paddle_width, paddle_height, x=(self.window.width - paddle_width) / 2,
                              y=self.window.height - paddle_offset - paddle_height)
        self.__paddle.filled = True
        self.__paddle.fill_color = 'gray'
        self.window.add(self.__paddle)
        # Center a filled ball in the graphical window
        self.ball_radius = ball_radius
        self.ball = GOval(ball_radius * 2, ball_radius * 2, x=self.window_width / 2 - ball_radius,
                          y=self.window_height / 2 - ball_radius)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball)
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners
        onmouseclicked(self.start)
        onmousemoved(self.paddle_move)
        # Draw bricks
        self.num_bricks = 0
        for i in range(brick_rows):
            for j in range(brick_cols):
                c = random.randint(1, 5)
                if c == 1:
                    random_color = 'red'
                elif c == 2:
                    random_color = 'blue'
                elif c == 3:
                    random_color = 'green'
                else:
                    random_color = 'yellow'
                self.__brick = GRect(brick_width, brick_height)
                self.__brick.filled = True
                self.__brick.fill_color = random_color
                self.window.add(self.__brick, x=j * (brick_width + brick_spacing),
                                y=brick_offset + i * (brick_height + brick_spacing))
                self.num_bricks += 1
        # print(self.num_bricks)
        self.life = 3
        self.life_board = GLabel('❤' * self.life)
        self.life_board.color = 'red'
        self.life_board.font = '-30'
        self.window.add(self.life_board, x=0, y=self.window_height)
        self.score = 0
        self.score_board = GLabel('Score: '+str(self.score))
        self.score_board.color = 'blue'
        self.score_board.font = '-30'
        self.window.add(self.score_board, x=250, y=self.window_height)

    def set_ball_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = random.randint(INITIAL_Y_SPEED, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def start(self, m):
        if self.__dx == 0 and self.__dy == 0:
            self.set_ball_velocity()

    def paddle_move(self, m):
        self.__paddle.x = m.x - self.__paddle.width / 2
        if self.__paddle.x <= 0:
            self.__paddle.x = 0
        if self.__paddle.x + self.__paddle.width >= self.window.width:
            self.__paddle.x = self.window.width - self.__paddle.width

    def move_dx(self, count=1):
        self.__dx = self.__dx * count
        return self.__dx

    def move_dy(self, count=1):
        self.__dy = self.__dy * count
        return self.__dy

    def ball_x_in_window(self):
        is_ball_x_in_window = 0 < self.ball.x < self.window.width - self.ball_radius * 2
        return is_ball_x_in_window

    def ball_y_in_window(self):
        is_ball_y_in_window = 0 < self.ball.y
        return is_ball_y_in_window

    def is_die(self):
        if self.ball.y >= self.window.height - self.ball_radius * 2:
            self.ball.x = self.window_width / 2 - self.ball_radius
            self.ball.y = self.window_height / 2 - self.ball_radius
            self.__dx = 0
            self.__dy = 0
            self.life -= 1
            self.window.remove(self.life_board)
            self.life_board = GLabel("❤" * self.life)
            self.life_board.color = 'red'
            self.life_board.font = '-30'
            self.window.add(self.life_board, x=0, y=self.window_height)

    def detect(self, p):
        if p is not None and p is not self.life_board and p is not self.score_board and p is not self.__paddle:
            return True
        return False

    def is_brick(self, p):
        if self.ball.y < self.__paddle.y - self.ball_radius * 2:
            self.window.remove(p)
            self.update_score()
            print(p)

    def is_paddle(self, p):
        if p is self.__paddle:
            return True
        return False

    def update_score(self):
        self.score += 1
        self.num_bricks -= 1
        self.window.remove(self.score_board)
        self.score_board = GLabel('Score: ' + str(self.score))
        self.score_board.color = 'blue'
        self.score_board.font = '-30'
        self.window.add(self.score_board, x=250, y=self.window_height)

    def is_collision(self):
        detection_value = BALL_RADIUS//10*3
        upper_left_corner = self.window.get_object_at(self.ball.x, self.ball.y)
        upper_left_left = self.window.get_object_at(self.ball.x - detection_value, self.ball.y + detection_value)
        upper_left_upper = self.window.get_object_at(self.ball.x + detection_value, self.ball.y - detection_value)
        upper_right_corner = self.window.get_object_at(self.ball.x + self.ball_radius * 2, self.ball.y)
        upper_right_right = self.window.get_object_at(self.ball.x + self.ball_radius * 2 + detection_value,
                                                      self.ball.y + detection_value)
        upper_right_upper = self.window.get_object_at(self.ball.x + self.ball_radius * 2 - detection_value,
                                                      self.ball.y - detection_value)
        lower_left_corner = self.window.get_object_at(self.ball.x, self.ball.y + self.ball_radius * 2)
        lower_left_left = self.window.get_object_at(self.ball.x - detection_value,
                                                    self.ball.y + self.ball_radius * 2 - detection_value)
        lower_left_lower = self.window.get_object_at(self.ball.x + detection_value,
                                                     self.ball.y + self.ball_radius * 2 + detection_value)
        lower_right_corner = self.window.get_object_at(self.ball.x + self.ball_radius * 2,
                                                       self.ball.y + self.ball_radius * 2)
        lower_right_right = self.window.get_object_at(self.ball.x + self.ball_radius * 2 + detection_value,
                                                      self.ball.y + self.ball_radius * 2 - detection_value)
        lower_right_lower = self.window.get_object_at(self.ball.x + self.ball_radius * 2 - detection_value,
                                                      self.ball.y + self.ball_radius * 2 + detection_value)

        if self.detect(upper_left_corner):
            if upper_left_left is not None:
                self.is_brick(upper_left_left)
                self.move_dx(-1)
                print('upper_left_left')
            elif upper_left_upper is not None:
                self.is_brick(upper_left_upper)
                self.move_dy(-1)
                print('upper_left_upper')
        elif self.detect(upper_right_corner):
            if upper_right_right is not None:
                self.is_brick(upper_right_right)
                self.move_dx(-1)
                print('upper_right_right')
            elif upper_right_upper is not None:
                self.is_brick(upper_right_upper)
                self.move_dy(-1)
                print('upper_right_upper')
        elif self.detect(lower_left_corner):

            if lower_left_left is not None:
                self.is_brick(lower_left_left)
                self.move_dx(-1)
                print('lower_left_left')

            elif lower_left_lower is not None:
                self.is_brick(lower_left_lower)
                self.move_dy(-1)
                print('lower_left_lower')
        elif self.detect(lower_right_corner):
            if lower_right_right is not None:
                self.is_brick(lower_right_right)
                self.move_dx(-1)
                print('lower_right_right')
                # if self.is_paddle(lower_right_corner) and self.__dy >= 0:
                #     self.move_dy(-1)
            elif lower_right_lower is not None:
                self.is_brick(lower_right_lower)
                self.move_dy(-1)
                print('lower_right_lower')

        if self.is_paddle(lower_right_corner) and self.__dy >= 0:
            self.move_dy(-1)
        elif self.is_paddle(lower_left_corner) and self.__dy >= 0:
            self.move_dy(-1)
