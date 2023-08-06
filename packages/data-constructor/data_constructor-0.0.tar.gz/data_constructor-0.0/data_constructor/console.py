from data_constructor.constructor import data
constructor = data()


class console:
    commands = ['ad', 'asd', 'afd', 'aid', 'gd', 'version', 'des', 'help', 'stop', 'open']


    def __del__(self):
        print('консоль остановленна')

    def start(self):
        print('Напишите help чтобы увидеть список команд')
        print('--------------------консоль--------------------')
        while True:
            command = str(input('constructor_console $~:'))
            print('command \"' + command +  '\"')

            if command == 'stop':
                quit()

            if command == 'ad':
                strData = str(input('какие текстовые даннные вы хотите добавить? :'))
                intData = int(input('какие числовые даннные вы хотите добавить? :'))
                floatData = float(input('какие дробные числовые даннные вы хотите добавить? :'))
                constructor.addData(strData, intData, floatData)
                print('добавленно!')

            if command == 'gd':
                data = constructor.getAll()
                for i in data:
                    print(i)

            if command == 'asd':
                strData = str(input('какие текстовые даннные вы хотите добавить? :'))
                constructor.addStrData(strData)

            if command == 'aid':
                intData = str(input('какие числовые даннные вы хотите добавить? :'))
                constructor.addIntData(intData)

            if command == 'afd':
                floatData = str(input('какие дробные числовые даннные вы хотите добавить? :'))
                constructor.addFloatData(floatData)

            if command == 'version':
                print(constructor.version)

            if command == 'des':
                print(constructor.description)

            if command == 'help':
                print('\n'
                      '             ПОМОЩЬ\n'
                      'ad: добавить данные\n'
                      'asd: добавить данные в текстовом формате(str)\n'
                      'aid: добавить данные в формате числа(int)\n'
                      'afd: добавить данные в формате дробного числа(float)\n'
                      'gd: просмотреть все данные\n'
                      'version: показать версию конструктора\n'
                      'des: показывает данные об текущем обновлении\n'
                      'help: показывает это сообщение\n'
                      'stop: остонавливает консоль\n'
                      'open: показывает данные по их ID\n'
                      'если вы утеряли ID данных вы можете посмотреть его в файле id.txt из папки old (последний айди '
                      'записывается в конце)\n '
                      '                ')
            if command not in self.commands:
                print('неизвестная команда. Напишите help чтобы увидеть список команд')

            if command == "open":
                id = str(input('пожалуйста, напишите ID ваших данных: '))
                try:
                    constructor.openData(id)
                except FileNotFoundError:
                    print('ОШИБКА:\nданные не найдены')
