import asyncio

import jsonpickle

from JackalBoard import JackalBoardResponse, JackalBoard


class Room:
    def __init__(self, max_players):
        self.__max_players = max_players
        self.__players = {}
        self.__board = JackalBoard(max_players)
        self.__nick_names = {}

    def is_fit(self):
        return len(self.__players.keys()) == self.__max_players

    async def add_player(self, player, name, color) -> int:
        new_color = color
        if color in self.__players.keys():
            new_color = next((c for c in range(self.__max_players) if c not in self.__players.keys()))

        self.__players[new_color] = player
        self.__nick_names[new_color] = name
        return new_color

    async def start_game(self):
        if not self.is_fit(): return

        response = RoomStartGameResponse(
            players=list([RoomStartGameResponse.Player(nick_name, color) for color, nick_name in self.__nick_names.items()]),
        )

        for color, player in self.__players.items():
            response.color = color
            await player.send(self.to_json(response))

        await asyncio.sleep(1)  # TODO убрать костыль

        response = self.__board.start()
        print(self.to_json(response))

        for color, player in self.__players.items():
            self.to_json(response.for_player(color))

            await player.send(self.to_json(response.for_player(color)))

    async def msg(self, msg, color):
        if not self.is_fit():
            return

        response = self.__board.perform_option(msg)
        print(response)

        for color, player in self.__players.items():
            await player.send(self.to_json(response.for_player(color)))

    @staticmethod
    def to_json(obj):
        return jsonpickle.dumps(obj, unpicklable=False, indent=2)


class RoomFactory:
    def __init__(self, max_players):
        self.__max_players = max_players
        self.__rooms = []

    async def get_room(self, player, name, expected_color) -> (Room, int):
        not_fitted_room = next((room for room in self.__rooms if not room.is_fit()), None)
        if not_fitted_room is None:
            not_fitted_room = Room(2)
            self.__rooms.append(not_fitted_room)
        color = await not_fitted_room.add_player(player, name, expected_color)
        return not_fitted_room, color


class RoomStartGameResponse:
    class Player:
        def __init__(self, name, color):
            self.color = color
            self.name = name

    def __init__(self, players: [Player]):
        self.color = -1
        self.players = players
        self.event_type = "game_started"


room_factory = RoomFactory(2)
