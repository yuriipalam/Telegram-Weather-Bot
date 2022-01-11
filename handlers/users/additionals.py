weather_smiles = {
    '01d': '\U00002600',  # clear sky
    '01n': '\U0001F319',
    '02d': '\U000026C5',  # few clouds
    '02n': '\U00002601',
    '03d': '\U00002601',  # scattered clouds
    '03n': '\U00002601',
    '04d': '\U0001F324',  # broken clouds
    '04n': '\U00002601',
    '09d': '\U0001F327',  # shower rain
    '09n': '\U0001F327',
    '10d': '\U0001F326',  # rain
    '10n': '\U0001F327',
    '11d': '\U000026C8',  # thunderstorm
    '11n': '\U000026C8',
    '13d': '\U00002744',  # snow
    '13n': '\U00002744',
    '50d': '\U0001F32B',  # mist
    '50n': '\U0001F32B'
}

monthes = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря"
}

class Orphography:
    @staticmethod
    def end_of_words(n):
        es = ['а', 'ы', '']
        n = n % 100
        if 11 <= n <= 19:
            return es[2]
        else:
            i = n % 10
            if i == 1:
                return es[0]
            elif i in [2, 3, 4]:
                return es[1]
            else:
                return es[2]

    @staticmethod
    def end_of_numbers(n):
        false_numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
        if n in false_numbers:
            return n.replace('0', '')
        return n
