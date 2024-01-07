from JackalCards import *


class JackalBoard:
    SIZE = 6
    WATER_SIZE = 3
    STACK = (
        JackalCardEmpty,
    )

    def __init__(self, max_players: int = 2):
        self.current_player = 0
        self.max_players = max_players

        self.ships: [JackalShip] = []
        self.pirates: [JackalPirate] = []
        self.cards: [JackalCardBase] = []
        self.items = []
        self.stack = []
        self.options: [JackalOptionBase] = []

        self.__create_water()
        self.__fill_stack()

    def start(self) -> 'JackalBoardResponse':
        if self.max_players == 2:
            actions = []
            actions.extend(self.__create_start_stuff_for_player(0, Vector2i(-1, 0)))
            actions.extend(self.__create_start_stuff_for_player(1, Vector2i(1, 0)))
            options = self.__get_start_options_for_player(0)
            self.options.extend(options)
            return JackalBoardResponse(options, actions)
        else:
            raise NotImplementedError

    def perform_option(self, option_id):
        # находит опцию по id
        option: JackalOptionBase = next((option for option in self.options if option.id == option_id), None)
        if option is None:
            print("Warning: wrong option id")
            return None

        options, actions, next_move = option.execute(self)  # выполняет ее и удаляет все опции из ее группы
        self.options = list(
            opt for opt in self.options if opt.group_id == "not_grouped" or opt.group_id != option.group_id)
        if next_move:  # если ход переходит к следующему игроку
            self.current_player = (self.current_player + 1) % self.max_players
            options.extend(self.__get_start_options_for_player(self.current_player))
        self.options.extend(options)
        return JackalBoardResponse(options, actions)

    def get_card(self, position: Vector2i):
        return next((card for card in self.cards if card.position == position), None)

    def get_possible_pirates_for_player(self, player_id):
        return (pirate.id for pirate in self.pirates if pirate.player_owner == player_id)

    def get_possible_options_for_pirate(self, pirate_id: str) -> [JackalOptionBase]:
        pirate: JackalPirate = next((pirate for pirate in self.pirates if pirate.id == pirate_id), None)
        if pirate is None:
            raise Exception("Cant find pirate with this id")
        card: JackalCardBase = self.get_card(pirate.position)
        if card is None:
            raise Exception(f"Cant find card for pirate on position {pirate.position}")
        return card.get_possible_options_for_pirate(pirate, self)

    def open_card(self, position: Vector2i) -> JackalActionsBase:
        # TODO: заменить на вероятностный алгоритм
        cars_cls_to_open = random.choice(self.stack)
        self.stack.remove(cars_cls_to_open)

        card: JackalCardBase = cars_cls_to_open(position)
        self.cards.append(card)
        return JackalActionOpenCard(
            frame=card.frame,
            rotation=card.rotation,
            open_position=position
        )

    def __create_start_stuff_for_player(self, player_id: int, direction: Vector2i) -> [JackalActionsBase]:
        position = direction * (self.SIZE + 1)
        actions: [JackalActionsBase] = []
        for _ in range(3):
            pirate = JackalPirate(position, player_id)
            self.pirates.append(pirate)
            actions.append(JackalActionSpawnPirate.from_pirate(pirate))
        ship = JackalShip(position, player_id)
        self.ships.append(ship)
        actions.append(JackalActionSpawnShip.from_ship(ship))
        return actions

    def __create_water(self):
        """
        Создает воду по краю карты
        :return:
        """
        for x in range(-self.SIZE - 2, self.SIZE + 3):
            for y in range(-self.SIZE - 2, self.SIZE + 3):
                if abs(x) > self.SIZE or abs(y) > self.SIZE:
                    self.cards.append(JackalCardWater(Vector2i(x, y)))

    def __get_start_options_for_player(self, player_id) -> [JackalOptionBase]:
        return [JackalOptionSelectPirate(
            for_player=player_id,
            pirate_id=pirate_id
        ) for pirate_id in self.get_possible_pirates_for_player(player_id)]

    def __fill_stack(self):
        for card_cls in self.STACK:
            self.stack.extend([card_cls for _ in range(card_cls.COUNT_IN_STACK)])


class JackalPirate:
    def __init__(self, position: Vector2i, player_owner: int, pirate_type: str = "simple"):
        self.pirate_type = pirate_type
        self.id = str(uuid.uuid4())
        self.position = position
        self.player_owner = player_owner


class JackalShip:
    def __init__(self, position: Vector2i, player_owner: int, moves_diagonal: bool = False, ship_type: str = "simple"):
        self.ship_type = ship_type
        self.id = str(uuid.uuid4())
        self.moves_diagonal = moves_diagonal
        self.player_owner = player_owner
        self.position = position


class JackalBoardResponse:
    def __init__(self, options: [], actions: []):
        self.options: [] = options
        self.actions: [] = actions
        self.event_type = "game_step"

    def for_player(self, for_player: int):
        return JackalBoardResponse(
            options=list(filter(lambda x: x.for_player in [-1, for_player, int(for_player)], self.options)),
            actions=list(filter(lambda x: x.for_player in [-1, for_player, int(for_player)], self.actions)),
        )
