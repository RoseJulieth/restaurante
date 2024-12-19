class Order:
    def __init__(self) -> None:
        self.__order_id: int = -1
        self.__user: object = None 
        self.__menu: object = None
    
    def get_order_id(self) -> int:
        return self.__order_id
    
    def set_order_id(self, order_id: int):
        self.__order_id = order_id

    def get_user(self) -> object:
        return self.__user
    
    def set_user(self, user: object):
        self.__user = user

    def get_menu(self) -> object:
        return self.__menu
    
    def set_menu(self, menu: object):
        self.__menu = menu
