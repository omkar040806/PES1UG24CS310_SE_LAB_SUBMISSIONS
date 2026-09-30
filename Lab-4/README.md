# Balloon Pop (Lab 4: Vibe Coding)

A Pygame Balloon Pop game. Balloons fall from the top of the screen and the
player pops them with the mouse. This version fixes the original click-detection
bug and adds balloon types, a lives system, and a timed round.

## Requirements

- Python 3.10+
- Pygame

## Setup and Run

```bash
cd balloon-pop
pip install -r requirements.txt
python main.py
```

**Controls:** Left-click a balloon to pop it. Press **R** (or click the Restart
button) on the Game Over screen to start a new round.

## What Was Fixed

### Task 1: Click-detection bug
`check_pop` in `game/click_detection.py` compared the *squared* distance from the
click to the balloon center against the plain radius. Clicks only registered
near the exact center. It now compares distance to the actual radius (or squared
distance to `radius**2`), so a click anywhere inside the visible circle pops the
balloon.

## Features Added

### Task 2: Balloon types

| Type    | Color         | Effect             |
|---------|---------------|--------------------|
| Normal  | [e.g. Red]    | [+10] points       |
| Bonus   | [e.g. Gold]   | [+30] points       |
| Penalty | Black         | [-20] points       |

The score never drops below 0.

### Task 3: Lives system
- The player starts with **3 lives**, shown on screen.
- Any balloon that reaches the bottom without being popped costs **1 life**.
  This applies to **all** balloon types, including penalty balloons.
- Popping a balloon never costs a life, whatever its type.
- The game ends when lives reach 0.

### Task 4: Timed round
- Each round lasts **30 seconds**, with the remaining time shown on screen.
- The round ends when the timer hits 0 **or** lives hit 0, whichever comes first.
- When the round ends, balloon spawning and clicks stop and the **final score**
  is displayed.
- Pressing **R** (or clicking Restart) starts a new round with the score, lives,
  timer and balloons all reset.

## Design Note

Penalty (black) balloons cost a life if they fall off the bottom, just like any
other balloon, as the lab spec states. Popping them costs points but never a
life. So the player must pop every balloon to keep their lives, but pop penalty
balloons at the cost of score.

## Folder Structure

```
balloon-pop/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── balloon.py
│   ├── click_detection.py
│   └── renderer.py
└── README.md
```

## Submission Contents (Lab-4 folder)

- Before video: gameplay showing the click-detection bug
- After video: gameplay showing the fix and all new features
- Updated code
- Chat history (link and PDF/doc export)

## Tools Used

- ChatGPT, for debugging and feature development through iterative prompting
