from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response, "id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        ) #авторизованный get на получение данных

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

# Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_not_authorized_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        #EDIT
        new_name = "Changed name"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Auth token not supplied", f"Unexpected response content {response2.content}"


# Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_by_another_user(self):
        #REGISTER USER  1
        register_data_1 = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=register_data_1)
        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")
        email_1 = register_data_1['email']
        password_1 = register_data_1['password']

        #REGISTER USER 2
        register_data_2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data_2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        email_2 = register_data_2['email']
        password_2 = register_data_2['password']
        first_name_2 = register_data_2['firstName']
        user_id_2 = self.get_json_value(response2, "id")

        #LOGIN USER 1
        login_data_1 = {
            'email': email_1,
            'password': password_1
        }
        response3 = MyRequests.post("/user/login", data=login_data_1)
        auth_sid_1 = self.get_cookie(response3, "auth_sid")
        token_1 = self.get_header(response3, "x-csrf-token")

        #EDIT USER 2
        new_name = "Changed name"
        response4 = MyRequests.put(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token_1},
            cookies={"auth_sid": auth_sid_1},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4, 200)

        #LOGIN USER 2
        login_data2 = {
            'email': email_2,
            'password': password_2
        }
        response5 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        #GET USER 2
        response6 = MyRequests.get(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2}
        )
        Assertions.assert_json_value_by_name(response6, "firstName", first_name_2, "The name was changed.")


# Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_with_invalid_email(self):
        #REGISTER
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

        #EDIT
        new_email = "learnqaexample.com"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response3.content}"

# Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_with_short_firstname(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")
        firstname = register_data['firstName']

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "f"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response4, "firstName", firstname, "The name was wrongly changed.")
