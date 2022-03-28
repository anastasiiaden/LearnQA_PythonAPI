import requests
from lib.logger import Logger
import allure
from environment import ENV_OBJECT

class MyRequests(): #центральный метод send статический т.к. класс является вспомогательным и создавать объекты этого класса нет необходимоти
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url}'"): #конструкция with это менеджер контекста, которая позволяет использовать теги allure внутри функций, а не как декораторы
            return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, headers, cookies, "DELETE")



    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
#в python нет приватных функций и чтобы обозначить, что функция должна использоваться только внутри класса ставиться _
#это означает, что метод вспомогательный и не должен вызываться из вне

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        Logger.add_request(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was reseived")

        Logger.add_response(response)

        return response


#python -m pytest --alluredir=test_results/ tests/test_user_auth.py
