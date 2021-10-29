import asyncio
import logging
import models
from typing import Optional
from utils.work_queue import work_queue
import json
import random

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
"""
Get status as an event generator
"""
status_stream_delay = 4  # second
status_stream_retry_timeout = 30000  # milisecond


async def status_event_generator(request):
    work: Optional[models.Work] = None
    move_number = 0
    while True:
        has_annotation = False
        is_new_game = False
        game_end = False
        if await request.is_disconnected():
            logger.debug("Request disconnected")
            break
        if work:
            if not work.completed:
                if move_number < len(work.fen_list):
                    logger.debug(work.get_update(move_number))
                    data = work.get_update(move_number)
                    if data["anno"]:
                        has_annotation = True
                    if move_number == len(work.fen_list) - 1:
                        game_end = True
                    if game_end and not has_annotation:
                        data["anno"] = "Game over."
                    yield {
                        "event": "update",
                        "retry": status_stream_retry_timeout,
                        "data": json.dumps(data),
                    }
                    move_number += 1
                else:
                    work.completed = True
            else:
                work.completed = False
                work_queue.add_work_item_to_back(work)
                work = None
        else:
            logger.debug("Getting new game")
            work = work_queue.get_next_work_item()
            move_number = 0
            if not work:
                logger.debug("No game found")
                yield {"event": "no_game", "data": ""}
            else:
                logger.debug(work.get_game_data())
                yield {"event": "new_game", "data": json.dumps(work.get_game_data())}
                is_new_game = True

        if is_new_game:
            delay = 2
        elif game_end:
            delay = 5
        elif has_annotation:
            delay = 20
        elif move_number < 15:
            delay = 5 + random.randint(-2, 2)
        else:
            delay = status_stream_delay + random.randint(-3, 3)
        await asyncio.sleep(delay)
