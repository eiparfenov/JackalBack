import asyncio
import websockets
from Rooms import room_factory


async def websocket_connection(websocket):
    name, expected_color = (await websocket.recv()).split()
    room, color = await room_factory.get_room(websocket, name, expected_color)
    print(f"joined player with room expected color {expected_color}")
    await room.start_game()
    async for msg in websocket:
        pass


async def main():
    async with websockets.serve(websocket_connection, "localhost", 5002):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
