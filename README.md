# Vacuum Cleaner Agent, Route Planning in a Grid World

A Python AI agent that **plans** and **verifies** cleaning routes for a vacuum robot navigating a walled grid (a "cave"), using depth-first search with backtracking. Built as a university AI assignment on state-space search and agent design.

## Overview

The robot lives in a 2D grid made of free cells, walls (`X`), and an optional start cell (`S`). Movement is in four directions (N/E/S/W) and **wraps around the grid edges** (toroidal world). The agent solves two tasks:

- **FIND PLAN** : compute a sequence of moves that visits and cleans every reachable free cell.
- **CHECK PLAN** : given a candidate plan, decide whether it cleans every free cell, returning `GOOD PLAN` or `BAD PLAN` together with the coordinates of any cells it missed.

It handles both a **known** start position and an **unknown** one — in the unknown case it reasons across every possible starting cell rather than assuming one.

## What it demonstrates

- Uninformed state-space search (DFS with backtracking)
- Environment modeling and simulation : walls, four-way movement, edge wrap-around
- Reasoning under uncertainty : verifying a plan when the start position isn't given
- Clean separation of concerns : parsing, simulation, verification, plan generation, and output are independent functions
- File-based batch processing over a set of problem instances

## How it works

1. Parse each problem file into a grid and locate the start cell if present.
2. **FIND PLAN** runs DFS from a cell, recursing into unvisited, non-wall neighbours and appending the opposite move to backtrack, producing one continuous cleaning walk that covers the reachable area.
3. **CHECK PLAN** simulates the given move sequence, records cleaned cells, and compares against all free cells. With an unknown start, it simulates from every possible start and aggregates the cells that could be missed.

## Repository contents

| File | What it is |
|---|---|
| `FinalCode.py` | The agent (input parsing, search, simulation, output) |
| `problems.zip` | Sample problem instances |
| `solutions.zip` | Expected outputs for those instances |
| `Description.pdf`, `assignment-1.0.A.docx` | Original assignment brief |

## Run it

```bash
# Python 3, no external dependencies
unzip problems.zip        # creates ./problems with .txt instances
mkdir -p solutions
python FinalCode.py       # reads ./problems, writes results into ./solutions
```

## Possible extensions

Swap DFS for BFS or A* to produce shorter cleaning plans, add a few unit tests around `check_plan`, and commit the `problems/` and `solutions/` folders directly instead of as zips so the script runs without a manual unzip.

---

*Suggested GitHub "About" description:* **Python AI agent that plans and verifies vacuum-cleaning routes in a grid world using DFS with backtracking.**
*Suggested topics:* `python` · `artificial-intelligence` · `search-algorithms` · `dfs` · `pathfinding` · `agent`
