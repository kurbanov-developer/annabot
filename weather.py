from yaweather import Russia, YaWeather
from num2t4ru import num2text

y = YaWeather(api_key='ecd214c0-fc73-4f2d-b470-578f7eb3ae3d')
res = y.forecast(Russia.Kazan, lang='ru_RU')

schedule = {
    'clear': 'ясно.',
    'partly-cloudy': 'малооблачно.',
    'cloudy': 'облачно с прояснениями.',
    'overcast': 'пасмурно.',
    'drizzle': 'морось.',
    'light-rain': 'небольшой дождь.',
    'rain': 'дождь.',
    'moderate-rain': 'умеренно сильный дождь.',
    'heavy-rain': 'сильный дождь.',
    'continuous-heavy-rain': 'длительный сильный дождь.',
    'showers': 'ливень.',
    'wet-snow': 'дождь со снегом.',
    'light-snow': 'небольшой снег.',
    'snow': 'снег.',
    'snow-showers': 'снегопад.',
    'hail': 'град.',
    'thunderstorm': 'гроза.',
    'thunderstorm-with-rain': 'дождь с грозой.',
    'thunderstorm-with-hail': 'гроза с градом.'
}

condition = res.fact.condition.replace(res.fact.condition, schedule[res.fact.condition])

