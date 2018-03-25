# coding=utf-8
from datetime import timedelta
from readtxt import InputTxtProcess, TrainDataTxtProcess
from string_tools import str_to_date


def __requests_count_everyday(datetime_list, start_date, end_date, lost_date):
    """
    统计flavor在训练集全期内每一天的请求次数，对于缺失的日期，采用指数平滑进行填补
    :param datetime_list:
    :param start_date:
    :param end_date:
    :param lost_date: 缺失日期组成的序列
    :return: {date：count}的字典
    """
    date_count_dict = {}
    standardized_date_list = []
    for dl in datetime_list:
        standardized_date_list.append(str_to_date(dl.split(' ')[0]))

    current_date = start_date
    while current_date <= end_date:
        current_count = 0
        for sdl in standardized_date_list:
            if sdl == current_date:
                current_count = current_count + 1
        date_count_dict[current_date] = current_count
        current_date = current_date + timedelta(1)

    # print lost_date
    # print date_count_dict[lost_date[0]],date_count_dict[lost_date[1]],date_count_dict[lost_date[2]]
    alpha = 1.1
    s1 = date_count_dict[start_date]
    s_list = {start_date: s1}
    current_date = start_date + timedelta(1)
    while current_date <= end_date:
        if current_date in lost_date:
            date_count_dict[current_date] = s_list[current_date - timedelta(1)]
        s = alpha * date_count_dict[current_date] + (1 - alpha) * s_list[current_date - timedelta(1)]
        s_list[current_date] = int(round(s))
        if s_list[current_date] < 0:
            s_list[current_date] = 0
        current_date = current_date + timedelta(1)
    # print date_count_dict[lost_date[0]], date_count_dict[lost_date[1]], date_count_dict[lost_date[2]]
    return date_count_dict


def __segmentation(flavor, fn, fnd, d, psd, sd, ed, ld):
    """
    以时间段d(delta)划分数据集统计每段flavor的请求数
    :param flavor: flavor名称
    :param fn: flavor_name序列
    :param fnd: flavor_name_datetime序列
    :param d: delta切分时间段
    :param psd: prediction_start_date预测开始日期
    :param sd: start_date训练集最早日期
    :param ed: end_date训练集结束日期
    :param ld: lost_date训练集中缺失的日期
    :return: [x_axis, y_axis]
    """
    x_axis = []  # 时间段
    y_axis = []  # 每个时间段flavor请求数量
    index = fn.index(flavor)
    datetime_list = fnd[index]  # 该flavor的所有日期数据
    date_count_dict = __requests_count_everyday(datetime_list, sd, ed, ld)  # 统计该flavor每一天的请求量

    # print datetime_list
    # first_date = str_to_date(datetime_list[0].split(' ')[0])  # 原数据中该flavor最早的日期
    start_count_date = psd  # 统计时flavor开始的日期
    # print first_date
    # print psd
    while start_count_date > sd:
        start_count_date = start_count_date - timedelta(d)
        x_axis.append(
            start_count_date.strftime("%Y-%m-%d") + " to " + (start_count_date + timedelta(d - 1)).strftime("%Y-%m-%d"))
    start_count_date = start_count_date + timedelta(d)
    x_axis.reverse()
    del x_axis[0]

    left_date = start_count_date
    right_date = left_date + timedelta(d)
    while right_date <= psd:
        count = 0
        current_date = left_date
        while current_date < right_date:
            count = count + date_count_dict[current_date]
            current_date = current_date + timedelta(1)
        # for dl in datetime_list:
        #     current_date = str_to_date(dl.split(' ')[0])
        #     if left_date <= current_date < right_date:
        #         count = count + 1
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
    start_date = tdtp.start_date()  # 训练集开始日期
    end_date = tdtp.end_date()  # 训练集结束日期
    flavor_name = tdtp.flavor_name()
    flavor_name_datetime = tdtp.flavor_name_datetime(flavor_name)
    lost_date = tdtp.find_lost_date()

    period_data = []  # [[x_axis,y_axis],[x_axis,y_axis],[x_axis,y_axis]...]
    for fs in flavor_selected:
        item = __segmentation(fs, flavor_name, flavor_name_datetime, DELTA, prediction_start_date, start_date, end_date,
                              lost_date)
        item.append(fs)
        period_data.append(item)

    return period_data
