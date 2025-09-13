import math


def half_interval(a, b):
    # Находим середину интервала
    return (a + b) / 2

def get_int():
    # Получаем данные от пользователя
    a, b, e = int(input("Точка а: ")), int(input("Точка b: ")), float(input("Точность: "))
    return a, b, e

def function(x):
    # Вычисляется значение функции
    return x ** 3 - 2 * x ** 2 - 4 * x + 7


def start():
    # Запрос данных
    a, b, e = get_int()
    counter = 0
    max_counter = 100

    # Находим значения функций
    fa = function(a)
    fb = function(b)
    print(f'f({a}) = {fa}, f({b}) = {fb}')

    if fa * fb > 0:
        print('Функция не меняет знак на интервали. Возможно корней нет')

    while abs(b - a) > e:
        counter += 1
        if counter >= max_counter:
            print('Шагов более 100. Конец подсчета')
            break

        # Находим середину отрезка
        c = half_interval(a, b)
        print('seredina',c)
        fc = function(c)
        print('func ot seredina',fc)

        if fc < 0:
            a = c
        else:
            b = c
    print(f'Значение корня (x_{counter}): {c}')
    print(f'Значение функции: {function(c)}')

start()
