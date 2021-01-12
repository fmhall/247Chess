from collections import deque
from typing import Deque, Dict, Optional, Set, List
import logging
from models import Work
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

    def get_next_work_item(self) -> Optional[Work]:
        if self.work_deque:
            return self.work_deque.pop()

    def __len__(self):
        return len(self.work_deque)


work_queue = WorkQueue()

