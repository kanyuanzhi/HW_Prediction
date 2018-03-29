# coding=utf-8
from data_process import *
from readtxt import InputTxtProcess
from adaline import adaline
from bp_network import bp_network

# import pandas as pd
# # # import statsmodels.api as sm
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt
# import matplotlib as mpl


def __your_prediction(prediction_numbers):
    num = 0
    # 根据prediction_numbers预测该flavor在下一阶段的数量num
    return num


def __average(prediction_numbers, period):
    prediction_list = prediction_numbers[-period:]
    return int(sum(prediction_list) / period)


def __onetime_exponential_smoothing(prediction_numbers):
    alpha = 1.1
    s1 = sum(prediction_numbers[0:3]) / 3.0
    s_list = [s1]
    for i in range(1, len(prediction_numbers)):
        s = (alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1])
        s_list.append(s)

    num = int(round(s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num


def __onetime_exponential_smoothing_enhanced(prediction_numbers):
    alpha = 0.7
    beta = 0.8
    s1 = prediction_numbers[0]
    s2 = prediction_numbers[1]
    s_list = [s1, s2]
    for i in range(1, len(prediction_numbers)):
        s = (alpha * prediction_numbers[i] + (1 - alpha) * s_list[i - 1] + beta * prediction_numbers[i - 1] + (
            1 - beta) * s_list[i - 2]) / 2
        s_list.append(s)

    num = int(round(s_list[len(s_list) - 1]))
    if num < 0:
        num = 0
    return num


def prediction(ecs_lines, input_lines):
    # itp = InputTxtProcess(input_lines)
    # delta = itp.delta()  # 预测时间段的天数
    period_data_oneday = data_process_oneday(ecs_lines, input_lines)  # 不切分，按天输出

    period_data = data_process(ecs_lines, input_lines)
    flavor_prediction_numbers = []
    # example ######
    for ps in period_data:
        flavor_prediction_numbers.append(__average(ps[1], 1))
    ###########################
    # for ps in period_data:
    #     flavor_prediction_numbers.append(__onetime_exponential_smoothing(ps[1]))

    # for ps in period_data:
    #     flavor_prediction_numbers.append(bp_network(ps[1], len(period_data[0][1]) / 2 + 2, ps[2]))

    # bp_network(period_data[7][1],len(period_data[0][1]) / 2 + 2)

    # for ps in period_data:
    #     flavor_prediction_numbers.append(adaline(ps[1], len(period_data[0][1]) / 2 + 2))

    # adaline(period_data[1][1], 10)


    # plt.figure(0)
    # for i, ps in enumerate(period_data_oneday):
    #     #flavor_prediction_numbers.append(__onetime_exponential_smoothing(ps[1]))
    #     dta = pd.Series(ps[1])
    #     diff1 = dta.diff(1)
    #     diff2 = dta.diff(2)
    #     ax = plt.subplot(len(period_data_oneday) / 2 + 1, 2, i + 1)
    #     plt.plot(dta)
    #     plt.sca(ax)
    # plt.figure(1)
    # for i, ps in enumerate(period_data_oneday):
    #     dta = pd.Series(ps[1])
    #     diff1 = dta.diff(1)
    #     ax = plt.subplot(len(period_data_oneday) / 2 + 1, 2, i + 1)
    #     plt.plot(diff1)
    #     plt.sca(ax)
    # plt.figure(2)
    # for i, ps in enumerate(period_data_oneday):
    #     dta = pd.Series(ps[1])
    #     diff2 = dta.diff(2)
    #     ax = plt.subplot(len(period_data_oneday) / 2 + 1, 2, i + 1)
    #     plt.plot(diff2)
    #     plt.sca(ax)
    # plt.show()

    #########################
    # print ps[2]
    # print ps[0]
    # print ps[1]

    # period_data_accumulate = data_process_oneday_accumulate(ecs_lines, input_lines)
    # # xs = period_data_oneday[0][0]
    # xs = period_data_accumulate[0][0]
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # # for i, ps in enumerate(period_data_oneday):
    # for i, ps in enumerate(period_data_accumulate):
    #     plt.plot(xs, ps[1], label=ps[2], linestyle="-")
    # plt.gcf().autofmt_xdate()
    # plt.legend(loc='upper left')
    # plt.grid(True)
    # plt.show()
    # flavor_prediction_numbers = [45, 12, 53, 50, 30]  # 预测数量

    # data_compare(flavor_prediction_numbers, input_lines, ecs_lines)

    return flavor_prediction_numbers
