import random
from Utils import *
from JackalOptions import *


class JackalCardBase:
    COUNT_IN_STACK = 0
    CENTER_WEIGHT = 0
    AWAY_WEIGHT = 0
    FRAMES = []

    def __init__(self, position: Vector2i):
        self.type = "base"
        self.position = position
        self.frame = random.choice(self.FRAMES)
        self.rotation = random.randint(0, 3)
        self.can_stand = True

    def get_possible_options_for_pirate(
            self,
            pirate,
            board,
            with_items: [] = (),
            for_player: int = None
    ) -> [JackalOptionBase]:
        raise NotImplementedError


class JackalCardWater(JackalCardBase):
    FRAMES = [-1]

    def __init__(self, position: Vector2i):
        super().__init__(position)
        self.type = "water"

    def get_possible_options_for_pirate(
            self,
            pirate,
            board,
            with_items: [] = (),
            for_player: int = None
    ) -> [JackalOptionBase]:
        options: [JackalOptionBase] = []
        ship = next((ship for ship in board.ships if ship.position == self.position), None)
        if ship is None:  # Пират плывет
            for direction in Vector2iUtils.DIRECTIONS:
                new_position = self.position + direction
                if new_position.is_in_box(board.SIZE + board.WATER_SIZE) and not new_position.is_in_box(board.SIZE):
                    options.append(JackalOptionMovePirate(
                        for_player=for_player if for_player is not None else pirate.player_owner,
                        pirate_id=pirate.id,
                        position=new_position,
                    ))
        else:  # Пират на корабле
            if self.position.is_on_side_of_box(board.SIZE):  # Пират сходит на берег
                options.append(JackalOptionMovePirate(
                    for_player=for_player if for_player is not None else pirate.player_owner,
                    pirate_id=pirate.id,
                    position=self.position.direction_to_center() + self.position
                ))

            for direction in Vector2iUtils.DIRECTIONS if ship.moves_diagonal else Vector2iUtils.DIRECTIONS_STRAIGHT:
                new_position = self.position + direction
                if new_position.is_in_box(board.SIZE + 2) and not new_position.is_in_box(board.SIZE):
                    options.append(JackalOptionMovePirate(
                        for_player=for_player if for_player is not None else pirate.player_owner,
                        pirate_id=pirate.id,
                        position=new_position,
                    ))
        return options


class JackalCardEmpty(JackalCardBase):
    FRAMES = [37, 38, 39, 40]
    COUNT_IN_STACK = 200

    def __init__(self, position: Vector2i):
        super().__init__(position)
        self.type = "simple"

    def get_possible_options_for_pirate(
            self,
            pirate,
            board,
            with_items: [] = (),
            for_player: int = None
    ) -> [JackalOptionBase]:
        options: [JackalOptionBase] = []
        for direction in Vector2iUtils.DIRECTIONS:
            options.append(JackalOptionMovePirate(
                for_player=for_player if for_player is not None else pirate.player_owner,
                pirate_id=pirate.id,
                position=self.position + direction
            ))
        return options


class JackalCardArrowBase(JackalCardBase):
    DIRECTIONS = []

    def __init__(self, position: Vector2i):
        super().__init__(position)
        self.type = "arrow"
        self.can_stand = False
        self.directions = (direction.rotate(self.rotation) for direction in self.DIRECTIONS)

    def get_possible_options_for_pirate(
            self,
            pirate,
            board,
            with_items: [] = (),
            for_player: int = None
    ) -> [JackalOptionBase]:
        options: [JackalOptionBase] = []
        for direction in self.directions:
            options.append(JackalOptionMovePirate(
                for_player=for_player if for_player is not None else pirate.player_owner,
                pirate_id=pirate.id,
                position=self.position + direction
            ))
        return options


class JackalCardArrowUp(JackalCardArrowBase):
    COUNT_IN_STACK = 4
    DIRECTIONS = [Vector2iUtils.UP]


class JackalCardArrowDiagonal(JackalCardArrowBase):
    COUNT_IN_STACK = 4
    DIRECTIONS = [Vector2i(1, 1)]


class JackalCardArrowCross(JackalCardArrowBase):
    COUNT_IN_STACK = 1
    DIRECTIONS = Vector2iUtils.DIRECTIONS_STRAIGHT
