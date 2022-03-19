import requests

class TestHeader:
    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print("Header: ",  response.headers)

        header_name = "x-secret-homework-header"
        header_value = "Some secret value"

        assert header_name in response.headers, "The header is wrong"
        assert header_value in response.headers["x-secret-homework-header"], "The header value is wrong"