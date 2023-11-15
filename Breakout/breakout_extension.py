"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
"""
File: breakout_extension.py
Name: Andy Lin
"""

from campy.gui.events.timer import pause
from campy.graphics.gobjects import GOval, GRect, GLabel, GArc, GPolygon
from breakoutgraphics_extension import BreakoutGraphicsExtension
import random

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts
BIGGER_BALL = 20
EXTENDED_PADDLE = 100
GRAVITY = 1.2
REDUCE = 0.9
score = 0
anti_gravity_mode = False
anti_gravity_time_left = 5
big_touched = 0
max_ball_size = 20
ball_size_check = 0


def main():
    # Import the class
    graphics = BreakoutGraphicsExtension()
    # Initialize ball speed from getter
    vx = graphics.get_vx()
    vy = graphics.get_vy()
    # Count the number of live
    lives = graphics.lives
    # Special tools drop velocity
    tool_vy = graphics.tool_vy()
    # Add the animation loop here!
    while True:
        if graphics.play_again:
            while True:
                global anti_gravity_mode, anti_gravity_time_left
                # pause
                pause(FRAME_RATE*2)
                # move ball if switch on button
                if graphics.game_running:  # Switch on button, let ball bounce until game over
                    # Check if in anti-gravity mode
                    if anti_gravity_mode:
                        anti_gravity_time_left -= 0.05
                        graphics.anti_gravity_label.text = "^^^^^: " + str(int(anti_gravity_time_left))
                        if anti_gravity_time_left <= 0:  # Turn off the anti-gravity button
                            anti_gravity_mode = False
                        else:                            # Keep anti-gravity bouncing
                            vy -= GRAVITY                # Reduce the bouncing distance
                    # Time reduce
                    graphics.time_left -= 0.02
                    graphics.time_label.text = "Time Left: " + str(int(graphics.time_left))
                    # Losing situation 1: time end, show losing label
                    if graphics.time_left <= 0:
                        graphics.game_over = True     # Switch off the button so can click restart
                        label = game_over(win=False)  # Game lose, print losing label
                        graphics.window.add(label, x=(graphics.window.width - graphics.score_board.width) // 2 - 40,
                                       y=graphics.window.height // 2 + 20)
                        # Store high score
                        if graphics.score > graphics.high_score:
                            graphics.high_score = graphics.score
                            graphics.high_score_board.text = 'High Score: ' + str(int(graphics.high_score))
                        else:
                            graphics.high_score = graphics.score
                        break
                    # Calculating score
                    graphics.score_label.text = "Scores: " + str(graphics.score)
                    # Winning situation
                    if graphics.brick_count == 0:        # Winning condition
                        print('You Win!')
                        # Calculate end score and set high score
                        graphics.score = graphics.time_left * 100 + graphics.score
                        if graphics.score > graphics.high_score:
                            graphics.high_score = graphics.score
                            graphics.high_score_board.text = 'High Score: ' + str(int(graphics.high_score))
                        else:
                            graphics.high_score = graphics.score
                        graphics.game_over = True    # Switch off the button so can click restart
                        label = game_over(win=True)  # Game win, print winning label
                        graphics.window.add(label, x=(graphics.window.width - graphics.score_board.width) // 2 - 40,
                                       y=graphics.window.height // 2 + 20)
                        break
                    # Fail to bounce situation
                    if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                        lives -= 1
                        # Remove current ball
                        graphics.window.remove(graphics.ball)
                        # Remove all live balls
                        for graphics.ball in graphics.lives_ball:
                            graphics.window.remove(graphics.ball)
                        graphics.lives_ball.clear()   # Clear list
                        # Reset lives balls x position
                        graphics.live_x_position = graphics.live_label.x + graphics.live_label.width + 5
                        # Show lives remaining with balls
                        for i in range(lives):       # Print remaining lives
                            live_remain = GOval(graphics.ball.width, graphics.ball.height, x=graphics.live_x_position,
                                                y=graphics.live_y_position)
                            live_remain.filled = True
                            live_remain.fill_color = 'royalblue'
                            graphics.window.add(live_remain)
                            graphics.lives_ball.append(live_remain)
                            graphics.live_x_position += 25
                        print("Lives: " + str(lives))
                        if lives > 0:                      # Check if still has lives
                            graphics.game_running = False  # Switch off button and reset ball velocity
                            graphics.is_ball_started = False
                            graphics.set_ball_velocity()
                            # Initialize ball's velocity
                            vx = graphics.get_vx()
                            vy = graphics.get_vy()
                            # Reset ball position
                            graphics.window.add(graphics.ball, x=(graphics.window.width - graphics.score_board.width)//2,
                                                y=graphics.window.height//2)
                        else:
                            # Losing situation 2: No lives left, show losing label
                            graphics.game_over = True
                            label = game_over(win=False)  # Game lose, print losing label
                            print("You Lose!")
                            graphics.window.add(label, x=(graphics.window.width - graphics.score_board.width)//2 - 60,
                                                y=graphics.window.height//2)
                            if graphics.score > graphics.high_score:
                                graphics.high_score = graphics.score
                                graphics.high_score_board.text = 'High Score: ' + str(int(graphics.high_score))
                            else:
                                graphics.high_score = graphics.score
                            break
                    graphics.ball.move(vx, vy)
                # bouncing if touch the left and right wall, and reset ball.x
                # Check left wall
                if graphics.ball.x <= 0:
                    vx = -vx
                    graphics.ball.x = 0
                # Check right wall
                elif graphics.ball.x + graphics.ball.width >= graphics.window.width - graphics.score_board.width:
                    vx = -vx
                    graphics.ball.x = graphics.window.width - graphics.score_board.width - graphics.ball.width
                # bouncing if touch the top and down wall, and reset ball.y
                if graphics.ball.y <= 0:
                    vy = -vy
                    graphics.ball.y = 0

                # Bouncing if touch the paddle and bricks
                collided = False        # Switch button for checking if ball touches things

                for i in range(2):
                    if collided:
                        break
                    for j in range(2):  # Check every corner of the ball with for loop
                        obj = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width * i,
                                                            graphics.ball.y + graphics.ball.height * j)
                        if obj is graphics.paddle:
                            graphics.window.add(graphics.ball, x=graphics.ball.x, y=obj.y-graphics.ball.height-1)
                            vy = -vy
                            # Need to break and out of for loop so the ball could recheck after touched one corner
                            collided = True
                            break
                        # Hit the bricks
                        elif obj in graphics.bricks_set:  # Make sure only bricks will be remove
                            brick_row = graphics.get_brick_row()
                            if 8 < brick_row <= 10:
                                graphics.score += 20
                            elif 6 < brick_row <= 8:
                                graphics.score += 40
                            elif 4 < brick_row <= 6:
                                graphics.score += 60
                            elif 2 < brick_row <= 4:
                                graphics.score += 80
                            elif 0 < brick_row <= 2:
                                graphics.score += 100
                            graphics.window.remove(obj)
                            graphics.bricks_set.remove(obj)
                            vy = -vy
                            graphics.brick_count -= 1
                            print("Bricks remain: ", str(graphics.brick_count))
                            # Initiate random tool
                            tool_num = random.randint(1, 10)
                            print(tool_num)
                            if tool_num in [1, 3, 5]:  # Only for valid tool number
                                if tool_num == 1:  # Bigger ball
                                    graphics.window.add(graphics.bigger_ball, obj.x, obj.y)
                                    graphics.falling_tools.append(graphics.bigger_ball)
                                elif tool_num == 3:  # Expend paddle
                                    graphics.window.add(graphics.extend_paddle, obj.x, obj.y)
                                    graphics.falling_tools.append(graphics.extend_paddle)
                                elif tool_num == 5:   # Anti-gravity
                                    graphics.window.add(graphics.anti_gravity, obj.x, obj.y)
                                    graphics.falling_tools.append(graphics.anti_gravity)
                            collided = True
                            break
                for tool in graphics.falling_tools:
                    tool.move(0, tool_vy)
                    # Check if the tool is out of the window
                    if tool.y - tool.height > graphics.window.height:
                        graphics.window.remove(tool)
                        graphics.falling_tools.remove(tool)
                #  Initiate special tool if paddle touch it
                for i in range(graphics.paddle.width + 1):
                    # Check every point of the paddle with for loop
                    paddle = graphics.window.get_object_at(graphics.paddle.x + i, graphics.paddle.y)
                    if paddle is graphics.bigger_ball and graphics.ball.width <= max_ball_size:
                        bigger_ball(graphics)
                    elif paddle is graphics.extend_paddle:
                        extend_paddle(graphics)
                    elif paddle is graphics.anti_gravity:
                        anti_gravity(graphics)
            graphics.play_again = False   # If end game, turn off the button
            lives = graphics.lives        # Since the game end and the game need to restart, lives should be reset.
        pause(FRAME_RATE)


def game_over(win):  # Winning and losing label
    if win:
        label = GLabel("You win!!")
        label.font = '-40'
        label.color = 'royalblue'
    else:
        label = GLabel("GGWP")
        label.font = '-40'
        label.color = 'rosybrown'
    return label


def anti_gravity(graphics):
    global anti_gravity_mode, anti_gravity_time_left
    print("The ball will be anti-gravity!")
    # Start anti-gravity ball
    anti_gravity_mode = True
    anti_gravity_time_left = 6
    # Remove anti_gravity tool from the window
    graphics.window.remove(graphics.anti_gravity)
    graphics.falling_tools.remove(graphics.anti_gravity)
    # Store old ball position and radius
    anti_ball_x = graphics.ball.x
    anti_ball_y = graphics.ball.y
    anti_ball_width = graphics.ball.width
    anti_ball_height = graphics.ball.height
    # Remove current ball
    graphics.window.remove(graphics.ball)
    # Create a new ball
    graphics.ball = GOval(anti_ball_width, anti_ball_height)
    graphics.ball.filled = True
    graphics.ball.fill_color = 'royalblue'
    # Set the new ball position
    graphics.window.add(graphics.ball, x=anti_ball_x, y=anti_ball_y)


def extend_paddle(graphics):
    print("The paddle will bigger twice!")
    # Store old center positions for the paddle
    old_p_center_x = graphics.paddle.x + graphics.paddle.width / 2
    old_p_center_y = graphics.paddle.y + graphics.paddle.height / 2
    # Double the paddle's size and limit its to the length of bouncing wall
    new_paddle_w = graphics.paddle.width * 2
    graphics.extend_paddle_label.text = "<===>: " + str(int(new_paddle_w))
    if new_paddle_w >= graphics.window.width - graphics.score_board.width:
        new_paddle_w = graphics.window.width - graphics.score_board.width
    new_paddle_h = graphics.paddle.height
    # Remove current paddle
    graphics.window.remove(graphics.paddle)
    # Create a new paddle
    graphics.paddle = GRect(new_paddle_w, new_paddle_h)
    graphics.paddle.filled = True
    graphics.paddle.fill_color = 'gray'
    # Set the new ball position so it remains its center as old ball
    new_paddle_x = old_p_center_x - new_paddle_w / 2
    new_paddle_y = old_p_center_y - new_paddle_h / 2
    graphics.window.add(graphics.paddle, x=new_paddle_x, y=new_paddle_y)
    # Remove bigger_ball tool from the window
    graphics.window.remove(graphics.extend_paddle)
    graphics.falling_tools.remove(graphics.extend_paddle)


def bigger_ball(graphics):
    global big_touched, ball_size_check
    big_touched += 1
    ball_size_check += 1
    print("The ball will bigger twice!")
    graphics.bigger_ball_label.text = "B : X" + str(int(ball_size_check))
    # Store old center positions for the ball
    old_b_center_x = graphics.ball.x + graphics.ball.width / 2
    old_b_center_y = graphics.ball.y + graphics.ball.height / 2
    # Double the ball's size
    new_ball_width = graphics.ball.width * 2
    new_ball_height = graphics.ball.height * 2
    # Remove current ball
    graphics.window.remove(graphics.ball)
    # Create a new ball with double size
    graphics.ball = GOval(new_ball_width, new_ball_height)
    graphics.ball.filled = True
    graphics.ball.fill_color = 'royalblue'
    # Set the new ball position so it remains its center as old ball
    new_ball_x = old_b_center_x - new_ball_width / 2
    new_ball_y = old_b_center_y - new_ball_height / 2
    graphics.window.add(graphics.ball, x=new_ball_x, y=new_ball_y)
    # Remove bigger_ball tool from the window
    graphics.window.remove(graphics.bigger_ball)
    graphics.falling_tools.remove(graphics.bigger_ball)


if __name__ == '__main__':
    main()
