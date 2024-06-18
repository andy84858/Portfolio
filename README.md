# Portfolio: Breakout


These two Python files, `breakout_extension.py` and `breakoutgraphics_extension.py`, together form a simple game inspired by "Block 130." 
The game's goal is to break all the blocks on the screen using a bouncing ball, while controlling a paddle to prevent the ball from falling off the game area.

* Gameplay
Players use the mouse to control a paddle, catching the ball as it bounces back and forth. The ball breaks blocks when it hits them, scoring points in the process. If the ball hits the screen's edges, it bounces back; however, if it falls off the bottom edge, the player loses a life. If all lives are lost, the game ends. The player wins by breaking all the blocks.

* Key Techniques
These files use several Python techniques, including:

1. Object-Oriented Programming: breakoutgraphics_extension.py defines a BreakoutGraphicsExtension class containing the paddle, blocks, ball, and other related game logic and objects.
2. Event-Driven Programming: Functions like onmouseclicked and onmousemoved handle mouse events, allowing the game to respond to user input.
3. Animation Loop: breakout_extension.py features a main loop that uses a timer to control animation. It uses the pause function for a consistent frame rate, ensuring smooth motion in the game.
4. Game State Management: Multiple global variables track the game's state, such as score, number of lives, and special tool status.

   
* Core Features
1. Block Generation: At the beginning of the game, a series of blocks are generated, and they're updated based on various conditions.
2. Mouse Control: Players use the mouse to move the paddle and start the game.
3. Special Tools: The game includes special tools(e.g Anti-Gravity, extended paddle, bigger ball) that add additional gameplay variations.
