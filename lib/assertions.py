from requests import Response
import json

class Assertions:

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON dosen't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"
        # символ \ обозначает, что метод будет продолжен на другой строке


    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON dosen't have key '{name}'"

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
#этот метод делаем статическим, так как этот класс Assertions не является прямым наследником для тестов
#и чтобы использовать функции этого класса в тестах требуется либо каждый раз создавать объет Assertions
#и вызывать функции от объекта, либо сделать функцию статической
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON dosen't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message