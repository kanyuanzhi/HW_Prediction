# coding=utf-8
from data_process import data_process


# import matplotlib.pyplot as plt


def __average(prediction_numbers):
    sum = 0
    for pn in prediction_numbers:
        sum += pn
    return int(sum / len(prediction_numbers))


def prediction(ecs_lines, input_lines):
    period_data = data_process(ecs_lines, input_lines)
    flavor_prediction_numbers = []

    for ps in period_data:
        flavor_prediction_numbers.append(__average(ps[1]))
        # print ps[2]
        # print ps[0]
        # print ps[1]
    # plt.plot(ps[1], label=ps[2], linestyle="-")
    #
    # plt.legend(loc='upper left')
    # plt.show()


    # flavor_prediction_numbers = [45, 12, 53, 50, 30]  # 预测数量

    return flavor_prediction_numbers
