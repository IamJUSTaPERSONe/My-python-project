"""Автоматически создает и перестраивает список с заданными значениями от пользователя"""
class Generation:
    def __init__(self, count, last_value ):
        if count <= 0:
            raise ValueError('Количество должно быть положительным числом')
        if last_value < count:
            raise ValueError('Последнее число списка должно быть больше количества')
        self._count = count
        self._last_value = last_value
        self._array = self._generate_array()

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if value <= 0:
            raise ValueError('Ошибка ввода: значение меньше или равно нулю')
        if value > self._last_value:
            raise  ValueError('Ошибка ввода')
        self._count = value
        self._array = self._generate_array()

    @property
    def last_value(self):
        return self._last_value

    @last_value.setter
    def last_value(self, value):
        if value < self.count:
            raise ValueError('Ошибка ввода: значение не может быть меньше количества')
        self._last_value = value
        self._array = self._generate_array()

    @property
    def array(self):
        return self._array

    def _generate_array(self):
        if self.count == 0:
            return []
        start = self.last_value - self.count + 1
        return list(range(start, self.last_value + 1))

# Проверка
gen = Generation(1,4)
print(gen.array)

# Изменяем свойство, массив перестраивается
gen.count = 4
print(gen.array)

# Изменяем последнее число
gen.last_value = 7
print(gen.array)