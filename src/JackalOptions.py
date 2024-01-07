import uuid

from JackalActions import *


class JackalOptionBase:
    def __init__(self, for_player: int):
        self.group_id = "not grouped"
        self.for_player = for_player
        self.id = str(uuid.uuid4())
        self.type = "base"

    def execute(self, board) -> (['JackalOptionBase'], ['JackalActionsBase'], bool):
        raise NotImplementedError

    @staticmethod
    def get_card(board, position: Vector2i):
        return next((card for card in board.cards if card.position == position), None)

    @staticmethod
    def get_pirate(board, pirate_id: str):
        return next((pirate for pirate in board.pirates if pirate.id == pirate_id), None)

    @staticmethod
    def get_ship_by_position(board, position: Vector2i):
        return next((ship for ship in board.ships if ship.position == position), None)

    @staticmethod
    def get_pirates_at_position(board, position: Vector2i):
        return list(pirate for pirate in board.pirates if pirate.position == position)


class JackalOptionSelectPirate(JackalOptionBase):
    def __init__(self, for_player: int, pirate_id: str):
        super().__init__(for_player)
        self.type = "select_pirate"
        self.pirate_id = pirate_id

    def execute(self, board) -> (['JackalOptionBase'], ['JackalActionsBase'], bool):
        # TODO: Check for items
        pirate = self.get_pirate(board, self.pirate_id)
        if pirate is None:
            raise Exception("Wrong pirate id")
        card = board.get_card(pirate.position)
        if card is None:
            raise Exception(f"No card at position {pirate.position}")

        options = card.get_possible_options_for_pirate(pirate, board)
        return options, [], False


class JackalOptionMovePirate(JackalOptionBase):
    def __init__(self, for_player: int, pirate_id: str, position: Vector2i, take_items: [str] = ()):
        super().__init__(for_player)
        self.type = "move_pirate"
        self.position = position
        self.pirate_id = pirate_id
        self.take_items = take_items

    def execute(self, board) -> (['JackalOptionBase'], ['JackalActionsBase'], bool):
        actions: [JackalActionsBase] = []
        options: [JackalOptionBase] = []
        pirate = self.get_pirate(board, self.pirate_id)
        if pirate is None:
            raise Exception('Pirate not found')

        start_card = self.get_card(board, pirate.position)
        end_card = self.get_card(board, self.position)

        if end_card is not None and start_card.type == "water" and end_card.type == "water":  # пират плывет
            ship = self.get_ship_by_position(board, pirate.position)
            if ship is not None:  # плывет на корабле
                for moving_pirate in self.get_pirates_at_position(board, pirate.position):
                    self.add_move_action_for_pirate(actions, moving_pirate)
                actions.append(JackalActionMoveShip(
                    ship_id=ship.id,
                    move_position=self.position
                ))
                ship.position = self.position
                return options, actions, True

        if end_card is None:  # открытие новой карточки
            open_action = board.open_card(self.position)
            actions.append(open_action)

        self.add_move_action_for_pirate(actions, pirate)
        return options, actions, True

    def add_move_action_for_pirate(self, actions, pirate):
        actions.append(JackalActionMovePirate(
            pirate_id=pirate.id,
            move_position=self.position
        ))
        pirate.position = self.position
