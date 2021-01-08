
from dataclasses import dataclass, field

from typing import List, Dict, Union

from lib.player import Player


@dataclass
class TimeTracker:
    _players: Dict[str, Player] = field(default_factory=dict)

    def __iter__(self):
        for player in self._players.values():
            yield player

    def add(self, id: str, name: str, seconds: int):
        if id in self._players:
            self._players[id].add_name(name)
            self._players[id].add_seconds(seconds)
        else:
            self._players[id] = Player(
                id=id,
                names=[name],
                seconds=seconds
            )

    def get_player_by_id(self, id: str) -> Union[Player, None]:
        return self._players.get(id, None)

    def get_player_by_name(self, name: str) -> List[Player]:
        return list(
            filter(
                lambda x: name in x.names, self._players.values()
            )
        )
