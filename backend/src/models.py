from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Dict, Optional, List, Any
from uuid import UUID
import uuid
import string
import random
import chess.pgn


def random_string(string_length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(string_length))


@dataclass
class PlayerInfo:
    name: str
    sub_text: str = "???? - ????"
    image_url: str = "https://media.discordapp.net/attachments/713929687969038337/822008816987275264/image0.jpg"


@dataclass
class Headers:
    date: str
    event: str
    round: str
    white: str
    black: str

    def get_headers(self):
        if self.date.find(".?") >= 0:
            date = self.date[: self.date.find(".?")]
        else:
            date = ""
        event = self.event if "?" not in self.event else ""
        round_num = "Round " + self.round if "?" not in self.round else ""
        combined = " - ".join([date, event, round_num]).rstrip(" - ")
        return {**self.__dict__, "combined": combined}


def headers_from_game(game: chess.pgn.GameT) -> Headers:
    headers = Headers(
        date=game.headers["Date"],
        event=game.headers["Event"],
        round=game.headers["Round"],
        white=game.headers["White"],
        black=game.headers["Black"],
    )
    return headers


@dataclass
class Work:
    game: chess.pgn.GameT
    fen_list: List[str]
    annotation_list: List[str]
    move_list: List[List[str]]
    completed: bool
    headers: Headers
    white_player_info: Optional[PlayerInfo] = None
    black_player_info: Optional[PlayerInfo] = None

    def get_update(self, move_number):
        return {
            "fen": self.fen_list[move_number],
            "uci": self.move_list[move_number],
            "anno": self.annotation_list[move_number],
        }

    def get_game_data(self):
        return {
            "headers": self.headers.get_headers(),
            "white": self.white_player_info.__dict__,
            "black": self.black_player_info.__dict__,
        }


class PgnRequest(BaseModel):
    pgn: str
