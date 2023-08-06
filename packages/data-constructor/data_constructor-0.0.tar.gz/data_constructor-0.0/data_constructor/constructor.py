import os, random, data_constructor.reader

class data():
    name = (random.choice('abcdefghijklmnopqrstuvwxyz') + str(random.randint(12354676678, 67867867867861380439758)) + random.choice('abcdefghijklmnopqrstuvwxyz') + random.choice('abcdefghijklmnopqrstuvwxyz'))
    version = '1.2'
    description = '''
        1. изменены названия команд в консоли 
        2. теперь после окончания работы программы ваши введённые 
    данные сохранятся и вам выдадут айди данных. по этому айди можно восстановить данные
        3. теперь есть инсталлер (установщик)
        4. конструктор русифицирован
    '''
    str = 'example'
    int = int(123)
    float = float(12.3)
    if not os.path.isdir('old'):
        os.mkdir('old')
    os.chdir('old')
    f = open(name, 'w')
    ids = open('ID.txt', 'a')

    def __init__(self):
        self.str = str('')
        self.int = int(0)
        self.float = float(0)

    def addData(self, str_data, int_data, float_data):
        self.str = str(str_data)
        self.int = int(int_data)
        self.float = float(float_data)

    def getStr(self):
        return self.str

    def getInt(self):
        return self.int

    def getFloat(self):
        return self.float

    def getAll(self):
        data = []
        data.clear()
        data.append(self.str)
        data.append(self.int)
        data.append(self.float)
        return data

    def __version__(self, show_description = False):
        pr =  ('ваша версия конструктора данных: ' + self.version)

        if show_description == True:
            pr = pr + '\n описание обновления' + self.description
        return pr


    def __del__(self):
        self.f.write('str: ' + self.str + ' int: ' + str(self.int) + ' float: ' + str(self.float))
        self.ids.write('\n' + self.name)
        print('ваш ID данных: ' + self.name)
        print('конструктор остановлен')

    def addStrData(self, data):
        self.str = data

    def addIntData(self, data):
        self.int = data

    def addFloatData(self, data):
        self.float = data

    def openData(self, id):
        data_constructor.reader.reader(id)

