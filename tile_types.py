from math import floor
from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint for the character
        ("fg", "3B"),  # Foreground color (RGB)
        ("bg", "3B"),  # Background color (RGB)
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # Can the player walk on this tile?
        ("transparent", np.bool_),  # Can the player see through this tile?
        ("dark", graphic_dt),  # Tile graphic when not lit
    ]
)

def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    """
    Create a new tile with the given properties.
    
    :param walkable: Can the player walk on this tile?
    :param transparent: Can the player see through this tile?
    :param dark: Graphic data for the tile when not lit
    :return: A numpy array representing the tile
    """
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150))
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (255, 255, 255), (0, 0, 100))
)