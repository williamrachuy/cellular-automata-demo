"""Cellular automata simulation engine."""

from automata.rules import decode_rule, get_next_cell


def initialize_grid(width: int, height: int) -> list[list[int]]:
    """
    Create an empty grid with a single cell in the center of the first row.

    Args:
        width: Number of columns
        height: Number of rows

    Returns:
        2D grid with first row initialized, rest empty
    """
    grid = [[0] * width for _ in range(height)]
    # Place a single cell at the center of the first row
    grid[0][width // 2] = 1
    return grid


def evolve_next_row(
    grid: list[list[int]],
    current_row: int,
    rule_transitions: list[int],
    width: int,
) -> None:
    """
    Compute the next generation row based on the current row.

    Uses toroidal boundary conditions where edges wrap around.

    Args:
        grid: 2D grid to mutate
        current_row: Index of the current row (we compute current_row + 1)
        rule_transitions: Lookup table from rules.decode_rule()
        width: Number of columns (for wraparound)
    """
    next_row_idx = current_row + 1
    if next_row_idx >= len(grid):
        return

    current = grid[current_row]
    next_row = grid[next_row_idx]

    for x in range(width):
        # Use toroidal boundary conditions
        left_x = (x - 1) % width
        right_x = (x + 1) % width

        left_val = current[left_x]
        center_val = current[x]
        right_val = current[right_x]

        next_row[x] = get_next_cell(rule_transitions, left_val, center_val, right_val)


def reset_simulation(state) -> None:
    """
    Reinitialize the grid and apply the current rule.

    Args:
        state: State object to reset
    """
    state.grid = initialize_grid(state.width, state.height)
    state.rule_transitions = decode_rule(state.rule_number)
    state.current_row = 0
    state.step_requested = False
