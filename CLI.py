class CL_Interface():
    def __init__(self, lang, playername):
        if lang == 'RU':
            self.text = {
                "sleep_text": 'Приложение не продолжит работу.',

                "read_settings": {
                    "finish": 'Найден файл Settings.json.',
                },

                "api_connect": {
                    "start": 'Попытка подключится к API.',
                    "error": 'Не удалось подключится к API, проверьте devid и authkey',
                    "error_value": 'Не удалось подключится к API, devid должен быть целым числом',
                    "finish": 'Успешно подключились к API.'
                },

                "searching_player": {
                    "start": f'Поиск игрока {playername}.',
                    "error": 'Не удалось найти игрока.',
                    "finish": 'Успешно найден игрок.',
                },

                "rich_presence_connect": {
                    "start": 'Попытка подключится к приложению discord',
                    "error": 'Не удалось подключится к приложению discord',
                    "finish": 'Успешное подключение к приложению discord',
                },

                "ActivePhase": {
                    "working_for": 'Приложение запущено уже',
                    "logged_as": 'Следим за игроком',
                    "in_lobby": 'В лобби, Paladins запущенны примерно',
                    "choosing_champion": 'Выбор чемпиона, Paladins запущены примерно',
                    "playing_as": 'В матче за',
                    "on_map": 'на карте',
                    "offline": 'Оффлайн в Paladins',
                    "total_hours": 'всего часов',
                    "level": 'уровень',
                    "rank": 'в рейтинговом режиме',
                }
            }
        #DEFAULT IS ENGLISH
        else:
            self.text = {
                "sleep_text": 'App will not continue work.',

                "read_settings": {
                    "finish": 'Settings.json is exist.',
                },

                "api_connect": {
                    "start": 'Trying to access API.',
                    "error": 'Fault to access API, check your devid and authkey',
                    "error_value": 'Fault to access API, devid should be integer',
                    "finish": 'Successfully get access to API.'
                },

                "searching_player": {
                    "start": f'Searching player {playername}.',
                    "error": 'Unable to find player.',
                    "finish": 'Sucessfully found player.',
                },

                "rich_presence_connect": {
                    "start": 'Trying to connect discord app',
                    "error": 'Fault to connect discord app',
                    "finish": 'Sucessfully connected to discord app',
                },

                "ActivePhase": {
                    "working_for": 'Working for',
                    "logged_as": 'Logged as',
                    "in_lobby": 'In lobby, Paladins launched for',
                    "choosing_champion": 'Choosing champion, Paladins launched for',
                    "playing_as": 'Playing as',
                    "on_map": 'on map',
                    "offline": 'Offline in Paladins',
                    "total_hours": 'total hours',
                    "level": 'level',
                    "rank": 'in ranked',
                }
            }
        self.ActivePhase = False
        self.Lines = 8


    def messaging(self, step, job, result):
        print(f'[{step}/4] {self.text[job][result]}')

    def print_cli(self, status, namespaces=None):
        self.ActivePhase = True
        line0 = f"░ Paladins Rich Presence by ValfyNico"
        line1 = f"░ {self.text['ActivePhase']['working_for']} {namespaces['time_rich_presence']}"
        line2 = f"░ {self.text['ActivePhase']['logged_as']} {namespaces['player']}"
        line_clean = f"░ "

        if status == 1:
            line4 = f"░ {self.text['ActivePhase']['in_lobby']} {namespaces['time']}"
        elif status == 2:
            line4 = f"░ {self.text['ActivePhase']['choosing_champion']} {namespaces['time']}"
        elif status == 3:
            line4 = f"░ {self.text['ActivePhase']['playing_as']} {namespaces['champion']} {self.text['ActivePhase']['on_map']} {namespaces['map']}"
        else:
            line4 = f"░ {self.text['ActivePhase']['offline']}"

        if namespaces:
            line3 = f"░ {namespaces['total_hours']} {self.text['ActivePhase']['total_hours']}," \
                    f" {namespaces['account_level']} {self.text['ActivePhase']['level']}," \
                    f" {namespaces['rank']} {self.text['ActivePhase']['rank']}"
            if namespaces['title']:
                line2 = f"░ {self.text['ActivePhase']['logged_as']} {namespaces['player']}, {namespaces['title']}"
        else:
            line3 = line_clean

        lineslen = max(len(line0), len(line1), len(line2), len(line3), len(line4))
        line0 += " " * (lineslen - len(line0) + 1)
        line1 += " " * (lineslen - len(line1) + 1)
        line2 += " " * (lineslen - len(line2) + 1)
        line3 += " " * (lineslen - len(line3) + 1)
        line4 += " " * (lineslen - len(line4) + 1)
        line_clean += " " * (lineslen - len(line_clean) + 1)
        line_edge = "░" * (lineslen + 2)

        print(line_edge)
        print(line0, end="░\n")
        print(line1, end="░\n")
        print(line_clean, end="░\n")
        print(line2, end="░\n")
        print(line3, end="░\n")
        print(line4, end="░\n")
        print(line_edge)
