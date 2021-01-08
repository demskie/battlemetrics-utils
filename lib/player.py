from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from math import ceil
from typing import List


@dataclass
@total_ordering
class Player:
    id: str
    names: List[str]
    seconds: int

    def __lt__(self, other: Player) -> bool:
        return self.seconds < other.seconds

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Player) and self.seconds == other.seconds

    def __str__(self) -> str:
        return (
            f"'{self.names[0]}' "
            f"{int(self.seconds/60/60)}hrs "
            f"{ceil(self.seconds/60)%60}mins"
        )

    def add_name(self, name: str) -> None:
        self.names = list(set([*self.names, name]))

    def add_seconds(self, seconds: int) -> None:
        self.seconds += seconds
