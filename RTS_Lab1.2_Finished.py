# Лабораторна робота №2
# Серебряков Роман, ІО-71
# Варіант №22
# Число гармонік в сигналі n = 10
# Гранична частота, Wгр = 1200
# Кількість дискретних відліків, N = 64
# Додаткове завдання №1 - графіки залежності часу обчислення Rxx і Rxy від N (NTICKS)

from random import uniform
from math import sin
import matplotlib.pyplot as plt
import datetime
import numpy as np

NHARMONIC = 10
LIMFREQ = 1200
NTICKS = 64


def correlate_old(x_list, y_list):
    r_list = [0 for i in range(len(x_list))]
    Mx, My = get_M(x_list), get_M(y_list)
    for t in range(len(x_list)):
        r_list[t] = sum((x_list[i] - Mx)*(y_list[i + t] - My) for i in range(len(x_list) - t))/(len(x_list) - 1)
    return r_list


def correalte_real(x_list, y_list):
    Mx, My = get_M(x_list), get_M(y_list)
    for t in range(len(x_list)):
        yield sum((x_list[i] - Mx)*(y_list[i + t] - My) for i in range(len(x_list) - t))/(len(x_list) - 1)


def correlate(x_list, y_list):
    R = [0] * (len(x_list) // 2)
    Mx, My = get_M(x_list), get_M(y_list)

    for t in range(len(x_list) // 2 - 1):
        #R[t] = 0
        for i in range(len(x_list) // 2 - 1):
            R[t] += (x_list[i] - Mx) * (y_list[i + t] - My)
        R[t] /= (len(x_list) - 1)

    return R


def do_plot(a_list):
    plt.plot([i for i in range(len(a_list))], a_list)
    plt.axis([0, len(a_list), min(a_list), max(a_list)])
    plt.show()



def getharm(t):
    x = 0
    for i in range(NHARMONIC):
        x += uniform(0, 1) * sin(LIMFREQ * (i / NHARMONIC) * t + uniform(0, 1))
    return x


def get_x_list(LEN):
    return [getharm(i) for i in range(LEN)]


def get_D(x_list, M_x):
    return sum((x_list[t] - M_x)**2 for t in range(len(x_list))) / (len(x_list) - 1)


def get_M(x_list):
    return sum(x_list) / len(x_list)




# Додаткове завдання №1 - графіки залежності часу обчислення Rxx і Rxy від N (NTICKS)
array_sizes = [N for N in range(NTICKS // 4, NTICKS * 4, 32)]
Rxx_times = []
Rxy_times = []
for N in array_sizes:
    x_list = get_x_list(N)
    y_list = get_x_list(N)

    Rxy_time = datetime.datetime.now()
    correlate(x_list, y_list)
    delta = datetime.datetime.now() - Rxy_time
    delta = delta.seconds * 1000000 + delta.microseconds
    Rxy_times.append(delta)

    Rxx_time = datetime.datetime.now()
    correlate(x_list, x_list)
    delta = datetime.datetime.now() - Rxx_time
    delta = delta.seconds * 1000000 + delta.microseconds
    Rxx_times.append(delta)
plt.plot(array_sizes, Rxx_times)
plt.plot(array_sizes, Rxy_times)
plt.show()

