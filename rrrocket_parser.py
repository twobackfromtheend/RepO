import json
import subprocess
from pathlib import Path
from typing import List, Tuple

from game import Game

print(subprocess.run(f"rrrocket -V", check=True, capture_output=True).stdout.decode("utf-8").strip())


def parse_all_replays(folder: Path) -> List[Tuple[Game, Path]]:
    games = []
    for replay_filepath in folder.glob("*.replay"):
        # cache_filepath = cache_folder / str(replay_filepath.name) + ".json"
        rrrocket_json = parse_replay(replay_filepath)
        game = Game(rrrocket_json['properties'])
        games.append((game, replay_filepath))
    return games


def parse_replay(replay_filepath: Path):
    return json.loads(subprocess.run(f"rrrocket \"{str(replay_filepath)}\"", check=True, capture_output=True).stdout)
