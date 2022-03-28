import os

class Environment:
    DEV = "dev"
    PROD = "prod"

    URLS = {
        DEV: "https://playground.learnqa.ru/api_dev",
        PROD: "https://playground.learnqa.ru/api"
    }
    def __init__(self):
        try:
            self.env = os.environ['ENV'] #если удалось прочитать переменную окружения(значит она выставлена), то положим значение этой переменной окружения
        except KeyError:
            self.env = self.DEV #то зададим дефолное значение

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}")

#создаём объект класса env
ENV_OBJECT = Environment()


#export MY_VAR="123" установить переменную окружения для linux и macOS
#set MY_VAR="123" # установить перемменную окружения для windows
#echo %ENV% проверить установленное значение