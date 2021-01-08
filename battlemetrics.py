#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timedelta
from math import ceil, floor
from time import sleep
from typing import Dict, List, Optional

import click
import requests

from lib.session import Session
from lib.tracker import TimeTracker


@click.group()
def cli() -> None:
    """scripts for gathering and processing battlemetrics data"""


@click.command()
@click.option("--days", type=click.IntRange(0, 365), default=30)
@click.option("--desired-players", type=click.IntRange(2, 999), default=32)
@click.option("--size", type=click.IntRange(1, 9999), default=20)
@click.option("--token", type=click.STRING)
@click.option(
    "--token-path", type=click.Path(exists=True, resolve_path=True, dir_okay=False)
)
@click.option("--server-id", type=click.INT)
@click.option("--server-name", type=click.STRING)
def seeders(
    days: int,
    desired_players: int,
    size: int,
    token: Optional[str],
    token_path: Optional[str],
    server_id: Optional[int],
    server_name: Optional[str],
):
    if not token:
        if not token_path:
            raise ValueError("--token-path is required")
        with open(token_path, "r") as token_file:
            token = token_file.read().replace("\n", "")

    if not server_id and not server_name:
        raise ValueError("--server-name is required")
    if not server_id and server_name:
        servers_dict = search_servers(server_name, token)
        if len(servers_dict) > 1:
            print(servers_dict)
        if len(servers_dict) != 1:
            raise ValueError(f'--server-name="{server_name}" is not valid')
        server_id = list(servers_dict.keys())[0]

    dt = datetime.utcnow()
    stop = dt.isoformat() + "Z"
    start = (dt - timedelta(days=days)).isoformat() + "Z"

    next_url = "https://api.battlemetrics.com/sessions"
    params: Optional[Dict[str, str]] = {
        "filter[servers]": f"{server_id}",
        "filter[range]": f"{start}:{stop}",
        "page[size]": "100",
    }

    sessions: List[Session] = list()
    tracker = TimeTracker()

    while next_url:
        response: Optional[requests.Response] = None

        for _ in range(5):
            response = requests.get(
                url=next_url, params=params, headers={"Authorization": f"Bearer {token}"}
            )
            if response.ok:
                break
            sleep(1 / 5)
        assert response

        if not response.ok:
            response.raise_for_status()

        for session in response.json().get("data", []):
            sessions.insert(
                0,
                Session(
                    id=session.get("relationships", {})
                    .get("player", {})
                    .get("data", {})
                    .get("id", None),
                    name=session.get("attributes", {}).get("name", ""),
                    start=session.get("attributes", {}).get("start", None),
                    stop=session.get("attributes", {}).get("stop", dt.isoformat() + "Z"),
                ),
            )

        next_url = response.json().get("links", {}).get("next", None)
        params = None

    online_sessions: List[Session] = list()

    for session in sessions:
        cursor_time = session.get_start_time()

        for online_session in online_sessions.copy():
            if len(online_sessions) < desired_players:
                tracker.add(
                    id=online_session.id,
                    name=online_session.name,
                    seconds=(cursor_time - online_session.get_start_time()).seconds,
                )
            if cursor_time < online_session.get_stop_time():
                online_session.set_start_time(cursor_time)
            else:
                online_sessions.remove(online_session)

        online_sessions.append(session)

    if len(online_sessions) < desired_players:
        for online_session in online_sessions:
            tracker.add(
                id=online_session.id,
                name=online_session.name,
                seconds=(
                    online_session.get_stop_time() - online_session.get_start_time()
                ).seconds,
            )

    for player in sorted(tracker, reverse=True)[:size]:
        print(
            f"{player.names[0].ljust(32)} "
            f"{int(player.seconds / 60 / 60)}hrs "
            f"{ceil(player.seconds / 60) % 60}mins"
        )


@click.command()
@click.option("--token", type=click.STRING)
@click.option(
    "--token-path", type=click.Path(exists=True, resolve_path=True, dir_okay=False)
)
@click.option("--server-id", type=click.INT)
@click.option("--server-name", type=click.STRING)
def afkers(
    token: Optional[str],
    token_path: Optional[str],
    server_id: Optional[int],
    server_name: Optional[str],
):
    if not token:
        if not token_path:
            raise ValueError("--token-path is required")
        with open(token_path, "r") as token_file:
            token = token_file.read().replace("\n", "")
    if not server_id and not server_name:
        raise ValueError("--server-name is required")
    if not server_id and server_name:
        servers_dict = search_servers(server_name, token)
        if len(servers_dict) > 1:
            print(servers_dict)
        if len(servers_dict) != 1:
            raise ValueError(f'--server-name="{server_name}" is not valid')
        server_id = sorted(list(servers_dict.keys()), reverse=True)[0]
    response = requests.get(
        url=f"https://api.battlemetrics.com/servers/{server_id}",
        params={"include": "player"},
        headers={"Authorization": f"Bearer {token}"},
    )
    players = response.json()["included"]
    header = False
    for player in players:
        player_name: str = player["attributes"]["name"]
        seconds: Optional[float] = None
        squad_id: Optional[int] = None
        score: Optional[int] = 0
        for metadata in player["meta"]["metadata"]:
            if metadata["key"] == "squadID":
                squad_id = metadata["value"]
            elif metadata["key"] == "time":
                seconds = metadata["value"]
            elif metadata["key"] == "score":
                score = metadata["value"]
        minutes = floor(seconds / 60) if seconds else 0
        if squad_id is None:
            if not header:
                print("Name                             Session   Score")
                header = True
            print(
                f"{player_name.ljust(32)} "
                f"{(str(minutes) + 'min').ljust(10)}"
                f"{score}pts"
            )
    return


def search_servers(query: str, token: str, online_only=True) -> Dict[int, str]:
    results: Dict[int, str] = dict()
    response = requests.get(
        url="https://api.battlemetrics.com/servers",
        params={"fields[server]": "name,status", "filter[search]": f'"{query}"'},
        headers={"Authorization": f"Bearer {token}"},
    )
    for server in response.json()["data"]:
        if server["attributes"]["status"] == "online" or not online_only:
            results[int(server["id"])] = server["attributes"]["name"]
    return results


cli.add_command(seeders)
cli.add_command(afkers)

if __name__ == "__main__":
    cli()
