from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
from uuid import UUID
import uuid
import string
import random
import chess.pgn


def random_string(string_length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(string_length))


class Work(BaseModel):
    game: chess.pgn.GameT
    completed: bool


class PgnRequest(BaseModel):
    pgn: str

