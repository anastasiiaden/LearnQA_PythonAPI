from requests import Response  # чтобы использовать функцию Response
import json.decoder
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find headers with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError: #чтобы упало с понятной нам ошибкой
            assert False, f"Response is not in JSON format. Response text is '{response.text}' " #убедиться, что ответ пришёл в формате json
        #если парсинг прошёл успешно
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None): #у передаваемого параметра email установлено дефолтное значение None и следовательно его можно не передавать
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%y%H%M%S")
            email = f"{base_part}{random_part}@{domain}" #переменная указывается через self, чтобы быть доступной в других фунциях и тестах
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }