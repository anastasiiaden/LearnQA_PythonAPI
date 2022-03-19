import requests

class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print("Cookie: ",  response.cookies)

        cookies_name = "HomeWork"
        cookies_value = "hw_value"

        assert cookies_name in response.cookies, "Cookie is wrong"
        assert cookies_value in response.cookies["HomeWork"], "Value cookie is wrong"