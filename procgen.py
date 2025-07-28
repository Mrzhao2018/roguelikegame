from __future__ import annotations

import re
from typing import Tuple, Iterable, List, TYPE_CHECKING
import random

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
    

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2) # This ensures that we’ll always have at least a one tile wide wall between our rooms, unless we choose to create overlapping rooms. In order to accomplish this, we add + 1 to x1 and y1.
    
    def intersects(self, other: RectangularRoom) -> bool:
        """Check if this room intersects with another room."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterable[Tuple[int, int]]:
    """Generate a tunnel between two points."""
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        # Horizontal first, then vertical
        corner_x, corner_y = x2, y1
    else:
        # Vertical first, then horizontal
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, map_width - room_width - 1)
        y = random.randint(0, map_height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
        # If the room is valid, add it to the list of rooms
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # This is the first room, place the player there
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(
                rooms[-1].center, new_room.center
            ):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list of rooms
        rooms.append(new_room)

    return dungeon