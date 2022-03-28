from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import pytest
import random
import string

class TestUserRegister(BaseCase):
    def test_creat_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    # Создание пользователя без указания одного из полей -
    # с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    reg_params = [
        ("email"),
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName")
    ]

    @pytest.mark.parametrize('condition', reg_params)
    def test_create_user_without_params(self, condition):
        data = self.prepare_registration_data()
        data.pop(condition)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {condition}", f"Unexpected response content {response.content}"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_firstName(self):
        data = self.prepare_registration_data()
        data.update({'firstName': 'f'})
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_firstName(self):
        data = self.prepare_registration_data()
        firstName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=251))
        data.update({'firstName': firstName})
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"

# python -m pytest -s tests/test_user_register.py
# ключ -s требуется, чтобы не были проигнорированы выводы не относящиеся к pytest
# python -m pytest -s tests/test_user_register.py -k test_creat_user_successfully
