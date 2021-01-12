import asyncio
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
'''
Get status as an event generator
'''
status_stream_delay = .5  # second
status_stream_retry_timeout = 30000  # milisecond


async def status_event_generator(request):
    start = datetime.now()
    previous_status = datetime.now()
    while True:
        if await request.is_disconnected():
            logger.debug('Request disconnected')
            break

        if previous_status and previous_status - start > timedelta(minutes=5):
            logger.debug('Request completed. Disconnecting now')
            yield {
                "event": "end",
                "data": ''
            }
            break

        current_status = datetime.now()
        if previous_status.strftime("%Y-%m-%d-%M-%S") != current_status.strftime("%Y-%m-%d-%M-%S"):
            yield {
                "event": "update",
                "retry": status_stream_retry_timeout,
                "data": current_status.strftime("%Y-%m-%d-%M-%S")
            }
            previous_status = current_status
            logger.debug('Current status :%s', current_status)
        else:
            logger.debug('No change in status...')

        await asyncio.sleep(status_stream_delay)
