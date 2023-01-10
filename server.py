import os

from sse_starlette.sse import EventSourceResponse
from fastapi import Request, FastAPI, Response

import uvicorn
import asyncio

app = FastAPI()
root = os.path.dirname(os.path.abspath(__file__))


async def numbers(minimum, maximum):
    try:
        for i in range(minimum, maximum + 1):
            await asyncio.sleep(0.9)
            yield dict(data=i)
    except asyncio.CancelledError as e:
        print('client close request')
        print(e)
        raise e


@app.get('/sse')
async def route(
        request: Request
):
    event_generator = numbers(10, 20)
    return EventSourceResponse(event_generator)


@app.get("/")
async def main():
    with open(os.path.join(root, 'index.html')) as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")

if __name__ == '__main__':
    uvicorn.run('server:app', host='127.0.0.1', port=2929, log_level='info', reload=True)
