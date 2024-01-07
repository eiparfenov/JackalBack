from Utils import Vector2i


class JackalActionsBase:
    def __init__(self, for_player: int = -1):
        self.for_player = for_player
        self.type = 'base'


class JackalActionSpawnPirate(JackalActionsBase):
    def __init__(self, pirate_id: str, player_owner: int, position: Vector2i,  pirate_type: str = "simple"):
        super().__init__()
        self.type = "spawn_pirate"
        self.pirate_id = pirate_id
        self.position = position
        self.player_owner = player_owner
        self.pirate_type = pirate_type

    @staticmethod
    def from_pirate(pirate):
        return JackalActionSpawnPirate(
                pirate_id=pirate.id,
                position=pirate.position,
                player_owner=pirate.player_owner,
                pirate_type=pirate.pirate_type
            )


class JackalActionSpawnShip(JackalActionsBase):
    def __init__(self, ship_id: str, position: Vector2i, ship_type: str, player_owner: int):
        super().__init__()
        self.type = "spawn_ship"
        self.position = position
        self.ship_id = ship_id
        self.player_owner = player_owner
        self.ship_type = ship_type

    @staticmethod
    def from_ship(ship):
        return JackalActionSpawnShip(
            ship_id=ship.id,
            ship_type=ship.ship_type,
            player_owner=ship.player_owner,
            position=ship.position
        )


class JackalActionMoveShip(JackalActionsBase):
    def __init__(self, ship_id: str, move_position: Vector2i):
        super().__init__()
        self.type = "move_ship"
        self.ship_id = ship_id
        self.move_position = move_position


class JackalActionMovePirate(JackalActionsBase):
    def __init__(self, pirate_id: str, move_position: Vector2i):
        super().__init__()
        self.move_position = move_position
        self.pirate_id = pirate_id
        self.type = "move_pirate"


class JackalActionOpenCard(JackalActionsBase):
    def __init__(self, frame: int, rotation: int, open_position: Vector2i):
        super().__init__()
        self.open_position = open_position
        self.rotation = rotation
        self.frame = frame
        self.type = "open_card"
