class Menu:
    def __init__(self) -> None:
        self.__id: int = -1
        self.__name: str = ""
        self.__description: str = ""
        self.__price: float = 0.0
        self.__availability: bool = True

    def get_id(self) -> int:
        return self.__id

    def set_id(self, id: int):
        self.__id = id

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_description(self) -> str:
        return self.__description

    def set_description(self, description: str):
        self.__description = description

    def get_price(self) -> float:
        return self.__price

    def set_price(self, price: float):
        self.__price = price

    def get_availability(self) -> bool:
        return self.__availability

    def set_availability(self, availability: bool):
        self.__availability = availability

    # Método estático para deserializar JSON a un objeto Menu
    @staticmethod
    def from_json(data: dict) -> 'Menu':
        menu = Menu()
        menu.set_id(data.get("id", -1))
        menu.set_name(data.get("name", ""))
        menu.set_description(data.get("description", ""))
        menu.set_price(data.get("price", 0.0))
        menu.set_availability(data.get("availability", True))
        return menu
