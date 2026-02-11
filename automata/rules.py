"""Elementary cellular automata rule encoding/decoding."""


def decode_rule(rule_number: int) -> list[int]:
    """
    Convert a rule number (0-255) to a lookup table of 8 transitions.

    Each rule number encodes all possible outcomes for 3-cell neighborhoods.
    The rule number's binary representation maps neighborhoods to outcomes:
    - Neighborhood index 0 (000) → bit 0
    - Neighborhood index 1 (001) → bit 1
    - ...
    - Neighborhood index 7 (111) → bit 7

    Args:
        rule_number: Integer 0-255 representing the CA rule

    Returns:
        List of 8 integers (0 or 1) indexed by neighborhood value

    Example:
        Rule 30 = 0b00011110
        Bit positions: 76543210
        Lookup table: [0,1,1,1,1,0,0,0]
    """
    return [(rule_number >> i) & 1 for i in range(8)]


def neighborhood_to_index(left: int, center: int, right: int) -> int:
    """
    Convert a 3-cell neighborhood to an index 0-7.

    Args:
        left: Left cell value (0 or 1)
        center: Center cell value (0 or 1)
        right: Right cell value (0 or 1)

    Returns:
        Index 0-7 representing the neighborhood

    Example:
        neighborhood_to_index(1, 1, 1) → 7
        neighborhood_to_index(0, 0, 0) → 0
    """
    return left * 4 + center * 2 + right


def get_next_cell(
    rule_transitions: list[int], left: int, center: int, right: int
) -> int:
    """
    Compute the next state of a cell given its neighborhood.

    Args:
        rule_transitions: Lookup table from decode_rule()
        left: Left neighbor value
        center: Center cell value
        right: Right neighbor value

    Returns:
        Next state of the center cell (0 or 1)
    """
    index = neighborhood_to_index(left, center, right)
    return rule_transitions[index]
