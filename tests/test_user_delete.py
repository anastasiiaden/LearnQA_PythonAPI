from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserDelete(BaseCase):
#Первый - на попытку удалить пользователя по ID 2.
    def test_delete_user_id2(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        #LOGIN
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        #DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

#Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться,
# что пользователь действительно удален.
    def test_delete_just_created_user(self):
        #REGISTR
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found", f"Unexpected response content {response4.content}"

#Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_as_another_user(self):
        #REGISTER USER 1
        register_data_1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data_1['email']
        password = register_data_1['password']

        #REGISTER USER 2
        register_data_2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data_2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id_2 = self.get_json_value(response2, "id")

        #LOGIN USER 1
        login_data_1 = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=login_data_1)
        auth_sid_1 = self.get_cookie(response3, "auth_sid")
        token_1 = self.get_header(response3, "x-csrf-token")

        #DELETE USER 2
        response4 = MyRequests.delete(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token_1},
            cookies={"auth_sid": auth_sid_1}
        )
        Assertions.assert_code_status(response4, 200)

        #GET USER 2
        response5 = MyRequests.get(f"/user/{user_id_2}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")
