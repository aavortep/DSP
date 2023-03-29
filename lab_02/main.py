from sampling import get_samples, get_gauss, get_rect
from cmath import exp, pi
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift
import time


def dft(signal):
    degree = [-2 * pi * complex(0, 1) * k / len(signal) for k in range(len(signal))]
    discreted = [0 for i in range(len(signal))]
    for k in range(len(discreted)):
        for n in range(len(signal)):
            discreted[k] += signal[n] * exp(degree[k] * n)
    return discreted


#def remove_twins(fft_signal, t0):


if __name__ == '__main__':
    sigma = 0.5  # для сигнала Гаусса
    tt = 4  # для прямоугольного импульса
    samples_num = 256
    dt = 0.05
    t_max = dt * (samples_num - 1) / 2  # правая граница
    samples = get_samples(t_max, dt)  # набор отсчетов
    # сигналы
    gauss = get_gauss(samples, sigma)
    rect = get_rect(samples, tt)

    # ДПФ
    start = time.perf_counter_ns()
    dft_gauss = dft(gauss)
    end = time.perf_counter_ns()
    dft_time = end - start
    dft_rect = dft(rect)

    # БПФ
    start = time.perf_counter_ns()
    fft_gauss = fft(gauss)
    end = time.perf_counter_ns()
    fft_time = end - start
    fft_rect = fft(rect)

    shifted_gauss = fftshift(fft_gauss)
    shifted_rect = fftshift(fft_rect)

    print("Время выполнения ДПФ: ", dft_time, " нс")
    print("Время выполнения БПФ: ", fft_time, " нс")

    x = [i for i in range(len(samples))]

    graph_gauss_dft = [abs(i) for i in dft_gauss]
    graph_rect_dft = [abs(i) for i in dft_rect]
    graph_gauss_fft = [abs(i) for i in fft_gauss]
    graph_rect_fft = [abs(i) for i in fft_rect]
    graph_shifted_gauss = [abs(i) for i in shifted_gauss]
    graph_shifted_rect = [abs(i) for i in shifted_rect]

    plt.subplot(3, 1, 1)
    plt.title('Сигнал Гаусса. ДПФ')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_gauss_dft)
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.title('Сигнал Гаусса. БПФ')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_gauss_fft)
    plt.grid()

    plt.show()

    plt.subplot(3, 1, 1)
    plt.title('Прямоугольный импульс. ДПФ')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_rect_dft)
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.title('Прямоугольный импульс. БПФ')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_rect_fft)
    plt.grid()

    plt.show()

    plt.subplot(3, 1, 1)
    plt.title('Сигнал Гаусса без "близнецов"')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_shifted_gauss)
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.title('Прямоугольный импульс без "близнецов"')
    plt.xlabel('x')
    plt.ylabel('|V(x)|')
    plt.plot(x, graph_shifted_rect)
    plt.grid()

    plt.show()
