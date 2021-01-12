import asyncio
import logging
from datetime import datetime, timedelta
import models
from typing import Optional
from utils.work_queue import work_queue
import json

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
"""
Get status as an event generator
"""
status_stream_delay = 3  # second
status_stream_retry_timeout = 30000  # milisecond


async def status_event_generator(request):
    work: Optional[models.Work] = None
    move_number = 0
    while True:
        if await request.is_disconnected():
            logger.debug("Request disconnected")
            break
        if work:
            if not work.completed:
                if move_number < len(work.fen_list):
                    logger.debug(work.get_update(move_number))
                    yield {
                        "event": "update",
                        "retry": status_stream_retry_timeout,
                        "data": json.dumps(work.get_update(move_number)),
                    }
                    move_number += 1
                else:
                    work.completed = True
            else:
                logger.debug("Getting new game")
                work = work_queue.get_next_work_item()
                move_number = 0
        else:
            work = work_queue.get_next_work_item()
            move_number = 0
            if not work:
                logger.debug("No game found")
                yield {"event": "no_game", "data": ""}
            else:
                logger.debug(work.get_game_data())
                yield {"event": "new_game", "data": json.dumps(work.get_game_data())}

        await asyncio.sleep(status_stream_delay)
