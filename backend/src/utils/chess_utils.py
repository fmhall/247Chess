import chess.pgn
import logging
import io
import models
import os
import requests
from typing import Optional

logger = logging.getLogger(__name__)

pgn_name = "games.pgn"


def pgn_to_game(pgn: str):
    f_pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(f_pgn)
    logger.info(game)

    return game


def load_games_from_file(player_name: str, num_games: int = -1):
    filename = "/".join(["utils", player_name, pgn_name])
    pgn = open(os.path.abspath(filename))
    i = 0
    work_list = []
    notable_players = get_notable_players()
    if num_games < 0:
        num_games = 1000
    while i < num_games:
        logger.debug(i)
        game = chess.pgn.read_game(pgn)
        fen_list = []
        annotations_list = []
        move_list = []
        if game:
            node = game.next()
            while node:
                annotations_list.append(node.comment)
                fen_list.append(node.board().fen())
                move_list.append(
                    [
                        chess.square_name(node.move.from_square),
                        chess.square_name(node.move.to_square),
                    ]
                )
                node = node.next()
            headers = models.headers_from_game(game)
            white_player_info = get_player_info_from_pgn_name(
                headers.white, notable_players
            )
            black_player_info = get_player_info_from_pgn_name(
                headers.black, notable_players
            )
            work = models.Work(
                game=game,
                headers=headers,
                move_list=move_list,
                annotation_list=annotations_list,
                fen_list=fen_list,
                completed=False,
                white_player_info=white_player_info,
                black_player_info=black_player_info,
            )
            work_list.append(work)
            print(work)
        i += 1
    return work_list


def get_player_info_from_pgn_name(
    name: str, notable_players
) -> Optional[models.PlayerInfo]:
    for notable_player in notable_players:
        aliases = notable_player["pgnAliases"]
        aliases.append(aliases[0].split(",")[0])
        if name in aliases:
            return models.PlayerInfo(
                name=notable_player["name"],
                image_url=notable_player["profile"]["imageUrl"],
                sub_text=notable_player["profile"]["subText"],
            )
    return models.PlayerInfo(name=name)


def get_notable_players():
    r = requests.get("https://goatchess.github.io/list.json")
    response = r.json()
    return response["list"]
