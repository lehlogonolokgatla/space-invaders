import turtle
import math
import time

# --- Game Screen Setup ---
wn = turtle.Screen()
wn.setup(width=600, height=800, startx=0, starty=0)
wn.bgcolor("black")
wn.title("Space Invaders")
wn.tracer(0) # Turns off screen updates for smoother animation

# --- GLOBAL VARIABLES ---
score = 0
bullet_state = "ready" # "ready" or "fire"
alien_direction = 1 # 1 for right, -1 for left
last_alien_move_time = time.time() # To track when aliens last moved
game_started = False # Flag to control game state (welcome, active, game over)
game_paused = False # NEW: Flag to control pause state

# --- Player Ship ---
player = turtle.Turtle()
player_shape_coords = ((0, 15), (-15, -15), (15, -15))
wn.register_shape("player_ship", player_shape_coords)
player.shape("player_ship")
player.color("white")
player.penup()
player.speed(0)
player.setheading(90)
player.sety(-300)

# --- Player Movement Functions ---
player_speed = 15

def move_left():
    global game_paused # Access global flag
    if game_started and not game_paused: # Only move if game is active and not paused
        x = player.xcor()
        x -= player_speed
        if x < -280:
            x = -280
        player.setx(x)

def move_right():
    global game_paused # Access global flag
    if game_started and not game_paused: # Only move if game is active and not paused
        x = player.xcor()
        x += player_speed
        if x > 280:
            x = 280
        player.setx(x)

# --- Player Bullet ---
bullet = turtle.Turtle()
bullet.shape("circle")
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
bullet.hideturtle()

bullet_speed = 20

# --- Bullet Firing Function ---
def fire_bullet():
    global bullet_state, game_paused # Access global flags
    if bullet_state == "ready" and game_started and not game_paused: # Only fire if game is active and not paused
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

# --- Alien Invaders (creation logic moved to a function) ---
aliens = [] # Keep this global to store current aliens

def create_aliens():
    global aliens # Ensure we're modifying the global list
    # Clear any existing aliens first if this is a restart
    for alien in aliens:
        alien.hideturtle()
        # Optional: Dispose of the turtle object to free up memory more completely
        # For simple games, just hiding is often sufficient.
        # alien.clear()
        # alien.setheading(0)
    aliens.clear() # Empty the list

    alien_rows = 3
    aliens_per_row = 6
    alien_x_start = -200
    alien_y_start = 300
    alien_x_spacing = 80
    alien_y_spacing = 60

    # Ensure alien shape is registered before creation
    alien_shape_coords = ((-10, 0), (-10, 10), (0, 20), (10, 10), (10, 0), (0, -10))
    if "alien_ship" not in wn.getshapes(): # Check if shape exists to prevent re-registration warning
        wn.register_shape("alien_ship", alien_shape_coords)

    for row in range(alien_rows):
        for i in range(aliens_per_row):
            alien = turtle.Turtle()
            alien.shape("alien_ship")
            alien.color("red")
            alien.penup()
            alien.speed(0)

            x = alien_x_start + (i * alien_x_spacing)
            y = alien_y_start - (row * alien_y_spacing)
            alien.setx(x)
            alien.sety(y)
            aliens.append(alien)

# --- Alien Movement Variables ---
alien_speed_x = 15
alien_drop_y = 40
alien_move_delay = 0.5

# --- Barriers (Bunkers) (creation logic moved to a function) ---
barriers = [] # Keep this global to store current barriers

def create_barriers():
    global barriers # Ensure we're modifying the global list
    # Clear any existing barriers first if this is a restart
    for barrier_seg in barriers:
        barrier_seg.hideturtle()
    barriers.clear() # Empty the list

    barrier_configs = [
        {"x": -200, "y": -150},
        {"x": -80, "y": -150},
        {"x": 80, "y": -150},
        {"x": 200, "y": -150},
    ]

    barrier_segment_width = 20
    barrier_segment_height = 20
    barrier_rows = 3
    barrier_cols = 4

    for config in barrier_configs:
        base_x = config["x"]
        base_y = config["y"]
        for row in range(barrier_rows):
            for col in range(barrier_cols):
                barrier_segment = turtle.Turtle()
                barrier_segment.shape("square")
                barrier_segment.color("green")
                barrier_segment.penup()
                barrier_segment.speed(0)
                barrier_segment.shapesize(stretch_wid=1, stretch_len=1)

                x = base_x + (col * barrier_segment_width) - (barrier_segment_width * barrier_cols / 2) + (barrier_segment_width / 2)
                y = base_y + (row * barrier_segment_height) - (barrier_segment_height * barrier_rows / 2) + (barrier_segment_height / 2)

                barrier_segment.setposition(x, y)
                barriers.append(barrier_segment)


# --- Score and Game Messages ---
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.setposition(0, 340)

# Function to update the score display
def update_score_display():
    score_display.clear()
    score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

# HELPER FUNCTION TO MANAGE SCORE UPDATES
def increase_score(points):
    global score
    score += points
    update_score_display()

# --- Collision Detection Function ---
def is_collision(t1, t2):
    # Ensure both turtles are visible before checking collision
    if not t1.isvisible() or not t2.isvisible():
        return False
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 20:
        return True
    else:
        return False

# --- Game Over / Win Message Turtles ---
game_message_turtle = turtle.Turtle()
game_message_turtle.speed(0)
game_message_turtle.color("white")
game_message_turtle.penup()
game_message_turtle.hideturtle()
game_message_turtle.setposition(0, 0)

# --- NEW: Pause Message Turtle ---
pause_message_turtle = turtle.Turtle()
pause_message_turtle.speed(0)
pause_message_turtle.color("yellow")
pause_message_turtle.penup()
pause_message_turtle.hideturtle()
pause_message_turtle.setposition(0, 50) # Position slightly above center

# --- NEW: Function to toggle pause state ---
def toggle_pause():
    global game_paused, game_started
    # Only allow pausing if the game has started and isn't already over
    if game_started:
        game_paused = not game_paused
        if game_paused:
            pause_message_turtle.clear()
            pause_message_turtle.write("PAUSED", align="center", font=("Courier", 48, "bold"))
            wn.tracer(1) # Temporarily turn tracer on to show pause message immediately
            wn.update()
            wn.tracer(0) # Turn tracer off again
        else:
            pause_message_turtle.clear()
        wn.update() # Update screen to reflect pause/unpause immediately


# --- Function to reset the game state ---
def reset_game():
    global score, bullet_state, alien_direction, last_alien_move_time, game_started, game_paused

    # Clear any existing messages
    game_message_turtle.clear()
    welcome_message.clear()
    pause_message_turtle.clear() # Clear pause message if visible

    # Reset game state variables
    score = 0
    bullet_state = "ready"
    alien_direction = 1
    last_alien_move_time = time.time()
    game_started = False # Go back to the welcome screen state
    game_paused = False # Ensure game is not paused on reset

    # Reset player
    player.setposition(0, -300)
    player.showturtle()

    # Reset bullet
    bullet.hideturtle()
    bullet.setposition(0, -400)

    # Re-create aliens and barriers
    create_aliens()
    create_barriers()

    # Update score display to 0
    update_score_display()

    # Show the welcome message again
    welcome_message.setposition(0, 0)
    welcome_message.write("SPACE INVADERS", align="center", font=("Courier", 48, "normal"))
    welcome_message.sety(-50)
    welcome_message.write("Press ENTER to start", align="center", font=("Courier", 20, "normal"))
    wn.update()

    # Re-bind keyboard controls for starting the game
    wn.onkeypress(None, "space")
    wn.onkeypress(None, "Left")
    wn.onkeypress(None, "Right")
    wn.onkeypress(None, "p") # Unbind pause key
    wn.onkeypress(start_game, "Return")
    wn.onkeypress(None, "r")


# --- Function to start the game ---
def start_game():
    global game_started, game_paused
    if not game_started:
        welcome_message.clear() # Clear the welcome message
        game_message_turtle.clear() # Ensure any previous game over/win message is cleared
        pause_message_turtle.clear() # Ensure pause message is cleared

        # Re-enable controls
        wn.onkeypress(move_left, "Left")
        wn.onkeypress(move_right, "Right")
        wn.onkeypress(fire_bullet, "space")
        wn.onkeypress(toggle_pause, "p") # NEW: Bind pause key
        update_score_display() # Display initial score
        game_started = True # Set flag to true
        game_paused = False # Ensure game starts unpaused

        # Unbind keys that are no longer needed
        wn.onkeypress(None, "Return")
        wn.onkeypress(None, "r")


# --- Initial setup for aliens and barriers ---
create_aliens()
create_barriers()


# --- Welcome Message Display Logic ---
welcome_message = turtle.Turtle()
welcome_message.speed(0)
welcome_message.color("white")
welcome_message.penup()
welcome_message.hideturtle()
welcome_message.setposition(0, 0)
welcome_message.write("SPACE INVADERS", align="center", font=("Courier", 48, "normal"))
welcome_message.sety(-50)
welcome_message.write("Press ENTER to start", align="center", font=("Courier", 20, "normal"))
wn.update()

# --- Keyboard Bindings (Setup for Game Start) ---
wn.listen()
# Temporarily disable player controls at startup until game starts
wn.onkeypress(None, "space")
wn.onkeypress(None, "Left")
wn.onkeypress(None, "Right")
wn.onkeypress(None, "p") # Ensure pause key is unbound until game starts
# Bind a key to call the start_game function
wn.onkeypress(start_game, "Return")

# --- Main Game Loop ---
while True:
    if game_started and not game_paused: # NEW: Only run game logic if started AND not paused
        wn.update() # Update screen only when active

        # Alien Movement Logic
        current_time = time.time()
        if current_time - last_alien_move_time > alien_move_delay:
            for alien in aliens:
                x = alien.xcor()
                x += alien_speed_x * alien_direction
                alien.setx(x)

            alien_hit_wall = False
            for alien in aliens:
                if alien.isvisible() and (alien.xcor() > 280 or alien.xcor() < -280):
                    alien_hit_wall = True
                    break

            if alien_hit_wall:
                alien_direction *= -1
                for alien in aliens:
                    if alien.isvisible():
                        y = alien.ycor()
                        y -= alien_drop_y
                        alien.sety(y)
            last_alien_move_time = current_time

            # Game Over Condition (Alien reaches bottom or collides with player)
            for alien in aliens:
                if alien.isvisible() and (alien.ycor() < -280 or is_collision(player, alien)):
                    player.hideturtle() # Hide player
                    for a in aliens: # Hide all remaining aliens
                        a.hideturtle()
                    # Display Game Over message
                    game_message_turtle.clear()
                    game_message_turtle.setposition(0, 0)
                    game_message_turtle.write("GAME OVER", align="center", font=("Courier", 48, "normal"))
                    game_message_turtle.sety(-50)
                    game_message_turtle.write("Press R to Restart", align="center", font=("Courier", 20, "normal"))
                    wn.update()

                    # Disable game controls and enable restart
                    wn.onkeypress(None, "space")
                    wn.onkeypress(None, "Left")
                    wn.onkeypress(None, "Right")
                    wn.onkeypress(None, "p") # Unbind pause key
                    wn.onkeypress(reset_game, "r") # Bind 'R' to restart
                    game_started = False # Stop main loop from running game logic
                    game_paused = False # Ensure not paused on game over
                    break # Break from this alien loop, game has ended

        # Move the bullet
        if bullet_state == "fire":
            y = bullet.ycor()
            y += bullet_speed
            bullet.sety(y)

            if bullet.ycor() > 380:
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.setposition(0, -400)

        # Check for collision between bullet and alien
        if bullet_state == "fire":
            for alien in list(aliens): # Use list() to allow modification during iteration
                if is_collision(bullet, alien): # is_collision already checks visibility
                    bullet.hideturtle()
                    bullet_state = "ready"
                    bullet.setposition(0, -400)

                    alien.hideturtle()
                    aliens.remove(alien)

                    increase_score(10)
                    break # Only one bullet can hit one alien at a time

        # Check for collision between bullet and barrier
        if bullet_state == "fire":
            for barrier_seg in list(barriers): # Use list() to allow modification during iteration
                if is_collision(bullet, barrier_seg): # is_collision already checks visibility
                    bullet.hideturtle()
                    bullet_state = "ready"
                    bullet.setposition(0, -400)

                    barrier_seg.hideturtle()
                    barriers.remove(barrier_seg)
                    break # Only one bullet can hit one barrier segment at a time

        # Game Win Condition (Check if all aliens are gone)
        if not aliens:
            game_message_turtle.clear()
            game_message_turtle.setposition(0, 0)
            game_message_turtle.write("YOU WIN!", align="center", font=("Courier", 48, "normal"))
            game_message_turtle.sety(-50)
            game_message_turtle.write("Final Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
            game_message_turtle.sety(-100) # New line for restart message
            game_message_turtle.write("Press R to Restart", align="center", font=("Courier", 20, "normal"))
            wn.update()

            # Disable game controls and enable restart
            wn.onkeypress(None, "space")
            wn.onkeypress(None, "Left")
            wn.onkeypress(None, "Right")
            wn.onkeypress(None, "p") # Unbind pause key
            wn.onkeypress(reset_game, "r") # Bind 'R' to restart
            game_started = False # Stop main loop from running game logic
            game_paused = False # Ensure not paused on win
    else:
        # If game is not started, or game is paused, just update the screen
        # to show welcome/game over/win/paused messages.
        wn.update()
