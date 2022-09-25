import json

from broadcaster import Broadcast

from internal.config import REDIS_DATABASE_URL


broadcast = Broadcast(REDIS_DATABASE_URL)


async def ws_receiver(websocket, chatname, username):
    async for message in websocket.iter_text():
        await broadcast.publish(chatname, message=json.dumps({'user': username, 'data': message}))


async def ws_sender(websocket, chatname):
    async with broadcast.subscribe(chatname) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
