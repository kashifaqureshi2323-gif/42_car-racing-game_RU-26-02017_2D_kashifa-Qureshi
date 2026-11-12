# Car Racing Game — PS No. 42

A 2D car racing / obstacle-avoidance game written in **Python 3** using **Pygame**. The player controls a blue car near the bottom of the road and moves left or right to avoid red obstacle cars that travel down the screen.

## 1. Project overview

| Item | Details |
|---|---|
| Project number | PS No. 42 |
| Project title | Car Racing Game |
| Language | Python 3 |
| Library | Pygame |
| Window size | 400 × 600 pixels |
| Target frame rate | 60 FPS |
| Player car | 40 × 80 pixels |
| Player starting position | `(180, 500)` |
| Road horizontal range | `x = 50` through `x = 350` |
| Player movement | 10 pixels per key press |
| Scoring | +1 for each obstacle that passes the screen |
| Collision response | Game Over screen with final score |
| Restart | Press `R` |

## 2. Features

- Opens a 400 × 600 game window.
- Draws a road with two boundaries and a moving dashed center line.
- Draws the player's blue car and red obstacle cars.
- Uses the left and right arrow keys to control the player.
- Keeps the player car inside the road.
- Creates obstacles at random valid horizontal positions.
- Moves obstacles downward continuously.
- Adds one point when an obstacle has passed completely beyond the bottom of the window.
- Detects collisions with `pygame.Rect.colliderect()`.
- Displays **GAME OVER** and the final score after a collision.
- Restarts the game when the player presses `R` after game over.

## 3. Project files

```text
car_racing_game_project/
├── car_racing_game.py   # Complete game implementation
├── README.md            # Project setup and usage documentation
├── SUMMARY.md           # Detailed implementation and test-case summary
└── requirements.txt      # Python dependency
```

## 4. Requirements

- Python 3.8 or later recommended.
- Pygame.
- A desktop environment capable of opening a graphical window.

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

Alternatively:

```bash
python -m pip install pygame
```

## 5. How to run

Open a terminal in the project directory and execute:

```bash
python car_racing_game.py
```

On some Windows installations, use:

```bash
py car_racing_game.py
```

A 400 × 600 game window should open.

## 6. Controls

| Key | Action |
|---|---|
| Left Arrow | Move the player's car 10 pixels left |
| Right Arrow | Move the player's car 10 pixels right |
| R | Restart after Game Over |
| Window close button | Exit the game |

The `R` key is intentionally used to restart only after the game has ended. During a running game, it has no effect.

## 7. Game rules and mechanics

### Player movement

The player starts at `(180, 500)`. The car is 40 pixels wide and 80 pixels high. Each left or right key press changes its horizontal coordinate by 10 pixels.

The legal horizontal range for the player's left edge is:

```text
50 <= player_x <= 310
```

The maximum value is 310 because the car is 40 pixels wide and the road's right edge is at x = 350. The movement code clamps the coordinate to this range, preventing the car from leaving the road.

### Obstacles

Obstacle cars are 40 × 80 pixels. Their initial horizontal position is selected randomly from the legal road range, and they move down the screen at a constant speed.

The spawn timer creates an obstacle approximately once per second. The timer uses a Pygame user event, so obstacle generation is handled by the normal event loop.

### Score

The score begins at zero. An obstacle awards one point when its top coordinate becomes greater than the window height (600), meaning it has completely passed below the visible screen. Each obstacle has a `passed` flag to ensure that it cannot award points more than once.

### Collision and game over

The game checks the player's rectangle against each obstacle rectangle:

```python
self.player.rect.colliderect(obstacle.rect)
```

If the rectangles overlap, the game enters the game-over state. The final score is displayed, and gameplay updates stop until the user presses `R`.

### Restart

Restarting calls the `reset()` method. It restores the player's starting position, clears all obstacles, sets the score to zero, and returns the game to the running state.

## 8. Program structure

The implementation uses three main classes:

- **`Car`** — stores a car's rectangle and color and draws its body, windows, and wheels.
- **`Obstacle`** — wraps an obstacle car, moves it downward, and tracks whether it has already been scored.
- **`CarRacingGame`** — manages the display, clock, game state, input, obstacle spawning, scoring, collision detection, and rendering.

The `main()` function creates the game object and starts the game loop.

## 9. Main game loop

The game runs at a target of 60 frames per second. Each loop iteration follows this order:

1. Process window, keyboard, and obstacle-spawn events.
2. Update obstacle positions.
3. Check whether obstacles have passed the screen and update the score.
4. Check for collisions.
5. Draw the road, cars, score, and any game-over overlay.
6. Limit the frame rate with `clock.tick(FPS)`.

This repeated sequence is the standard game-loop pattern.

## 10. Test cases from the assignment

| Test | Input / scenario | Expected result |
|---|---|---|
| 1 — Normal input | Player x = 180; press Right | Player x = 190; score remains 0; game continues |
| 2(a) — Left boundary | Player x = 50; press Left | Player remains at x = 50 |
| 2(b) — Right boundary | Player x = 310; press Right | Player remains at x = 310 |
| 3 — Invalid input | Player x = 180; press Space | No movement; game continues |
| 4(a) — Obstacle passed | Starting score = 3; obstacle passes below the screen | Score becomes 4 |
| 4(b) — Collision | Player at (180, 500); obstacle at (200, 520) | Collision detected; Game Over; final score shown |

### Notes about the test cases

- The assignment describes the obstacle at `(300, 600)` as having left the screen. The implementation awards the point when the obstacle's top edge is **greater than** 600. At exactly y = 600, an 80-pixel-tall obstacle is still partly outside / at the bottom boundary; it will be counted on a subsequent update after it moves farther down.
- The collision example overlaps: the player's rectangle spans x = 180–220 and y = 500–580, while the obstacle spans x = 200–240 and y = 520–600.
- Keyboard movement is event-based: one movement step is applied per key-down event, matching the assignment's 10-pixel-per-key-press requirement.

## 11. Concepts used

- **Pygame:** window creation, drawing, fonts, events, timers, and frame-rate control.
- **Game loop:** continuous event processing, state updates, and rendering.
- **Keyboard input:** `pygame.KEYDOWN`, `pygame.K_LEFT`, and `pygame.K_RIGHT`.
- **Random numbers:** `random.randint()` selects obstacle lanes / positions.
- **Rectangles:** `pygame.Rect` represents car boundaries and supports collision checks.
- **Collision detection:** `Rect.colliderect()` tests rectangle overlap.
- **State management:** `game_over` controls whether gameplay continues.
- **Lists:** multiple obstacles are stored and updated in a list.
- **Functions and classes:** code is separated into reusable responsibilities.

## 12. Customization

The main settings are grouped near the top of `car_racing_game.py`:

- `WINDOW_WIDTH`, `WINDOW_HEIGHT` — display dimensions.
- `FPS` — target frame rate.
- `ROAD_LEFT`, `ROAD_RIGHT` — road boundaries.
- `CAR_WIDTH`, `CAR_HEIGHT` — car dimensions.
- `PLAYER_SPEED` — movement step per key press.
- `OBSTACLE_SPEED` — downward obstacle speed.
- `OBSTACLE_SPAWN_MS` — time between obstacle spawn events.

Changing these values may require adjusting the starting positions and test expectations.

## 13. Troubleshooting

**`ModuleNotFoundError: No module named 'pygame'`**

Install Pygame in the same Python environment used to run the program:

```bash
python -m pip install pygame
```

**The game window opens and closes immediately**

Run the file from a terminal so any error message remains visible. Confirm that Pygame installed successfully.

**The game is slow**

Close other demanding applications and check that the computer can maintain the target 60 FPS. The target is a frame-rate limit, not a guarantee that every computer will achieve 60 FPS.

## 14. Submission checklist

- [ ] Python source file included.
- [ ] Pygame dependency documented.
- [ ] Game opens at 400 × 600.
- [ ] Player movement and road boundaries work.
- [ ] Obstacles spawn and move down.
- [ ] Score increments for passed obstacles.
- [ ] Collision triggers Game Over.
- [ ] Final score is displayed.
- [ ] `R` restarts the game.
- [ ] README and summary are included.
- [ ] Run and test the game on the submission computer before uploading to GitHub.

## 15. GitHub upload

From the project directory:

```bash
git init
git add car_racing_game.py README.md SUMMARY.md requirements.txt
git commit -m "Add Pygame car racing game"
```

Create an empty repository on GitHub, then connect it:

```bash
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your own repository.

---

**Project:** Car Racing Game  
**Project number:** PS No. 42  
**Implementation:** Python 3 + Pygame
