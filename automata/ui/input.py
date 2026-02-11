"""Input handling for the cellular automata application."""

import curses


def configure_input(stdscr) -> None:
    """
    Configure terminal input settings.

    Args:
        stdscr: curses window object
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.keypad(True)  # Enable special keys


def read_key(stdscr) -> int | None:
    """
    Read a key from input in non-blocking mode.

    Args:
        stdscr: curses window object

    Returns:
        Key code (int) if a key was pressed, None otherwise
    """
    try:
        key = stdscr.getch()
        return key if key != -1 else None
    except curses.error:
        return None


def handle_input(state, key: int) -> None:
    """
    Route input to appropriate handler based on current state.

    Args:
        state: State object
        key: Key code from curses
    """
    from automata.ui.menu import handle_menu_input, open_menu

    if state.menu_open:
        handle_menu_input(state, key)
    else:
        # Handle keys during simulation
        if key == 27:  # ESC
            open_menu(state)
        elif state.simulation_mode == "none":
            # Waiting for user to choose mode
            if key == 13 or key == 10:  # Enter key
                state.simulation_mode = "auto"
            elif key == ord(" "):  # Space key
                state.simulation_mode = "step"
        elif state.simulation_mode == "step":
            if key == ord(" "):  # Space key for step
                state.step_requested = True
