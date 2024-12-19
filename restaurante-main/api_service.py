import requests

class ApiService:
    BASE_URL = "https://poo.nsideas.cl/api/menus"

    @staticmethod
    def get_all_menus():
        response = requests.get(ApiService.BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error al obtener datos de la API externa")

    @staticmethod
    def get_menu_details(menu_id):
        response = requests.get(f"{ApiService.BASE_URL}/{menu_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error al obtener datos de la API externa")

        