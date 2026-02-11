"""Application state management for cellular automata."""

from dataclasses import dataclass, field


@dataclass
class State:
    """Central state object holding all application data."""

    # Rule and simulation configuration
    rule_number: int = 30
    step_delay: float = 0.1
    simulation_mode: str = "none"  # "none" | "auto" | "step"
    step_requested: bool = False

    # Menu state
    menu_open: bool = False
    menu_selection: int = 0
    menu_mode: str = "main"  # "main" | "rule_input" | "delay_input"
    menu_input: str = ""

    # Grid state
    grid: list = field(default_factory=list)
    current_row: int = 0

    # Application control
    running: bool = True

    # Display dimensions
    width: int = 80
    height: int = 160

    # Precomputed rule lookup table
    rule_transitions: list = field(default_factory=list)
