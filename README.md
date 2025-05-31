This project is a recreation of the classic arcade game Space Invaders, built entirely with Python's built-in Turtle graphics module. It's a fun example of basic game development principles.

Space Invaders Game Screenshot
The game features a player spaceship, enemy aliens, and defensive barriers. Players can move left and right, fire bullets, and aim to clear the screen of invaders. The game includes logic for collision detection, scorekeeping, and managing different game states (welcome screen, active play, paused, game over, and win).

Key features and concepts demonstrated:

Real-time Animation: Smooth movement of game objects using `wn.tracer(0)` for efficient updates.
Game Entities: Player, aliens, bullets, and destructible barriers are represented by Turtle objects.
Collision Handling: Detects when bullets hit aliens or barriers, and when aliens reach the player or the bottom of the screen.
Keyboard Controls: Responds to user input for ship movement, firing, and pausing.
Game Flow Management: Transitions between welcome, active, paused, game over, and win screens, and includes a restart option.
