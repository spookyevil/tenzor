import requests
import datetime
import time

# Функция для получения данных от API
def get_yandex_time():
    url = 'https://yandex.com/time/sync.json?geo=213'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            timestamp = data['time'] / 1000  # Преобразуем миллисекунды в секунды
            utc_offset = data['clocks']['213']['offset'] / 3600000  # Преобразуем миллисекунды смещения в часы
            city_name = data['clocks']['213']['name']
            return {
                'timestamp': timestamp,
                'utc_offset': utc_offset,
                'city_name': city_name
            }
        else:
            raise Exception(f'Запрос завершился неудачно. Код статуса: {response.status_code}')
    except Exception as e:
        return {'error': str(e)}

# Выполняем серию из пяти запросов
deltas = []
for i in range(5):
    # Фиксируем начальное время перед запросом
    start_time = time.time()

    # Получаем данные от API
    result = get_yandex_time()

    # Фиксируем время после получения ответа
    end_time = time.time()

    # Вычисляем дельту времени между началом и концом выполнения запроса
    request_duration = end_time - start_time
    deltas.append(request_duration)

    # Выводим результаты каждого запроса
    print(f"Запрос #{i+1}: Дельта времени выполнения запроса: {request_duration:.6f} секунд")

# Рассчитываем среднюю дельту времени
average_delta = sum(deltas) / len(deltas)

# Выводим среднюю дельту
print(f"Средняя дельта времени выполнения запроса: {average_delta:.6f} секунд")
