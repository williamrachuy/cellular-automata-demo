"""Rendering system for the cellular automata application."""

from automata.ui.menu import MENU_ITEMS


def render(stdscr, state) -> None:
    """
    Main rendering entry point.

    Args:
        stdscr: curses window object
        state: State object
    """
    stdscr.clear()

    try:
        height, width = stdscr.getmaxyx()
    except:
        height, width = state.height, state.width

    lines = build_display_lines(state, width, height)

    for i, line in enumerate(lines):
        if i >= height:
            break
        try:
            stdscr.addstr(i, 0, line[: width - 1])
        except:
            pass

    stdscr.refresh()


def build_display_lines(state, width: int, height: int) -> list[str]:
    """
    Build the complete display as a list of strings.

    Args:
        state: State object
        width: Terminal width
        height: Terminal height

    Returns:
        List of strings, one per line to display
    """
    lines = [""] * height

    # Render rule panel at top (3 rows)
    render_ruleset_panel(lines, state, width)

    # Separator line
    lines[2] = "─" * width

    # Render CA grid
    render_automata_grid(lines, state, width, height, 3)

    # Render status line at bottom
    render_status_line(lines, state, height)

    # Render menu if open
    if state.menu_open:
        render_menu(lines, state, width, height)

    return lines


def render_ruleset_panel(lines: list[str], state, width: int) -> None:
    """
    Render the rule visualization at the top.

    Shows the rule number and visual representation of all 8 transitions.

    Args:
        lines: List to modify in-place
        state: State object
        width: Terminal width
    """
    # Line 0: Rule number
    rule_label = f"Rule {state.rule_number}"
    lines[0] = rule_label.ljust(width)

    # Line 1: Visual representation of neighborhoods
    rule_text = "  "
    neighborhoods = [
        (7, "111"),
        (6, "110"),
        (5, "101"),
        (4, "100"),
        (3, "011"),
        (2, "010"),
        (1, "001"),
        (0, "000"),
    ]

    for idx, label in neighborhoods:
        result = "█" if state.rule_transitions[idx] else " "
        rule_text += f"{label}→{result}  "

    lines[1] = rule_text.ljust(width)


def render_automata_grid(
    lines: list[str], state, width: int, height: int, panel_height: int
) -> None:
    """
    Render the CA grid.

    Args:
        lines: List to modify in-place
        state: State object
        width: Terminal width
        height: Terminal height
        panel_height: Starting line for CA grid (skip rule panel)
    """
    grid_start = panel_height + 1
    grid_height = height - grid_start - 1  # Reserve bottom for status

    for row in range(grid_start, min(grid_start + grid_height, height)):
        grid_row = row - grid_start
        if grid_row < len(state.grid) and grid_row <= state.current_row:
            line = ""
            for cell in state.grid[grid_row][: width]:
                line += "█" if cell else " "
            lines[row] = line.ljust(width)
        else:
            lines[row] = " " * width


def render_status_line(lines: list[str], state, height: int) -> None:
    """
    Render the status line at the bottom.

    Args:
        lines: List to modify in-place
        state: State object
        height: Terminal height
    """
    status_line_idx = height - 1

    if state.simulation_mode == "none":
        status = "[Enter] Auto Mode  [Space] Step Mode  [ESC] Menu"
    elif state.simulation_mode == "auto":
        status = "[ESC] Menu  Running (Auto)..."
    else:  # step mode
        status = "[Space] Next Step  [ESC] Menu  (Step Mode)"

    lines[status_line_idx] = status.ljust(len(lines[status_line_idx]))


def render_menu(lines: list[str], state, width: int, height: int) -> None:
    """
    Render the menu overlay.

    Args:
        lines: List to modify in-place
        state: State object
        width: Terminal width
        height: Terminal height
    """
    menu_height = len(MENU_ITEMS) + 4  # Items + title + borders
    menu_width = 50
    start_y = (height - menu_height) // 2
    start_x = (width - menu_width) // 2

    # Draw menu background and border
    for y in range(start_y, min(start_y + menu_height, height)):
        for x in range(start_x, min(start_x + menu_width, width)):
            if y >= len(lines):
                continue
            if x >= len(lines[y]):
                lines[y] = lines[y].ljust(x + 1)

    # Build menu content
    if state.menu_mode == "main":
        render_main_menu(lines, state, start_y, start_x, menu_width, menu_height)
    elif state.menu_mode == "rule_input":
        render_rule_input(lines, state, start_y, start_x, menu_width)
    elif state.menu_mode == "delay_input":
        render_delay_input(lines, state, start_y, start_x, menu_width)


def render_main_menu(lines, state, start_y, start_x, width, height) -> None:
    """Render the main menu items."""
    title = "MENU"
    title_line = f"┌{title.center(width - 2)}┐".ljust(width)
    if start_y < len(lines):
        lines[start_y] = " " * start_x + title_line

    for i, item in enumerate(MENU_ITEMS):
        y = start_y + i + 1
        if y >= len(lines):
            break

        # Add current value for certain items
        display_item = item
        if item == "Set Rule Number":
            display_item = f"{item}: {state.rule_number}"
        elif item == "Set Step Delay":
            display_item = f"{item}: {state.step_delay}s"
        elif item == "Toggle Mode":
            mode_str = "Auto" if state.simulation_mode == "auto" else "Step"
            display_item = f"{item}: [{mode_str}]"

        # Highlight selected item
        if i == state.menu_selection:
            line = f"│ > {display_item:<{width-5}}│"
        else:
            line = f"│   {display_item:<{width-5}}│"

        lines[y] = " " * start_x + line

    # Bottom border
    bottom_y = start_y + len(MENU_ITEMS) + 1
    if bottom_y < len(lines):
        lines[bottom_y] = " " * start_x + f"└{'─' * (width - 2)}┘"


def render_rule_input(lines, state, start_y, start_x, width) -> None:
    """Render rule number input dialog."""
    title = "Enter Rule Number (0-255)"
    title_line = f"┌{title.center(width - 2)}┐".ljust(width)
    if start_y < len(lines):
        lines[start_y] = " " * start_x + title_line

    input_line = f"│ {state.menu_input:>{width-4}}│"
    if start_y + 1 < len(lines):
        lines[start_y + 1] = " " * start_x + input_line

    help_text = "[Enter] OK  [ESC] Cancel"
    help_line = f"│ {help_text:<{width-4}}│"
    if start_y + 2 < len(lines):
        lines[start_y + 2] = " " * start_x + help_line

    bottom_line = f"└{'─' * (width - 2)}┘"
    if start_y + 3 < len(lines):
        lines[start_y + 3] = " " * start_x + bottom_line


def render_delay_input(lines, state, start_y, start_x, width) -> None:
    """Render step delay input dialog."""
    title = "Enter Step Delay (seconds)"
    title_line = f"┌{title.center(width - 2)}┐".ljust(width)
    if start_y < len(lines):
        lines[start_y] = " " * start_x + title_line

    input_line = f"│ {state.menu_input:>{width-4}}│"
    if start_y + 1 < len(lines):
        lines[start_y + 1] = " " * start_x + input_line

    help_text = "[Enter] OK  [ESC] Cancel"
    help_line = f"│ {help_text:<{width-4}}│"
    if start_y + 2 < len(lines):
        lines[start_y + 2] = " " * start_x + help_line

    bottom_line = f"└{'─' * (width - 2)}┘"
    if start_y + 3 < len(lines):
        lines[start_y + 3] = " " * start_x + bottom_line
