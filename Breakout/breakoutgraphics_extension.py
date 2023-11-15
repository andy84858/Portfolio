"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
"""
File: breakoutgraphic_extension.py
Name: Andy Lin
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GArc, GPolygon, GLine
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
SCORE_BOARD_W = 200    # Score board for score label, count time and other special tool
TOOL_DROP_SPEED = 3
NUM_LIVES = 3


class BreakoutGraphicsExtension:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 score_board_w=SCORE_BOARD_W, title='Breakout_extension'):
        # Set number of lives in beginning
        self.lives = NUM_LIVES
        # Set play again button if turn on it
        self.play_again = True
        # Create a switch button control whether start ball movement or restart game
        self.game_over = False
        # Create a graphical window, with score board
        bouncing_wall_w = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_width = bouncing_wall_w + score_board_w
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        # Create score board
        self.score_board = GRect(score_board_w, window_height, x=bouncing_wall_w, y=0)
        self.score_board.filled = True
        self.score_board.fill_color = 'gray'
        self.window.add(self.score_board)
        # Create score label
        self.score = 0
        self.score_label = GLabel('Score:    ' + str(self.score))
        self.score_label.x = bouncing_wall_w + 10
        self.score_label.y = 30
        self.score_label.font = '-20'
        self.score_label.color = 'black'
        self.window.add(self.score_label, self.score_label.x, self.score_label.y)
        # Create a time label
        self.time_left = 120  # Count down for 120 seconds
        self.time_label = GLabel('Time Left:   ' + str(self.time_left))
        self.time_label.x = bouncing_wall_w + 10
        self.time_label.y = 60
        self.time_label.font = "-20"
        self.time_label.color = 'black'
        self.window.add(self.time_label, self.time_label.x, self.time_label.y)
        # Create remaining lives label
        self.live_label = GLabel("Lives: ")
        self.live_label.x = bouncing_wall_w + 10
        self.live_label.y = 90
        self.live_label.font = '-20'
        self.live_label.color = 'black'
        self.window.add(self.live_label, self.live_label.x, self.live_label.y)
        # initial 3 lives position
        self.live_x_position = self.live_label.x + self.live_label.width + 5
        self.live_y_position = self.live_label.y - self.live_label.height
        self.lives_ball = []
        for i in range(3):
            self.live_remain = GOval(ball_radius, ball_radius, x=self.live_x_position, y=self.live_y_position)
            self.live_remain.filled = True
            self.live_remain.fill_color = 'royalblue'
            self.window.add(self.live_remain)
            self.lives_ball.append(self.live_remain)
            self.live_x_position += 25
        # Create special tool label
        self.special_tool = GLabel('Special Tools')
        self.special_tool.font = '-20'
        self.special_tool.color = 'black'
        self.special_tool_x = bouncing_wall_w + 10
        self.separate_line_1 = GLine(bouncing_wall_w, 130, window_width, 130)
        self.separate_line_2 = GLine(bouncing_wall_w, 300, window_width, 300)
        self.window.add(self.special_tool, self.special_tool_x, 160)
        self.window.add(self.separate_line_1)
        self.window.add(self.separate_line_2)
        self.bigger_ball_label = GLabel('B : ')
        self.bigger_ball_label.font = '-30'
        self.bigger_ball_label.color = 'blue'
        self.bigger_ball_l_x = bouncing_wall_w + 10
        self.extend_paddle_label = GLabel('<===> : ')
        self.extend_paddle_label.font = '-30'
        self.extend_paddle_label.color = 'Green'
        self.extend_paddle_l_x = bouncing_wall_w + 10
        self.anti_gravity_label = GLabel('^^^^^ : ')
        self.anti_gravity_label.font = '-30'
        self.anti_gravity_label.color = 'pink'
        self.anti_gravity_l_x = bouncing_wall_w + 10
        self.window.add(self.bigger_ball_label, self.bigger_ball_l_x, 210)
        self.window.add(self.extend_paddle_label, self.extend_paddle_l_x, 250)
        self.window.add(self.anti_gravity_label, self.anti_gravity_l_x, 290)
        # Create highest score board
        self.high_score = 0
        self.high_score_board = GLabel("High Score: ")
        self.high_score_board.x = bouncing_wall_w + 10
        self.high_score_board.y = 120
        self.high_score_board.font = '-20'
        self.high_score_board.color = 'black'
        self.window.add(self.high_score_board, self.high_score_board.x, self.high_score_board.y)
        # Create restart button
        # self.create_restart_button()
        button_width = 100
        button_height = 40
        button_x = self.window.width - button_width - 50
        button_y = 320
        self.restart_button = GRect(button_width, button_height, x=button_x, y=button_y)
        self.restart_button.filled = True
        self.restart_button.fill_color = 'gray'
        self.restart_button.color = 'black'

        self.restart_label = GLabel("RESTART")
        self.restart_label.font = "-15"
        restart_label_x = button_x + (button_width - self.restart_label.width) / 2
        restart_label_y = button_y + (button_height + self.restart_label.height) / 2

        self.window.add(self.restart_button)
        self.window.add(self.restart_label, x=restart_label_x, y=restart_label_y)
        # Draw a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(bouncing_wall_w-paddle_width)/2,
                            y=(window_height-paddle_offset-paddle_height))
        self.paddle.filled = True
        self.paddle.fill_color = 'gray'
        self.window.add(self.paddle)
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius, x=bouncing_wall_w/2, y=window_height/2)
        self.ball.filled = True
        self.ball.fill_color = 'royalblue'
        self.window.add(self.ball)
        # Brick count
        self.brick_count = brick_cols * brick_rows

        # Special tools - Bigger ball
        self.bigger_ball = GLabel('B')
        self.bigger_ball.font = '-40'
        self.bigger_ball.color = 'blue'
        # Special tools - Extend paddle
        self.extend_paddle = GLabel('<===>')
        self.extend_paddle.font = '-40'
        self.extend_paddle.color = 'Green'
        # Special tools - Anti-gravity
        self.anti_gravity = GLabel('^^^^^')
        self.anti_gravity.font = '-40'
        self.anti_gravity.color = 'pink'
        # Special tool list
        self.falling_tools = []
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        # Initialize our mouse listeners
        onmousemoved(self.move_paddle)
        onmouseclicked(self.handle_mouse_click)
        # Initial ball movement
        self.is_ball_started = False  # Start the ball when clicked the mouse
        self.game_running = False    # The initial stage, where the game not in playing
        # Draw bricks
        self.bricks_set = set()                               # Set empty set and put bricks in so can check them later
        brick_x = 0                                           # Initial position x
        brick_y = brick_offset                                # Initial position y
        for i in range(brick_cols):
            for j in range(brick_rows):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                if i <= 1:
                    self.brick.fill_color = 'red'
                elif 1 < i <= 3:
                    self.brick.fill_color = 'orange'
                elif 3 < i <= 5:
                    self.brick.fill_color = 'yellow'
                elif 5 < i <= 7:
                    self.brick.fill_color = 'green'
                else:
                    self.brick.fill_color = 'blue'
                self.window.add(self.brick, brick_x, brick_y)
                self.bricks_set.add(self.brick)               # Add brick in set when create a brick
                brick_x = brick_x + brick_width + brick_spacing
            brick_x = 0                                       # Reset brick_x
            brick_y = brick_y + brick_height + brick_spacing  # Move to next row

    def move_paddle(self, mouse):
        # mouse.x equals to middle of paddle
        self.paddle.x = mouse.x - self.paddle.width//2
        # Limit to left edge
        if mouse.x <= 0:
            self.paddle.x = 0
        # Limit to right edge
        elif mouse.x + (self.paddle.width//2) >= self.score_board.x:
            self.paddle.x = (self.window.width - self.score_board.width) - self.paddle.width

    def handle_mouse_click(self, event):  # Check for the mouse click to start or restart the game
        print("Mouse clicked!")  # Test if mouse is clicked
        if self.game_over:
            print('Game is over. Checking restart button')
            if self.restart_button.x <= event.x <= self.restart_button.x + self.restart_button.width \
                    and self.restart_button.y <= event.y <= self.restart_button.y + self.restart_button.height:
                print('Restart button clicked!')
                self.reset_game()
        else:
            # Ball is not moving(False situation), need to click mouse to let ball move
            if not self.is_ball_started and not self.game_over:
                self.is_ball_started = True
                self.game_running = True

    def set_ball_velocity(self):   # Determine the ball velocity
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

    @staticmethod
    def get_vx():
        return random.randint(1, MAX_X_SPEED)

    @staticmethod
    def get_vy():
        return INITIAL_Y_SPEED

    @staticmethod
    def tool_vy():
        return TOOL_DROP_SPEED

    def get_brick_row(self):  # Count the row when the brick is broken
        hit_brick_y = self.ball.y + self.brick.height
        row = int(hit_brick_y - BRICK_OFFSET) // (BRICK_HEIGHT + BRICK_SPACING)
        return row

    def reset_game(self):
        # Turn off game running button
        self.game_running = False
        self.is_ball_started = False
        # Store the current high score before clearing everything
        current_high_score = self.high_score
        # Clear the window
        self.window.clear()
        # Reset all game attributes except for high_score
        self.__init__()
        # Restore the high score
        self.high_score = current_high_score
        self.high_score_board.text = 'High Score: ' + str(self.high_score)



