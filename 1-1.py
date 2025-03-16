import requests

# Указываем URL ресурса
url = 'https://yandex.com/time/sync.json?geo=213'

# Выполняем GET-запрос
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    # Выводим сырой ответ
    print(response.text)
else:
    print(f'Ошибка: {response.status_code}')