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

# Запуск основного процесса
if __name__ == "__main__":
    # Фиксируем начальное время перед запросом
    start_time = time.time()  # Текущее время в секундах

    # Получаем данные от API
    result = get_yandex_time()

    # Фиксируем время после получения ответа
    end_time = time.time()

    # Вычисляем дельту времени между началом и концом выполнения запроса
    request_duration = end_time - start_time

    # Преобразуем время из результата API в удобный формат
    server_time_utc = datetime.datetime.utcfromtimestamp(result['timestamp'])
    server_time_local = server_time_utc + datetime.timedelta(hours=result['utc_offset'])  # Учитываем часовой пояс

    # Выводим результаты
    print(f"Начальное время: {start_time:.6f} секунд")
    print(f"Конечное время: {end_time:.6f} секунд")
    print(f"Дельта времени выполнения запроса: {request_duration:.6f} секунд")
    print(f"Серверное время (UTC): {server_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Серверное время (местное): {server_time_local.strftime('%Y-%m-%d %H:%M:%S')} ({result['city_name']})")
