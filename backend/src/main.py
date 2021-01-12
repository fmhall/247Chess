from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request, status
from utils.events import status_event_generator
from utils.chess_utils import pgn_to_game
from utils.work_queue import work_queue
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import models
from uvicorn.config import LOGGING_CONFIG

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(
    __name__
)  # the __name__ resolve to "main" since we are at the root of the project.
# This will get the root logger since no logger in the configuration has this name.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


@router.get("/status/stream")
async def runStatus(request: Request, response: Response):
    event_generator = status_event_generator(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return EventSourceResponse(event_generator)


app.include_router(router)


@app.post("/game", status_code=status.HTTP_202_ACCEPTED)
def post_game(pgn_request: models.PgnRequest):
    game = pgn_to_game(pgn_request.pgn)
    if game:
        work_queue.add_work_item(models.Work(game=game, completed=False))
    else:
        logger.debug("Could not load game")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"pgn": str(game)})
