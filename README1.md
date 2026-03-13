# 2048 — AI Board Game Project

This repository is for the course assignment: implement **the 2048 game** (single-player) plus an **AI player** based on **search algorithms from the course**, benchmark it, and write a short report.

---

## 1) Read the assignment carefully

First understand the full workflow. You must:

- Choose a board game → **2048 (single-player)**
- Implement the **game engine**
- Implement an **AI player** using course **search algorithms**
- **Benchmark** the AI
- Write a **4–6 page report**

---

## 2) Understand the required deliverables

You must hand in:

- A **PDF report**
- A **PDF group declaration** stating who did what (ideas, implementation, report)
- A **ZIP** containing the source code, including a **README** for how to install and run

So already at the start, your group can prepare:

- a project folder structure
- a README skeleton
- a report outline
- a work distribution document

**Important constraint:**
The **AI must be clearly separated from the game engine**.

---

## 3) Prepare for choosing the game (analysis checklist)

Consider:

- complexity of rules
- ease of implementation
- size of state space
- perfect or imperfect information
- observability or partial observability
- deterministic or stochastic
- suitable AI methods
- expected difficulty

Also reflect on:

1. What kind of reasoning are you as a human using when thinking about the next move to make?
2. Which algorithms from the course could possibly be used to create a computer opponent (an AI) for the game?
3. Can any of the human reasoning and intuition used to play the game be implemented in the AI algorithm?
4. How would you represent game states on the computer?

**Game simplification option:**
If necessary to ensure a functional AI, the game can be simplified by reducing the board size, limiting the number of pieces, or omitting certain rules while preserving the core mechanics.

---

## 4) Make a README skeleton early

Prepare the README early, for example with:

- project title
- game overview / short project description
- how to run the code
- folder structure

---

## 5) Choose the game and its rules (report-focused, for 2048)
**2048 (game rule)**

2048 is a single-player sliding tile puzzle video game written by Italian web developer Gabriele Cirulli and published on GitHub.[2] The objective of the game is to slide numbered tiles on a grid to combine them to create a tile with the number 2048; however, one can continue to play the game after reaching the goal, creating tiles with larger numbers.
2048 was intended to be an improved version of two other games, both of which were clones of the iOS game Threes released a month earlier. Cirulli himself described 2048 as being "conceptually similar" to Threes.[3] The release of 2048 resulted in the rapid appearance of many similar games, akin to the flood of Flappy Bird variations from 2013. The game received generally positive reviews from critics, with it being described as "viral" and "addictive".

**Gameplay (rules)**

2048 is played on a plain 4×4 grid, with numbered tiles that slide when a player moves them using the four arrow keys.[4] The game begins with two tiles already in the grid, having a value of either 2 or 4, and another such tile appears in a random empty space after each turn.[5] Tiles with a value of 2 appear 90% of the time, and tiles with a value of 4 appear 10% of the time.[6] Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.[7][8] The resulting tile cannot merge with another tile again in the same move. Higher-scoring tiles emit a soft glow;[5] the largest possible tile is 131,072.[9]

If a move causes three consecutive tiles of the same value to slide together, only the two tiles farthest along the direction of motion will combine. If all four spaces in a row or column are filled with tiles of the same value, a move parallel to that row/column will combine the first two and last two.[10] A scoreboard on the upper-right keeps track of the user's score. The user's score starts at zero, and is increased whenever two tiles combine, by the value of the new tile.[5]

The game is won when a tile with a value of 2048 appears on the board. Players can continue beyond that to reach higher scores.[11][12][13] When the player has no legal moves (there are no empty spaces and no adjacent tiles with the same value), the game ends.[3][14]

**Strategy**

Strategies in 2048 include keeping the largest tile in a specific corner with other large tiles filling the row (either vertically or horizontally). If the row remains filled, the player can then move in three different directions while still keeping the largest tile in the preferred corner. As a general rule, no small tiles should be separated from other small tiles by a large tile.[15][16]

Example drawing (largest tile locked in the top-left corner):

```
Preferred corner: top-left

+------+------+------+------+
| 1024 |  512 |  256 |  128 |
+------+------+------+------+
|   64 |   32 |   16 |    8 |
+------+------+------+------+
|    4 |    2 |    2 |    . |
+------+------+------+------+
|    . |    . |    . |    . |
+------+------+------+------+

Good move directions while preserving the corner setup:
LEFT  <-   UP  ^   DOWN  v

Avoid RIGHT -> because it can pull large tiles away from the corner.
```


**Game Type Classification (2048)**

- Single-player
- Non-competitive and non-cooperative (no opponent team dynamics)
- Non-zero-sum (there is no opposing utility to minimize)
- Turn-based (one action per step: up/down/left/right)
- Perfect information and fully observable (entire board is visible)
- Not deterministic overall
- Stochastic

**Clarification on determinism**

- The move and merge mechanics themselves are deterministic.
- However, after each valid move, a new tile appears randomly:
  - Value: 2 (90%) or 4 (10%)
  - Position: random empty cell
- Because of this random spawn step, the overall game is stochastic, not deterministic.

**What this implies for AI methods**

- Classical adversarial search like minimax is not the right fit, because there is no opponent.
- Expectimax is a strong fit, because it models:
  - Max nodes for player actions
  - Chance nodes for random tile spawns
- MCTS is also a strong fit, especially when deeper lookahead is expensive; it handles stochastic transitions through sampling.
- Dynamic programming style MDP methods are theoretically relevant, but exact solutions are impractical due to huge state space.
- In practice, the strongest assignment-friendly approaches are:
  - Expectimax plus heuristic evaluation
  - MCTS plus rollout policy and heuristic guidance

**One-line summary**

2048 is a single-agent, fully observable, turn-based stochastic decision problem, which points to expectimax, MCTS, and heuristic search rather than adversarial game-tree methods.

### Game Rules

**Board**
- 4×4 grid

**Initial State**
- Two tiles (2 or 4)

**Actions**
- {Up, Down, Left, Right}

**Transition**
- Deterministic slide + merge
- Tiles slide as far as possible in the chosen direction until blocked by edge or another tile
- Random tile spawn:
  - 2 with probability 0.9
  - 4 with probability 0.1
  - Random empty cell
- New tile is spawned only when a move actually changes the board (valid move)

**Merge Rule**
- Same-value tiles merge **once per move**
- Score increases by merged value
- Three consecutive same tiles: the two farthest along the movement direction merge first
  - Example (LEFT): `[2, 2, 2, 0] -> [4, 2, 0, 0]`
- Four same tiles in a row merge as pairs
  - Example (LEFT): `[2, 2, 2, 2] -> [4, 4, 0, 0]`

**Terminal Condition**
- No legal moves available

**Objective**
- Reach 2048 tile (player can continue afterward)

**UI Rules (Current Implementation)**
- Score is displayed on screen
- Move counter is displayed on screen

---


## 7) Review course algorithms first (implementation-focused, for 2048)

### Search problem foundations

- State-space modeling
- Transition model
- Goal-test vs terminal states
- Formal problem formulation

Using Lecture 5 formalization:

- **s₀ (initial state):** initial 4×4 board with two random tiles
- **Players:** single player
- **Actions(s):** {Up, Down, Left, Right} where legal
- **Result(s, a):** two-stage transition:
  1) deterministic slide/merge
  2) probabilistic tile spawn
  Formally: stochastic transition distribution `P(s' | s, a)` (equivalently, a set of possible `s'` with probabilities)
  This matches stochastic modeling from Lecture 4 (slides04)
- **Terminal-Test(s):** True if:
  - no empty cells, and
  - no adjacent equal tiles
- **Utility(s):**
  - for terminal states: final score
  - for non-terminal (search evaluation): heuristic value

At this stage, the goal is not to choose the final method yet, but to understand:

- which methods fit single-player games
- which methods become harder with partial observability or multiple players

---

## 7.1) Game Type and Properties

| Property | Value |
|---|---|
| Players | 1 |
| Turn-based | Yes |
| Perfect information | Yes |
| Deterministic | No |
| Stochastic | Yes |
| Adversarial | No |
| Zero-sum | No |

**Important implication:**
Because the environment introduces randomness, we must model **chance nodes**.

---

## 7.2) Suitable AI Methods (from lectures)

❌ **Minimax**
Not suitable: no adversary.

✔ **Expectimax**
Appropriate for stochastic environments. Models:
- Player nodes (max)
- Chance nodes (expected value)

✔ **Monte-Carlo Tree Search (MCTS)**
Lecture 6 explicitly discusses 2048 in MCTS context. MCTS characteristics:
- sample-based
- random playout evaluation
- UCB selection
- works well when evaluation is hard to design

For 2048: **MCTS is highly appropriate.**

---

## 7.3) Human Reasoning vs AI

Human strategies:
- Keep largest tile in a corner
- Maintain monotonic ordering
- Avoid breaking structure
- Prefer smooth gradients

AI implementation:
These can become heuristic features:
- monotonicity score
- smoothness penalty
- empty tile count
- max tile weight

---

## 7.4) State-Space Size (required by assignment)

Rough estimation:

- 16 board cells
- each cell can hold values: 0, 2, 4, 8, … up to large powers of 2

Upper bound rough idea:
- if each cell could take k values: state space ≈ k¹⁶

Even conservative estimate gives:
- between 10¹³ – 10²⁰+

Conclusion:
- full search to terminal depth is impossible
- this justifies heuristic search or sampling

---

## 8) Project Scope Decision

Keep scope realistic:

- standard 4×4 board
- simple GUI
- one or more AI method
- one baseline
- benchmark comparison such as random, greedy, or human comparison

Avoid:

- neural networks
- reinforcement learning training
- overcomplicated UI

---

## 9) Design a project structure for 2048

Before focusing on the chosen game, define the main components:

- Game State
- Move / Action
- Game Engine
- GUI
- Rules / Transition Function
- AI Player
- Evaluation / Heuristic
- Benchmark Module
- Configuration / Parameters

For 2048, the engine and AI should be clearly separated:

- the game engine handles board updates, rules, score, and random tile spawning
- the AI player only queries the state and selects an action

---

## 10) Implement the game engine first

Do not start with the AI. First implement:

- board representation
- legal moves
- move execution
- merge logic
- score updates
- random tile spawning
- reset / start state
- terminal detection
- win detection (2048 reached, if included separately)

This is the core of the system.
The game engine must work correctly before any AI is added.

---

## 11) Make the game playable by a human

First milestone:
A human can play 2048 correctly on the computer.

This proves that:

- the game rules are implemented correctly
- the GUI and input handling work
- the engine can run independently of the AI

A simple playable version is enough; the assignment does not require a fancy GUI.

---

## 12) Define the interface between engine and AI

Before implementing AI, define the API the AI will use, for example:

- get current state
- get legal actions
- apply action
- simulate action on clone state
- clone state
- test terminal state
- get score
- get highest tile

It is better if the AI does not directly modify the live game object.
Instead, it should work on copied / simulated states during search.

---

## 13) Prepare benchmark infrastructure early

Before the AI is fully ready, build a benchmark runner that can record:

- final score
- highest tile
- number of moves
- runtime per move
- total runtime per game
- average result over many runs N

This makes it easier later to compare:

- baseline player vs AI
- different search depths
- different heuristics or evaluation functions
- different rollout counts or parameter settings

---

## 14) Implement a simple baseline player

Before the main AI, implement a basic comparison player, such as:

- random player
- simple greedy player

A baseline is important, because otherwise it is difficult to show whether the main AI is actually good.

For 2048, a greedy player could choose the move with:

- highest immediate score gain, or
- highest number of empty cells after the move

---

## 15) Implement the AI player

Now implement the real search-based AI. This should come after:

- the game engine works
- the human-playable version works
- the engine–AI interface is clean
- the benchmark setup exists
- the baseline player exists

For 2048, the main AI should model:

- player decision nodes
- stochastic tile-spawn outcomes

So the implementation should fit a method such as:

- Expectimax, or
- Monte-Carlo Tree Search (MCTS)

---

## 17) Implementation plan

### 17.0 Decide the technical setup

Before coding, decide:

- programming language: Python
- how to run the project
- simple GUI
- testing strategy

### 17.1 Create the repository and folder structure

Example structure:

```text
project_root/
│
├── src/
│   │
│   ├── game/
│   │   └── game.py
│   ├── ai/
│   │   ├── expectimax.py
│   │   ├── mcts.py
│   │   └── heuristics.py
│   ├── benchmark/
│   │   └── runner.py
│   │
│   └── utils/
│       └── config.py
├── main.py
├── tests/
│   └── test_game.py
├── README.md
└── report/
```

Responsibilities:

- `game/game.py` → full 2048 engine (board, moves, merge, spawn, terminal)
- `ai/` → completely separate AI logic
- `benchmark/` → automated experiments
- `tests/` → unit tests for merge and move correctness
- `main.py` → entry point (human mode / AI mode / benchmark mode)

---

### 17.2 Game engine (src/game/game.py) — task cards

**Card: Implement board initialization**
- Create empty 4×4 board
- Add two initial tiles
- Reset/start game function

**Card: Implement random tile spawning**
- Find empty cells
- Spawn 2 with probability 0.9
- Spawn 4 with probability 0.1

**Card: Implement move-left logic**
- Slide tiles
- Merge equal tiles once
- Return updated row/board

**Card: Implement move-right logic**
- Reverse row
- Reuse left logic
- Reverse back

**Card: Implement move-up logic**
- Transpose board
- Reuse left logic
- Transpose back

**Card: Implement move-down logic**
- Transpose board
- Reuse right logic
- Transpose back

**Card: Implement score tracking**
- Add merged tile value to score
- Store current score in game state

**Card: Prevent invalid spawn after unchanged move**
- Check whether board changed
- Spawn new tile only after valid move

**Card: Implement win detection**
- Detect tile 2048

**Card: Implement terminal detection**
- Detect no empty cells
- Detect no adjacent equal tiles

**Card: Implement legal actions function**
- Return valid moves from current state

**Card: Implement clone/simulation support**
- Deep copy game state
- Make AI simulation safe

**Card: Implement clean game API**
- `get_state()`
- `get_legal_actions()`
- `apply_action()`
- `clone()`
- `is_terminal()`
- `get_score()`
- `get_highest_tile()`

---

### 17.3 GUI + main loop (main.py) — task cards

**Card: Create pygame window**
- Set screen size
- Set title
- Initialize clock

**Card: Draw board and tiles**
- Draw background
- Draw empty cells
- Draw numbered tiles

**Card: Add keyboard input for human play**
- Arrow keys
- Apply move through engine API

**Card: Show game result**
- Show “You won”
- Show “Game over”

**Card: Add mode selection in main**
- Human mode
- AI mode
- Benchmark mode

---

### 17.4 Heuristics (src/ai/heuristics.py) — task cards

**Card: Implement empty-cells heuristic**
- Reward states with more empty cells

**Card: Implement max-tile heuristic**
- Reward larger max tile

**Card: Combine heuristics into evaluation function**
- Weighted sum of features
- Make weights adjustable

---

### 17.5 Expectimax (src/ai/expectimax.py) — task cards

**Card: Implement Expectimax player nodes**
- Max over legal actions

**Card: Implement chance nodes**
- Enumerate empty-cell spawn outcomes
- Include probabilities for 2 and 4

**Card: Add depth cutoff**
- Stop search at chosen depth
- Use heuristic evaluation

**Card: Add best-action selection**
- Return chosen move from root

**Card: Optimize Expectimax**
- Reduce repeated state computation
- Improve runtime if needed

---

### 17.6 MCTS (src/ai/mcts.py) — task cards

**Card: Define MCTS node structure**
- State
- Parent
- Children
- Visits
- Reward

**Card: Implement selection step**
- UCB-based child selection

**Card: Implement expansion step**
- Add unexplored child

**Card: Implement simulation step**
- Run rollout from child state

**Card: Implement backup step**
- Backpropagate reward

**Card: Implement MCTS action selection**
- Return best move after iteration budget

**Card: Add configurable MCTS parameters**
- Number of iterations
- Exploration constant
- Rollout policy

---

### 17.7 Benchmarking (src/benchmark/runner.py) — task cards

**Card: Create benchmark runner**
- Run many games automatically

**Card: Record benchmark metrics**
- Final score
- Highest tile
- Number of moves
- Runtime per move
- Total runtime

**Card: Benchmark random baseline**
- Run N games
- Save averages

**Card: Benchmark greedy baseline**
- Run N games
- Save averages

**Card: Benchmark Expectimax**
- Compare different depths
- Save averages

**Card: Benchmark MCTS**
- Compare different iteration counts
- Save averages

**Card: Compare methods**
- Random vs greedy vs Expectimax vs MCTS
- Prepare results for report

---

### 17.8 Tests (tests/test_game.py) — task cards

**Card: Test board initialization**
- 4×4 board
- Two starting tiles

**Card: Test tile spawn logic**
- Spawn only on empty cells
- Value is 2 or 4

**Card: Test merge rules**
- Equal tiles merge once
- Triple-tile case works correctly
- Four equal tiles merge pairwise

**Card: Test each move direction**
- Left
- Right
- Up
- Down

**Card: Test unchanged move behavior**
- No new tile if move has no effect

**Card: Test terminal detection**
- Correctly detect game over

**Card: Test win detection**
- Correctly detect 2048 tile

**Card: Test clone correctness**
- AI simulation does not modify live state

---

## 18) Report skeleton (4–6 pages)

Create the report structure early, even before everything is implemented. The report should be concise and focus on:

- Introduction
- Game Rules
- Game Type and Properties
- The size of the state space
- Formal Game Model (elements of the game)
- State and Move Representation in the computer
- Chosen methods and algorithms
- Heuristics / Evaluation Function
- Experiments and Benchmarks
- Future Work
