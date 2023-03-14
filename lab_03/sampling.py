from math import pi, exp, sin
import matplotlib.pyplot as plt


def get_samples(t_max, dt):
    samples = []
    t = -t_max
    while t <= t_max:
        samples.append(t)
        t += dt
    return samples


def get_gauss(args, sigma):
    u = []
    for x in args:
        u.append(exp(-x * x / (sigma * sigma)))
    return u


def get_rect(args, t):
    u = []
    for x in args:
        if abs(x) > t / 2:
            u.append(0)
        else:
            u.append(1)
    return u


def restore_signal(sampled_signal, samples, x, dt):
    restored = []
    for t in x:
        u = 0
        for i in range(len(samples)):
            if t == samples[i]:
                u += sampled_signal[i]
            else:
                u += sampled_signal[i] * sin(pi * (t - samples[i]) / dt) / \
                     (pi * (t - samples[i]) / dt)
        restored.append(u)
    return restored


if __name__ == '__main__':
    sigma = 1  # для сигнала Гаусса
    tt = 2  # для прямоугольного импульса
    samples_num = int(input("Введите количество отсчетов: "))
    dt = float(input("Введите частоту дискретизации (шаг): "))
    t_max = dt * (samples_num - 1) / 2  # правая граница
    samples = get_samples(t_max, dt)  # набор отсчетов
    x = get_samples(t_max, 0.005)  # набор значений аргументов исходного сигнала

    # дискретизованные сигналы
    sampled_gauss = get_gauss(samples, sigma)
    sampled_rect = get_rect(samples, tt)

    # исходные сигналы
    gauss = get_gauss(x, sigma)
    rect = get_rect(x, tt)

    # восстановленные сигналы
    restored_gauss = restore_signal(sampled_gauss, samples, x, dt)
    restored_rect = restore_signal(sampled_rect, samples, x, dt)

    plt.subplot(3, 1, 1)
    plt.title('Сигнал Гаусса')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(x, restored_gauss, label='Восстановленный')
    plt.plot(x, gauss, label='Исходный')
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.title('Прямоугольный импульс')
    plt.xlabel('x')
    plt.ylabel('U(x)')
    plt.plot(x, restored_rect, label='Восстановленный')
    plt.plot(x, rect, label='Исходный')
    plt.legend()
    plt.grid()

    plt.show()
