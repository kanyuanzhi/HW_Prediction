# coding=utf-8
from datetime import timedelta
from readtxt import InputTxtProcess, TrainDataTxtProcess
from string_tools import str_to_date


def __segmentation(flavor, fn, fnd, d, psd, sd):
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
    # first_date = str_to_date(datetime_list[0].split(' ')[0])  # 原数据中该flavor最早的日期
    start_count_date = psd  # 统计时flavor开始的日期
    # print first_date
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


def data_process(ecs_lines, input_lines):
    itp = InputTxtProcess(input_lines)
    DELTA = itp.delta()  # 预测时间段的天数
    flavor_selected = itp.flavor_selected()  # input.txt中需要预测的flavor
    prediction_start_date = itp.prediction_start_date()

    tdtp = TrainDataTxtProcess(ecs_lines)
    start_date = tdtp.start_date()
    flavor_name = tdtp.flavor_name()
    flavor_name_datetime = tdtp.flavor_name_datetime(flavor_name)

    period_data = []  # [[x_axis,y_axis],[x_axis,y_axis],[x_axis,y_axis]...]
    for fs in flavor_selected:
        item = __segmentation(fs, flavor_name, flavor_name_datetime, DELTA, prediction_start_date, start_date)
        item.append(fs)
        period_data.append(item)

    return period_data
