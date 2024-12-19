from infraestructure.mysql_connection import MySQLConnection
from infraestructure.repositories.user_repository import UserRepository
from infraestructure.repositories.menu_repository import MenuRepository
from infraestructure.repositories.order_repository import OrderRepository
from infraestructure.logs_utils import Logger
from models.user import User
import credentials_db
import bcrypt
import getpass


# Inicializar la conexión
conn = MySQLConnection(credentials_db.HOST, credentials_db.USER, credentials_db.PASSWORD, credentials_db.DATABASE)
menu_repository = MenuRepository(conn)

# Instanciar repositorios
user_repository = UserRepository(conn)
menu_repository = MenuRepository(conn)
order_repository = OrderRepository(conn)
logs_utils = Logger(conn)
# Menú principal
def menu_restaurante():
    while True:
        try:
            print("\n")
            print("1. Crear un menú")
            print("2. Ver todos los menús")
            print("3. Ver detalles de un menú")
            print("4. Editar un menú")
            print("5. Eliminar un menú")
            print("6. Realizar un pedido")
            print("7. Cancelar un pedido")
            print("8. Mostrar pedidos activos")
            print("9. Volver al menú principal")
            print("10. obtener menus de API")
            option = input("Ingrese una opción: ")
            if option == "1":
                menu = menu_repository.get_menu_input() 
                menu_repository.create_menu(menu)
                print("Menú creado con éxito")
            elif option == "2":
                menu_repository.all_menus_info()
            elif option == "3":
                menu_id = int(input("Ingrese el ID del menú: "))
                menu = menu_repository.get_menu_by_id(menu_id)
                if menu:
                    print(f"Menú encontrado: \nNombre: {menu.get_name()}\nDescripción: {menu.get_description()}\nPrecio: {menu.get_price()}\nDisponibilidad: {menu.get_availability()}")
                else:
                    print("Menú no encontrado.")
            elif option == "4":
                menu_repository.all_menus_info()
                menu = menu_repository.get_menu_input_for_editing()
                menu_repository.update_menu(menu)
                print("Menú editado correctamente")
            elif option == "5":
                menu_repository.all_menus_info()
                menu_id = int(input("Ingrese el ID del menú que desea eliminar: "))
                menu_repository.delete_menu(menu_id)
                print("Menú eliminado correctamente")
            elif option == "6":
                menu_repository.all_menus_info()
                try:
                    menu_id = int(input("Ingrese el ID del menú que desea ordenar: "))
                    if not menu_repository.is_menu_available(menu_id):
                        print("Menú no disponible")
                    else:
                        name = input("Ingrese el nombre del usuario: ")
                        password = getpass.getpass("Ingrese la contraseña del usuario: ")
                        user = user_repository.login_user(name, password)
                        if user:
                            menu = menu_repository.get_menu_by_id(menu_id)
                            order_repository.place_order(menu, user)
                        else:
                            print("Usuario o contraseña inválidos")
                except Exception as e:
                    print(f"Ha ocurrido un error: {e}")
                    logs_utils.register_log(f"Error: {e}")
            elif option == "7":
                order_repository.show_orders()
                order_id = int(input("Ingrese el ID del pedido a cancelar: "))
                menu_id = int(input("Ingrese el ID del menú asociado al pedido: "))
                menu = menu_repository.get_menu_by_id(menu_id)
                order_repository.cancel_order(order_id, menu)
            elif option == "8":
                order_repository.show_orders()
            elif option == "9":
                print("Volviendo al menú principal\n")
                return
            elif option == "10":
                menu_repository.fetch_menus_from_api()
            else:
                print("Debe ingresar una opción válida entre 1 y 9")
        except ValueError as e:
            print(f"Error: {e}")
            logs_utils.register_log(f"Error: {e}")

# Menú para gestionar usuarios
while True:
    print("HELLO, AND WELCOME TO LOS POLLOS HERMANOS FAMILY")
    print("1. Registrar un usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    option = input("Ingrese su opción: ")
    if option == "1":
        try:
            name = input("Ingrese el nombre del usuario: ").strip()
            password = getpass.getpass("Ingrese la contraseña del usuario: ").strip()
            if not name or not password:
                print("Error: Nombre o contraseña no pueden estar vacíos.")
            else:
                user = User()
                user.set_name(name)
                user.set_password(password)
                user_repository.create_user(user)
                print("Usuario registrado exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")
    elif option == "2":
        name = input("Ingrese el nombre del usuario: ")
        password = input("Ingrese la contraseña del usuario: ")
        result = user_repository.login_user(name, password)
        if result:
            print(f"Bienvenido a la tienda {result.get_name()}!")
            menu_restaurante()
        else:
            print("El usuario o contraseña son inválidos.")
    elif option == "3":
        print("El programa se ha cerrado correctamente")
        break
    else:
        print("Debe ingresar una opción válida entre 1 y 3")
        

