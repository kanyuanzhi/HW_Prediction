# coding=utf-8
from math import pi, pow, exp


class Gauss:
    """
    高斯滤波
    """
    def __init__(self, date_list, n, sigma):
        """
        :param date_list: 待处理序列
        :param n: 平滑范围
        :param sigma: sigma值
        """
        self.__date_list = date_list
        self.__n = n
        self.__sigma = sigma

    def process(self):
        head_append_list = [self.__date_list[0] for i in range(self.__n)]
        tail_append_list = [self.__date_list[len(self.__date_list) - 1] for i in range(self.__n)]
        date_list_extend = head_append_list + self.__date_list + tail_append_list
        weight_list = generate_weight_list(self.__n, self.__sigma)
        for i in range(len(self.__date_list)):
            count_processed = 0
            for j in range(len(weight_list)):
                count_processed = count_processed + weight_list[j] * date_list_extend[i + j]
            self.__date_list[i] = count_processed
        # return self.__date_list


def gauss(r, sigma):
    g = (1 / pow(2 * pi * pow(sigma, 2), 0.5)) * exp(-pow(r, 2) / (2 * pow(sigma, 2)))
    return g


def generate_weight_list(n, sigma):
    gauss_value_list = []
    weight_list = []
    for i in range(n + 1):
        gauss_value_list.append(gauss(i, sigma))
    for gauss_value in gauss_value_list[::-1]:
        weight_list.append(gauss_value)
    for gauss_value in gauss_value_list[1:]:
        weight_list.append(gauss_value)
    s = sum(weight_list)
    weight_list_final = [weight / s for weight in weight_list]
    return weight_list_final


if __name__ == "__main__":
    a = [1, 2, 20, 4, 2]
    g = Gauss(a, 3, 0.5)
    g.process()
    print a
