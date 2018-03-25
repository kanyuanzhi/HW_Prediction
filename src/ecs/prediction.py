# coding=utf-8
from data_process import data_process


# import matplotlib.pyplot as plt

def __your_prediction(prediction_numbers):
    num = 0
    # 根据prediction_numbers预测该flavor在下一阶段的数量num
    return num


def __average(prediction_numbers):
    sum = 0
    for pn in prediction_numbers:
        sum = sum + pn
    return int(sum / len(prediction_numbers))


def __onetime_exponential_smoothing(prediction_numbers):
    alpha = 1.1
    s1 = sum(prediction_numbers[0:3]) / 3.0
    s_list = [s1]
    for i in range(1, len(prediction_numbers)):
        s = alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1]
        s_list.append(s)

    num = int(round(s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num


def prediction(ecs_lines, input_lines):
    period_data = data_process(ecs_lines, input_lines)
    flavor_prediction_numbers = []
    # example ######
    # for ps in period_data:
    #    flavor_prediction_numbers.append(__your_prediction(ps[1]))
    ###########################

    # test ######
    for ps in period_data:
        # flavor_prediction_numbers.append(__average(ps[1]))
        flavor_prediction_numbers.append(__onetime_exponential_smoothing(ps[1]))
        #########################
        # print ps[2]
        # print ps[0]
        # print ps[1]
    # plt.plot(ps[1], label=ps[2], linestyle="-")
    #
    # plt.legend(loc='upper left')
    # plt.show()


    # flavor_prediction_numbers = [45, 12, 53, 50, 30]  # 预测数量

    return flavor_prediction_numbers
