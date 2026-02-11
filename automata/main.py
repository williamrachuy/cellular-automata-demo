"""Main application loop for cellular automata demo."""

import curses
import time

from automata.state import State
from automata.simulation import reset_simulation
from automata.ui.renderer import render
from automata.ui.input import configure_input, read_key, handle_input
from automata.simulation import evolve_next_row


def _run(stdscr) -> int:
    """
    Main application loop.

    Args:
        stdscr: curses window object

    Returns:
        Exit code (0 for success)
    """
    configure_input(stdscr)

    # Initialize state
    state = State(
        rule_number=30,
        step_delay=0.1,
        width=80,
        height=160,
        simulation_mode="none",
        menu_open=False,
    )
    reset_simulation(state)

    last_step_time = time.monotonic()

    while state.running:
        now = time.monotonic()

        # Evolution step logic
        if state.simulation_mode == "auto":
            if now - last_step_time >= state.step_delay:
                if state.current_row < state.height - 1:
                    evolve_next_row(
                        state.grid, state.current_row, state.rule_transitions, state.width
                    )
                    state.current_row += 1
                last_step_time = now
        elif state.simulation_mode == "step":
            if state.step_requested:
                if state.current_row < state.height - 1:
                    evolve_next_row(
                        state.grid, state.current_row, state.rule_transitions, state.width
                    )
                    state.current_row += 1
                state.step_requested = False

        # Input handling
        key = read_key(stdscr)
        if key is not None:
            handle_input(state, key)

        # Rendering
        render(stdscr, state)

        # Small sleep to prevent CPU spinning
        time.sleep(0.01)

    return 0


def main() -> int:
    """
    Entry point for the application.

    Returns:
        Exit code
    """
    try:
        return curses.wrapper(_run)
    except KeyboardInterrupt:
        return 0
