from infraestructure.connection import Connection
from models.menu import Menu
from models.user import User
from models.order import Order

class OrderRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def place_order(self, menu: Menu, user: User) -> Order:
        if self.is_menu_available(menu.get_id()):
            try:
                sql = "INSERT INTO orders (user_id, user_name, menu_id, menu_name) VALUES (%s, %s, %s, %s)"
                self.__conn.execute(sql, (
                    user.get_id(),
                    user.get_name(),
                    menu.get_id(),
                    menu.get_name()
                ))
                self.__conn.commit()

                sql_update = "UPDATE menus SET availability = 0 WHERE menu_id = %s"
                self.__conn.execute(sql_update, (menu.get_id(),))
                self.__conn.commit()

                print(f"Orden realizada con éxito. Usuario: {user.get_name()}, Menú: {menu.get_name()}")
                order = Order()
                order.set_user(user)
                order.set_menu(menu)
                return order
            except Exception as e:
                print(f"Error al procesar la orden: {e}")
                return None
        else:
            print("El menú no está disponible.")
            return None

    def is_menu_available(self, menu_id: int) -> bool:
        sql = "SELECT availability FROM menus WHERE menu_id = %s"
        self.__conn.execute(sql, (menu_id,))
        result = self.__conn.fetchone()
        return result and result[0] == 1

    def cancel_order(self, order_id: int, menu: Menu):
        try:
            sql_check = "SELECT * FROM orders WHERE order_id = %s AND menu_id = %s"
            self.__conn.execute(sql_check, (order_id, menu.get_id()))
            result = self.__conn.fetchone()

            if not result:
                print("La orden no existe o los datos no coinciden.")
                return

            sql = "DELETE FROM orders WHERE order_id = %s AND menu_id = %s"
            self.__conn.execute(sql, (order_id, menu.get_id()))
            self.__conn.commit()

            sql_update = "UPDATE menus SET availability = 1 WHERE menu_id = %s"
            self.__conn.execute(sql_update, (menu.get_id(),))
            self.__conn.commit()

            print(f"El menú '{menu.get_name()}' ha sido cancelado y está disponible nuevamente.")
        except Exception as e:
            print(f"Error al cancelar la orden: {e}")

    def show_orders(self):
        sql = "SELECT order_id, user_name, user_id, menu_name, menu_id FROM orders"
        self.__conn.execute(sql)
        results = self.__conn.fetchall()

        if not results:
            print("No hay órdenes activas.")
        else:
            for order in results:
                print(f"ID de Orden: {order[0]}, Usuario: {order[1]}, ID de Usuario: {order[2]}, Menú: {order[3]}, ID de Menú: {order[4]}")
