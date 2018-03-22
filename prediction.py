# *coding=utf8
from datetime import date, timedelta
from readtxt import InputTxtProcess, DataTrainTxtProcess

import matplotlib.pyplot as plt


def str_to_date(str):
    """将字符串转换为标准日期
    example: '2015-02-20'->2015-02-20
    :param str:
    :return: Date格式日期
    """
    str_array = str.split('-')
    return date(int(str_array[0]), int(str_array[1]), int(str_array[2]))


def segmentation(flavor, fn, fnd, d, psd, sd):
    """tongji

    :param flavor: flavor名称
    :param fn: flavor_name序列
    :param fnd: flavor_name_datetime序列
    :param d: delta切分时间段
    :param psd: prediction_start_date预测开始日期
    :param sd: start_date训练数据集中最早日期
    :return: [x_axis, y_axis]
    """
    x_axis = []  # 时间段
    y_axis = []  # 每个时间段flavor请求数量
    index = fn.index(flavor)
    datetime_list = fnd[index]  # 该flavor的所有日期数据
    # print datetime_list
    # print len(datetime_list)
    first_date = str_to_date(datetime_list[0].split(' ')[0])  # 原数据中该flavor最早的日期
    start_count_date = psd  # 统计时flavor开始的日期
    print first_date
    # print psd
    while start_count_date > sd:
        start_count_date -= timedelta(d)
        x_axis.append(
            start_count_date.strftime("%Y-%m-%d") + " to " + (start_count_date + timedelta(d - 1)).strftime("%Y-%m-%d"))
    start_count_date += timedelta(d)
    x_axis.reverse()
    del x_axis[0]
    # print start_count_date
    # print x_axis

    left_date = start_count_date
    right_date = left_date + timedelta(d)

    # todo:统计每个时间段flavor的请求数量应该有更快的算法
    while right_date <= psd:
        count = 0
        for dl in datetime_list:
            current_date = str_to_date(dl.split(' ')[0])
            if left_date <= current_date < right_date:
                count = count + 1
        y_axis.append(count)
        left_date = right_date
        right_date = left_date + timedelta(d)

    result = [x_axis, y_axis]
    return result


#################################
# 处理input.txt文件
# f_input = open("input_5flavors_cpu_7days.txt")
# input_data = f_input.readlines()
# f_input.close()
#
# flavor_selected = []  # input.txt中需要预测的flavor
# for id in input_data:
#     if id[:6] == "flavor":
#         flavor_selected.append(id.split(' ')[0])
#
# prediction_start = input_data[-2:-1][0].split(' ')[0]
# prediction_start_date = str_to_date(prediction_start)
# prediction_end = input_data[-1:][0].split(' ')[0]
# prediction_end_date = str_to_date(prediction_end)
# prediction_delta = (prediction_end_date - prediction_start_date).days  # 预测时间段的天数
#
# operator = {7: 7, 14: 7}
# DELTA = operator[prediction_delta]  # 切分统计的时间段
#################################
DELTA = InputTxtProcess().delta()  # 预测时间段的天数
flavor_selected = InputTxtProcess().flavor_selected()  # input.txt中需要预测的flavor
prediction_start_date = InputTxtProcess().prediction_start_date()

# #################################
# # 处理TrainData.txt文件
# # f_train = open("TrainData_2015.1.1_2015.2.19.txt")
# f_train = open("TrainData.txt")
# train_data = f_train.readlines()
# f_train.close()
#
# data_matrix = []
# for d in train_data:
#     data_matrix.append(d.split('\t'))
#
# start_date = str_to_date(data_matrix[0][2].split(' ')[0])
# end_date = str_to_date(data_matrix[len(data_matrix) - 1][2].split(' ')[0])
# #################################
#
#
# #################################
# # 提取flavor name
# flavor_name = []  # ['flavor1', 'flavor2', 'flavor3', 'flavor4', 'flavor5', ...]
# flavor_name_temp = []
# flavor_id = []
# for dm in data_matrix:
#     if dm[1] not in flavor_name_temp:
#         flavor_name_temp.append(dm[1])
#         flavor_id.append(int(dm[1][6:]))
#
# flavor_id.sort()
# for fi in flavor_id:
#     for fnt in flavor_name_temp:
#         if int(fnt[6:]) == fi:
#             flavor_name.append(fnt)
#
# # print flavor_name
# #################################
#
#
# #################################
# # 提取flavor对应的所有时间点
# flavor_name_datetime = []
# for fn in flavor_name:
#     fnd_item = []
#     for dm in data_matrix:
#         if dm[1] == fn:
#             fnd_item.append(dm[2])
#     flavor_name_datetime.append(fnd_item)
#
# # print flavor_name_datetime
# #################################

start_date = DataTrainTxtProcess().start_date()
flavor_name = DataTrainTxtProcess().flavor_name()
flavor_name_datetime = DataTrainTxtProcess().flavor_name_datetime(flavor_name)

period_data = []  # [[x_axis,y_axis],[x_axis,y_axis],[x_axis,y_axis]...]
final_period = []
max_period_length = 0
for fs in flavor_selected:
    period_data.append(segmentation(fs, flavor_name, flavor_name_datetime, DELTA, prediction_start_date, start_date))

for ps in flavor_selected:
    print period_data[flavor_selected.index(ps)][0]
    print period_data[flavor_selected.index(ps)][1]
    plt.plot(period_data[flavor_selected.index(ps)][1], label=ps, linestyle="-")

plt.legend(loc='upper left')
plt.show()
