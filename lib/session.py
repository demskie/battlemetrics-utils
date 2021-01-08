from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Session:
    id: str
    name: str
    start: str
    stop: str

    def get_start_time(self) -> datetime:
        assert self.start
        return datetime.fromisoformat(self.start.replace("Z", "")).replace(tzinfo=timezone.utc)

    def set_start_time(self, start_time: datetime) -> None:
        self.start = start_time.isoformat()

    def get_stop_time(self) -> datetime:
        return datetime.fromisoformat(self.stop.replace("Z", "")).replace(tzinfo=timezone.utc) if self.stop else datetime.utcnow().replace(tzinfo=timezone.utc)
