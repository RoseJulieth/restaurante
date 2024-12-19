import requests
from models.menu import Menu
from infraestructure.logs_utils import Logger
from infraestructure.connection import Connection

class MenuRepository:
    def __init__(self, conn: Connection):
        self.__conn = conn
        self.logger = Logger(conn)

    def create_menu_from_api(self, menu_data: dict) -> Menu:
        menu = Menu()
        menu.set_id(menu_data.get("id", -1))
        menu.set_name(menu_data.get("name", ""))
        menu.set_description(menu_data.get("description", ""))
        menu.set_price(menu_data.get("price", 0.0))
        menu.set_availability(menu_data.get("availability", True))
        return menu

    def fetch_menus_from_api(self):
        api_url = "https://poo.nsideas.cl/api/menus"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                menus = response.json()
                for menu_data in menus:
                    menu = self.create_menu_from_api(menu_data)
                    self.create_menu(menu)
                return "Menús sincronizados con éxito."
            else:
                return f"Error al obtener menús de la API. Código de estado: {response.status_code}"
        except Exception as e:
            self.logger.register_log(f"Error al conectar con la API: {e}")
            return f"Error de conexión: {e}"
    def all_menus_info(self):
        sql = """
            SELECT * FROM menus
        """
        self.__conn.execute(sql)
        result = self.__conn.fetchall()
        print(result)     

    def create_menu(self, menu: Menu):
        try:
            sql = """
            INSERT INTO menus (name, description, price, availability)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=%s, description=%s, price=%s, availability=%s
            """
            self.__conn.execute(sql, (
                menu.get_name(),
                menu.get_description(),
                menu.get_price(),
                menu.get_availability()
                ))
            self.__conn.commit()
        except Exception as e:
            self.logger.register_log(f"Error al crear menú en la base de datos: {e}")
