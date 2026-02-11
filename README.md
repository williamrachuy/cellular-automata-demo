# Cellular Automata Demo

An interactive terminal-based visualization of 1D elementary cellular automata.

## Features

- **Interactive Menu**: Configure rules, step timing, and simulation modes
- **Rule Selection**: Support for all 256 elementary CA rules (Rule 0-255)
- **Two Simulation Modes**:
  - **Auto Mode**: Automatic evolution with configurable timing
  - **Step Mode**: Manual step-by-step evolution, one generation per Space press
- **Rule Visualization**: Top panel shows visual representation of the current rule
- **Terminal-Based**: Pure ASCII graphics, works in any terminal

## Usage

```bash
python -m automata
```

### Controls

**Startup**:
- Press **Enter** to start in Auto Mode (automatic evolution)
- Press **Space** to start in Step Mode (manual stepping)

**During Simulation**:
- **ESC**: Open menu
- **Space** (in Step Mode): Advance one generation

**Menu Navigation**:
- **Up/Down Arrows**: Navigate menu items
- **Enter**: Select menu item or confirm input
- **ESC**: Close menu or cancel input
- **0-9, Backspace**: Enter numbers for rule and delay

## Interesting Rules to Try

- **Rule 30**: Chaotic expansion pattern
- **Rule 110**: Complex behavior (Turing complete)
- **Rule 90**: Sierpinski triangle pattern
- **Rule 184**: Traffic flow model

## Technical Details

- **No External Dependencies**: Uses only Python standard library
- **Curses-Based**: Works on Linux, macOS, and Unix
- **Toroidal Boundaries**: Edges wrap around for seamless patterns
- **Display Size**: 80 columns × 160 rows

## Architecture

```
automata/
├── main.py           # Main event loop
├── state.py          # Application state
├── rules.py          # Rule encoding/decoding
├── simulation.py     # CA evolution engine
└── ui/
    ├── renderer.py   # Display rendering
    ├── input.py      # Input handling
    └── menu.py       # Menu system
```

## How Elementary CA Rules Work

Each rule number (0-255) encodes how a cell evolves based on its 3-cell neighborhood:

```
Rule 30 (binary: 00011110)
┌─────────────┬─────────┐
│ Neighborhood│ Next    │
├─────────────┼─────────┤
│ 111 → 0     │ Dead    │
│ 110 → 0     │ Dead    │
│ 101 → 0     │ Dead    │
│ 100 → 1     │ Alive   │
│ 011 → 1     │ Alive   │
│ 010 → 1     │ Alive   │
│ 001 → 1     │ Alive   │
│ 000 → 0     │ Dead    │
└─────────────┴─────────┘
```

The rule number's binary representation directly encodes these transitions.