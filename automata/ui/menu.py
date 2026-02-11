"""Menu system for the cellular automata application."""

from automata.simulation import reset_simulation


MENU_ITEMS = [
    "Set Rule Number",
    "Set Step Delay",
    "Toggle Mode",
    "Reset Simulation",
    "Resume",
    "Quit",
]


def open_menu(state) -> None:
    """
    Open the menu and pause simulation.

    Args:
        state: State object
    """
    state.menu_open = True
    state.menu_mode = "main"
    state.menu_selection = 0
    state.menu_input = ""


def handle_menu_input(state, key: int) -> None:
    """
    Process input while menu is open.

    Args:
        state: State object
        key: Key code from curses
    """
    if state.menu_mode == "main":
        handle_main_menu(state, key)
    elif state.menu_mode == "rule_input":
        handle_text_input(state, key, "rule_input")
    elif state.menu_mode == "delay_input":
        handle_text_input(state, key, "delay_input")


def handle_main_menu(state, key: int) -> None:
    """
    Handle input in main menu mode.

    Args:
        state: State object
        key: Key code
    """
    if key == curses.KEY_UP or key == ord("k"):
        state.menu_selection = (state.menu_selection - 1) % len(MENU_ITEMS)
    elif key == curses.KEY_DOWN or key == ord("j"):
        state.menu_selection = (state.menu_selection + 1) % len(MENU_ITEMS)
    elif key == 13 or key == 10:  # Enter
        apply_menu_selection(state)
    elif key == 27:  # ESC to close menu
        state.menu_open = False


def handle_text_input(state, key: int, input_mode: str) -> None:
    """
    Handle text input for rule number or delay.

    Args:
        state: State object
        key: Key code
        input_mode: "rule_input" or "delay_input"
    """
    if key == 27:  # ESC to cancel
        state.menu_mode = "main"
        state.menu_input = ""
    elif key == 10 or key == 13:  # Enter to confirm
        confirm_text_input(state, input_mode)
    elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
        state.menu_input = state.menu_input[:-1]
    elif 48 <= key <= 57:  # 0-9
        state.menu_input += chr(key)
    elif key == ord(".") and input_mode == "delay_input":  # Allow decimal point
        if "." not in state.menu_input:
            state.menu_input += chr(key)


def confirm_text_input(state, input_mode: str) -> None:
    """
    Confirm and apply text input.

    Args:
        state: State object
        input_mode: "rule_input" or "delay_input"
    """
    if input_mode == "rule_input":
        try:
            rule = int(state.menu_input)
            if 0 <= rule <= 255:
                state.rule_number = rule
                reset_simulation(state)
                state.menu_mode = "main"
                state.menu_input = ""
        except ValueError:
            state.menu_input = ""
    elif input_mode == "delay_input":
        try:
            delay = float(state.menu_input)
            if delay > 0:
                state.step_delay = delay
                state.menu_mode = "main"
                state.menu_input = ""
        except ValueError:
            state.menu_input = ""


def apply_menu_selection(state) -> None:
    """
    Execute the selected menu action.

    Args:
        state: State object
    """
    selection = MENU_ITEMS[state.menu_selection]

    if selection == "Set Rule Number":
        state.menu_mode = "rule_input"
        state.menu_input = str(state.rule_number)
    elif selection == "Set Step Delay":
        state.menu_mode = "delay_input"
        state.menu_input = str(state.step_delay)
    elif selection == "Toggle Mode":
        if state.simulation_mode == "auto":
            state.simulation_mode = "step"
        elif state.simulation_mode == "step":
            state.simulation_mode = "auto"
    elif selection == "Reset Simulation":
        reset_simulation(state)
        state.menu_open = False
    elif selection == "Resume":
        state.menu_open = False
    elif selection == "Quit":
        state.running = False
        state.menu_open = False


# Import curses at module level
import curses
