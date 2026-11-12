# Car Racing Game — Detailed Project Summary

## 1. Project identity

- **PS Number:** 42
- **Project title:** Car Racing Game
- **Programming language:** Python 3
- **Library:** Pygame
- **Application type:** 2D keyboard-controlled arcade game

## 2. Problem statement

The objective is to build a 2D car racing game in which the player controls a car on a road. The player can move left and right using the keyboard arrow keys. Other cars (obstacles) enter from the top of the screen and travel downwards. The player must avoid these obstacles.

A point is added to the score whenever an obstacle successfully passes the player and leaves the visible screen. If the player's car collides with an obstacle, the game ends. The game-over screen must show the final score and allow the player to restart using the `R` key.

## 3. Requirements translated into implementation

| Assignment requirement | Implementation |
|---|---|
| Python 3 and Pygame | The game imports and uses Pygame |
| 400 × 600 window | `WINDOW_WIDTH = 400`, `WINDOW_HEIGHT = 600` |
| 60 FPS | `clock.tick(FPS)` with `FPS = 60` |
| Road from x = 50 to x = 350 | Road rectangle and boundary lines use these coordinates |
| Player car at (180, 500) | `PLAYER_START_X = 180`, `PLAYER_Y = 500` |
| Car size 40 × 80 | `CAR_WIDTH = 40`, `CAR_HEIGHT = 80` |
| Move 10 px per key press | `PLAYER_SPEED = 10` |
| Stay inside road | Horizontal position is clamped between 50 and 310 |
| Random obstacle positions | `random.randint(ROAD_LEFT, ROAD_RIGHT - CAR_WIDTH)` |
| Obstacles move down | Obstacle y-coordinate increases each update |
| +1 for each passed obstacle | Score increments once when the obstacle passes the bottom |
| Collision detection | `pygame.Rect.colliderect()` |
| Game Over and final score | Game-over overlay renders the message and score |
| Restart using R | `reset()` is called on `pygame.K_r` after game over |

## 4. Screen coordinate explanation

Pygame uses a coordinate system whose origin `(0, 0)` is at the top-left of the window:

- x increases toward the right.
- y increases toward the bottom.
- A rectangle's `(x, y)` represents its top-left corner.

The road occupies x coordinates 50 through 350. Since the car is 40 pixels wide, the player's left edge must stay between 50 and 310:

```text
Minimum player x = 50
Maximum player x = 350 - 40 = 310
```

The player's rectangle at the starting position is:

```text
x = 180
y = 500
width = 40
height = 80
```

## 5. Program design

### `Car`

The `Car` class represents a vehicle. It stores a Pygame rectangle and a color. Its `draw()` method paints the car body, windows, and wheels.

### `Obstacle`

The `Obstacle` class represents a falling vehicle. It contains a `Car`, moves the car downward in `update()`, and stores a Boolean `passed` flag. This flag prevents duplicate score increments.

### `CarRacingGame`

This is the main controller. It initializes Pygame, creates the display and fonts, starts the obstacle timer, and maintains the game state.

Its main responsibilities are:

1. Resetting the game.
2. Spawning obstacles.
3. Handling keyboard and window events.
4. Updating obstacle positions and the score.
5. Detecting collisions.
6. Drawing the road, cars, score, and game-over overlay.
7. Running the main loop.

### `main()`

Creates the `CarRacingGame` object and calls `run()`.

## 6. Algorithm / execution flow

```text
START
  |
  v
Initialize Pygame and create the 400 x 600 window
  |
  v
Reset player, obstacles, score, and game state
  |
  v
MAIN GAME LOOP
  |
  +--> Read events
  |      |
  |      +--> Left arrow: move left by 10 px, not below x=50
  |      |
  |      +--> Right arrow: move right by 10 px, not above x=310
  |      |
  |      +--> Timer event: create an obstacle
  |      |
  |      +--> Quit event: exit
  |
  +--> If game is running:
  |      |
  |      +--> Move obstacles downward
  |      +--> If obstacle passes bottom: add 1 point once
  |      +--> If player overlaps obstacle: set Game Over
  |
  +--> Draw road, cars, score, and game-over overlay if needed
  |
  +--> Limit loop to 60 FPS
  |
  v
If Game Over and R is pressed:
  |
  +--> Reset player, obstacles, and score
  +--> Continue game loop
  |
  v
END when window is closed
```

## 7. Important logic

### Player movement and boundaries

A left-arrow press subtracts 10 from the player's x-coordinate, but `max()` prevents it from becoming smaller than 50. A right-arrow press adds 10, but `min()` prevents it from becoming greater than 310.

This ensures the complete 40-pixel-wide player car remains between the road boundaries.

### Obstacle generation

A Pygame timer emits a custom event approximately every 1000 milliseconds. When this event is received during active gameplay, an obstacle is created at a random legal x-coordinate.

### Scoring

Each obstacle has a `passed` flag. When its top coordinate is greater than the window height, the score increases by one and the flag becomes true. The obstacle is then removed from the active list.

### Collision detection

Both cars are represented by `pygame.Rect` objects. `colliderect()` returns true when their rectangular areas overlap. On collision, the `game_over` flag is set to true.

### Restart

When the game is over, the `R` key calls `reset()`. The player returns to `(180, 500)`, the obstacle list is cleared, the score becomes zero, and gameplay resumes.

## 8. Test case analysis

### Test Case 1 — Normal input

**Input:** Player x = 180; RIGHT arrow pressed.

**Expected:** Player x = 190, score = 0, game running.

**Reason:** The right-arrow handler adds the configured 10-pixel movement step. No obstacle collision is involved in this test.

### Test Case 2 — Boundary / minimum input

**(a) Input:** Player x = 50; LEFT arrow pressed.

**Expected:** Player x remains 50.

**Reason:** The `max()` boundary check prevents movement beyond the left road edge.

**(b) Input:** Player x = 310; RIGHT arrow pressed.

**Expected:** Player x remains 310.

**Reason:** The `min()` boundary check prevents the 40-pixel-wide car from crossing the road's right edge at x = 350.

### Test Case 3 — Invalid input

**Input:** Player x = 180; SPACE pressed.

**Expected:** Key ignored, player remains at x = 180, game running.

**Reason:** The input handler only contains movement logic for the left and right arrow keys. Space does not change the player position.

### Test Case 4 — Different valid scenario

**(a) Obstacle passed**

**Input:** Starting score = 3; an obstacle moves beyond the bottom of the screen.

**Expected:** Score becomes 4.

**Reason:** The obstacle's `passed` flag ensures one point is added for that obstacle.

**(b) Collision**

**Input:** Player at `(180, 500)` and obstacle at `(200, 520)`.

**Expected:** Collision detected, Game Over displayed, final score shown.

**Reason:** The rectangles overlap:

- Player rectangle: x 180–220, y 500–580.
- Obstacle rectangle: x 200–240, y 520–600.

Their intersection is non-empty, so `colliderect()` detects the collision.

## 9. Test case interpretation note

The assignment says that an obstacle at `(300, 600)` leaves the screen. With an obstacle height of 80 pixels, its top-left y-coordinate being exactly 600 means the obstacle begins at the bottom edge and is not yet completely beyond the visible screen. This implementation awards the point once the obstacle's top y-coordinate is **greater than 600**. The obstacle will pass this threshold on a subsequent update.

If an instructor expects scoring at `y >= 600` instead, the scoring condition can be changed in `CarRacingGame.update()` from:

```python
obstacle.rect.top > WINDOW_HEIGHT
```

to:

```python
obstacle.rect.top >= WINDOW_HEIGHT
```

The current implementation uses the stricter interpretation of “completely passed below the screen.”

## 10. Programming concepts demonstrated

1. **Object-oriented programming:** `Car`, `Obstacle`, and `CarRacingGame` organize related data and behavior.
2. **Game loop:** Events, updates, and rendering repeat continuously.
3. **Event handling:** Pygame keyboard, timer, and quit events are processed.
4. **Conditional statements:** Movement, boundaries, scoring, and collision behavior depend on conditions.
5. **Loops:** The main loop runs the game; loops also draw and update obstacle collections.
6. **Lists:** The obstacle list stores multiple active obstacles.
7. **Randomization:** Random x positions make obstacle placement less predictable.
8. **Collision detection:** Rectangle overlap is checked with `colliderect()`.
9. **State management:** A Boolean game-over state controls gameplay and restart behavior.
10. **Time and frame-rate management:** A Pygame timer spawns obstacles and a clock limits the frame rate.

## 11. Limitations and possible improvements

This implementation intentionally focuses on the assignment's minimum requirements. Possible future improvements include:

- Increasing obstacle speed gradually as the score rises.
- Adding sound effects and background music.
- Adding a start screen and pause function.
- Adding multiple obstacle colors or car designs.
- Adding a high-score system.
- Adding touch or mouse controls.
- Adding automated unit tests for movement, boundaries, scoring, and collision logic.

## 12. Conclusion

The Car Racing Game demonstrates a complete beginner-friendly Pygame application. It implements player movement, road boundaries, obstacle generation, downward movement, scoring, collision detection, a game-over state, and restart functionality. The code is organized into classes and uses a standard event-update-render game loop.

The source code and README provide the runnable project and setup instructions. This summary explains how the implementation maps to the assignment requirements and how each supplied test case is expected to behave.
