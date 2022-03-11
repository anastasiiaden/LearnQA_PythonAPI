import requests
import json
import time


#1.создание задачи
url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
token = json.loads(response.text)["token"]
token1 = 'AO0oTM0oTOxASMx0yMw0iMyAjMq' #для проверки ошибок
print("token: ", token)
time_response = json.loads(response.text)["seconds"]
print("time: ", time_response)
payload = {"token": f"{token}"}
payload1 = {"token": f"{token1}"} #для проверки ошибок
#2.Один запрос с token ДО того, как задача готова, убеждался в правильности поля status
print("Запрос ДО")
response2 = requests.get(url, params=payload)
if "status" in json.loads(response2.text):
    if json.loads(response2.text)["status"] == 'Job is NOT ready':
        print("status: ", json.loads(response2.text)["status"])
        #3.ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
        time.sleep(time_response)
        #4.делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
        print("Запрос ПОСЛЕ")
        response3 = requests.get(url, params=payload)
        if "status" in json.loads(response3.text):
            if json.loads(response3.text)["status"] == 'Job is ready' and json.loads(response3.text)["result"] != 0:
                print("status: ", json.loads(response3.text)["status"])
                print("result: ", json.loads(response3.text)["result"])
        elif "error" in json.loads(response3.text):
            print("error: ", json.loads(response3.text)["error"])
elif "error" in json.loads(response2.text):
    print("error: ", json.loads(response2.text)["error"])


