from sampling import get_rect, get_gauss, get_samples
from convolution import convolution
from math import exp
from numpy.random import normal
import random
# from scipy.signal import filtfilt
import matplotlib.pyplot as plt


def gen_impulse_noise(size, N, mult):
    step = size // N
    y = [0 for i in range(size)]
    for i in range(N // 2):
        y[round(size / 2) + i * step] = mult * (0.5 + random.random())
        y[round(size / 2) - i * step] = mult * (0.5 + random.random())
    return y


def distorted_signals(ideal_sig, rect_noise, gauss_noise):
    sig_1 = [ideal_sig[i] + rect_noise[i] for i in range(len(ideal_sig))]
    sig_2 = [ideal_sig[i] + gauss_noise[i] for i in range(len(ideal_sig))]
    return sig_1, sig_2


def get_butter_filter(samples, D, filter_type):
    n = 2
    # freqs = [i for i in range(1, sig_len + 1)]
    if filter_type == "low":
        H = [1 / (1 + (f / D)) ** (2 * n) for f in samples]
    else:
        H = [1 / (1 + (D / f)) ** (2 * n) for f in samples]
    return H


def get_gauss_filter(samples, D, filter_type):
    # freqs = [i for i in range(1, sig_len + 1)]
    if filter_type == "low":
        H = [exp(-f * f / (2 * D * D)) for f in samples]
    else:
        H = [1 - exp(-f * f / (2 * D * D)) for f in samples]
    return H


if __name__ == '__main__':
    sigma = 0.5  # для сигнала Гаусса
    tt = 4  # для прямоугольного импульса
    samples_num = 256
    dt = 0.05
    t_max = dt * (samples_num - 1) / 2  # правая граница
    samples = get_samples(t_max, dt)  # набор отсчетов
    # сигналы
    gauss = get_gauss(samples, sigma)
    noise_rect = gen_impulse_noise(len(gauss), 7, 0.4)
    noise_gauss = [normal(0, 0.05) for i in range(len(gauss))]

    # искаженные сигналы
    distorted_rect, distorted_gauss = distorted_signals(gauss, noise_rect, noise_gauss)
    # фильтры
    sig_len = len(distorted_rect)
    butter_filter = get_butter_filter(samples, 6, "low")
    gauss_filter = get_gauss_filter(samples, 2, "low")

    # фильтрация частот
    rect_butter = convolution(distorted_rect, butter_filter, samples_num)
    rect_gauss = convolution(distorted_rect, gauss_filter, samples_num)
    gauss_butter = convolution(distorted_gauss, butter_filter, samples_num)
    gauss_gauss = convolution(distorted_gauss, gauss_filter, samples_num)

    n_graph = [i for i in range(2 * samples_num)]
    plt.subplot(3, 1, 1)
    plt.title('Сигнал, искаженный импульсной помехой')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(samples, distorted_rect)
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.title('Фильтрация Баттеруортом')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(n_graph, rect_butter)
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.title('Фильтрация Гауссом')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(n_graph, rect_gauss)
    plt.grid()
    plt.show()

    plt.subplot(3, 1, 1)
    plt.title('Сигнал, искаженный гауссовой помехой')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(samples, distorted_gauss)
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.title('Фильтрация Баттеруортом')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(n_graph, gauss_butter)
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.title('Фильтрация Гауссом')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(n_graph, gauss_gauss)
    plt.grid()
    plt.show()
