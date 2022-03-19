from requests import Response
import json.decoder

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
#этот метод делаем статическим, так как этот класс Assertions не является прямым наследником для тестов
#и чтобы использовать функции этого класса в тестах требуется либо каждый раз создавать объет Assertions
#и вызывать функции от объекта, либо сделать функцию статической
        try:
            response_as_dict = response.json()
        except json.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

            assert name in response_as_dict, f"Response JSON dosen't have key '{name}'"
            assert response_as_dict[name] == expected_value, error_messsage