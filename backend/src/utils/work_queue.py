from collections import deque
from typing import Deque, Dict, Optional, Set, List
import logging
from models import Work
from utils.chess_utils import load_games_from_file

logger = logging.getLogger(__name__)


class WorkQueue:
    """
    Work Queue for engine analysis work
    Also stores game analysis information
    """

    work_deque: Deque[Work]

    def __init__(self):
        self.work_deque = deque()

    def add_work_item(self, item: Work):
        self.work_deque.append(item)
        print(item)

    def get_next_work_item(self) -> Optional[Work]:
        if self.work_deque:
            return self.work_deque.pop()

    def __len__(self):
        return len(self.work_deque)


work_queue = WorkQueue()
work_list = load_games_from_file("famous", num_games=10)
for work in work_list:
    work_queue.add_work_item(work)
