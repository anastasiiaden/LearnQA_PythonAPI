import requests

URL = "https://playground.learnqa.ru/api/compare_query_type"

#1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response1 = requests.get(URL)
print("1. ", response1.text, response1.status_code)

#2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response2 = requests.head(URL)
print("2. ", response2.text, response2.status_code)

#3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
payload3 = {"method": "POST"}
response3 = requests.post(URL, data=payload3)
print("3. ", response3.text, response3.status_code)

#4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для всех типов запроса.
# Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок.

print("4. ")
methods = ["GET", "POST", "PUT", "DELETE"]
for i in methods:
    payload4 = {"method": i}
    ok = '{"success":"!"}'
    wrong = 'Wrong method provided'
    print(i)

    response_get = requests.get(URL, params=payload4)
    if (response_get.text == ok and i == methods[0]) or (response_get.text == wrong and i != methods[0]):
        print(" GET: ", response_get.text, " - Сервер отвечает верно")
    else:
        print(" GET: ", response_get.text, " - Сервер отвечает НЕ верно")

    response_post = requests.post(URL, data=payload4)
    if (response_post.text == ok and i == methods[1]) or (response_post.text == wrong and i != methods[1]):
        print(" POST: ", response_post.text, " - Сервер отвечает верно")
    else:
        print(" POST: ", response_post.text, " - Сервер отвечает НЕ верно")

    response_put = requests.put(URL, data=payload4)
    if (response_put.text == ok and i == methods[2]) or (response_put.text == wrong and i != methods[2]):
        print(" PUT: ", response_put.text, " - Сервер отвечает верно")
    else:
        print(" PUT: ", response_put.text, " - Сервер отвечает НЕ верно")

    response_delete = requests.delete(URL, data=payload4)
    if (response_delete.text == ok and i == methods[3]) or (response_delete.text == wrong and i != methods[3]):
        print(" DELETE: ", response_delete.text, " - Сервер отвечает верно")
    else:
        print(" DELETE: ", response_delete.text, " - Сервер отвечает НЕ верно")


