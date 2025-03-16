import requests
import datetime

def get_yandex_time():
    url = 'https://yandex.com/time/sync.json?geo=213'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            timestamp = data['time'] / 1000  # Преобразуем миллисекунды в секунды
            utc = data["clocks"]["213"]["offsetString"]
            
            # Преобразуем Unix timestamp в человекопонятный формат
            time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                'Время': time,
                'Часовой пояс': utc
            }
        
        else:
            raise Exception(f'Запрос завершился неудачно. Код статуса: {response.status_code}')
    
    except Exception as e:
        return {'error': str(e)}

result = get_yandex_time()
print(result)
