# coding=utf-8
from datetime import timedelta
from readtxt import InputTxtProcess, TrainDataTxtProcess
from string_tools import str_to_date
from gauss_filter import Gauss


def __requests_count_everyday(datetime_list, start_date, end_date, lost_date):
    """
    统计flavor在训练集全期内每一天的请求次数，对于缺失的日期，采用指数平滑进行填补
    :param datetime_list:
    :param start_date:
    :param end_date:
    :param lost_date: 缺失日期组成的序列
    :return: {date：count}的字典
    """
    holiday_date = ['2013-01-01', '2013-02-09', '2013-05-01', '2013-10-01', '2013-11-11',
                    '2014-01-01', '2014-01-30', '2014-05-01', '2014-10-01', '2014-11-11',
                    '2015-01-01', '2015-02-18', '2015-05-01', '2015-10-01', '2015-11-11',
                    '2016-01-01', '2016-02-07', '2016-05-01', '2016-10-01', '2016-11-11',
                    '2017-01-01', '2017-01-27', '2017-05-01', '2017-10-01', '2017-11-11',
                    '2018-01-01', '2018-02-15', '2018-05-01', '2018-10-01', '2018-11-11']
    # standardized_holiday_date = []
    # for hd in holiday_date:
    #     standardized_holiday_date.append(str_to_date(hd))
    standardized_holiday_date = [str_to_date(hd) for hd in holiday_date]

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

    for current_date in date_count_dict:
        # 将节假日的数据取两边平均
        if current_date in standardized_holiday_date:
            if current_date - timedelta(1) not in date_count_dict:
                date_count_dict[current_date] = date_count_dict[current_date + timedelta(1)]
            elif current_date + timedelta(1) not in date_count_dict:
                date_count_dict[current_date] = date_count_dict[current_date - timedelta(1)]
            else:
                date_count_dict[current_date] = (date_count_dict[current_date - timedelta(1)] + date_count_dict[
                    current_date + timedelta(1)]) / 2
    # print lost_date
    # print date_count_dict[lost_date[0]],date_count_dict[lost_date[1]],date_count_dict[lost_date[2]]
    # alpha = 1.1
    # s1 = date_count_dict[start_date]
    # s_list = {start_date: s1}
    # current_date = start_date + timedelta(1)
    # while current_date <= end_date:
    #     if current_date in lost_date:
    #         date_count_dict[current_date] = s_list[current_date - timedelta(1)]
    #     s = alpha * date_count_dict[current_date] + (1 - alpha) * s_list[current_date - timedelta(1)]
    #     s_list[current_date] = int(round(s))
    #     if s_list[current_date] < 0:
    #         s_list[current_date] = 0
    #     current_date = current_date + timedelta(1)
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
    period_count_list = []
    current_date = sd
    while current_date <= ed:
        period_count_list.append(date_count_dict[current_date])
        current_date = current_date + timedelta(1)

    # 对原始数据做高斯去噪
    g = Gauss(period_count_list, 7, 1.5)
    g.process()

    # print datetime_list
    # first_date = str_to_date(datetime_list[0].split(' ')[0])  # 原数据中该flavor最早的日期
    start_count_date = ed + timedelta(1)  # 统计时flavor开始的日期
    while True:
        start_count_date = start_count_date - timedelta(d)
        if start_count_date < sd:
            break
        x_axis.append(start_count_date)

    x_axis.reverse()
    # del x_axis[0]

    period_numbers = int(len(period_count_list) / d)
    start_count_index = len(period_count_list) - period_numbers * d
    for i in range(period_numbers):
        y_axis.append(sum(period_count_list[start_count_index + i * d:start_count_index + (i + 1) * d]))

    # left_date = start_count_date
    # right_date = left_date + timedelta(d)
    # while right_date <= psd:
    #     count = 0
    #     current_date = left_date
    #     while current_date < right_date:
    #         count = count + date_count_dict[current_date]
    #         current_date = current_date + timedelta(1)
    #     # for dl in datetime_list:
    #     #     current_date = str_to_date(dl.split(' ')[0])
    #     #     if left_date <= current_date < right_date:
    #     #         count = count + 1
    #     y_axis.append(count)
    #     left_date = right_date
    #     right_date = left_date + timedelta(d)

    result = [x_axis, y_axis]
    return result


def data_process(ecs_lines, input_lines):
    itp = InputTxtProcess(input_lines)
    DELTA = itp.delta()  # 预测时间段的天数
    flavor_selected = itp.flavor_selected()  # input.txt中需要预测的flavor
    prediction_start_date = itp.prediction_start_date()
    prediction_end_date = itp.prediction_end_date()

    tdtp = TrainDataTxtProcess(ecs_lines)
    start_date = tdtp.start_date()  # 训练集开始日期
    end_date = tdtp.end_date()  # 训练集结束日期
    flavor_name = tdtp.flavor_name()
    flavor_name_datetime = tdtp.flavor_name_datetime(flavor_name)
    lost_date = tdtp.find_lost_date()
    period_data = []  # [[x_axis,y_axis],[x_axis,y_axis],[x_axis,y_axis]...]
    if prediction_start_date == end_date + timedelta(1):
        period_data1 = []
        for fs in flavor_selected:
            item = __segmentation(fs, flavor_name, flavor_name_datetime, DELTA, prediction_start_date, start_date,
                                  end_date, lost_date)
            item.append(fs)
            period_data1.append(item)
        period_data = [period_data1]
    else:
        # 处理预测开始时间与训练结束时间不连续的情况
        period_data1 = []
        period_data2 = []
        delta1 = (prediction_start_date - end_date).days - 1
        delta2 = delta1 + DELTA
        for fs in flavor_selected:
            item1 = __segmentation(fs, flavor_name, flavor_name_datetime, delta1, prediction_start_date, start_date,
                                   end_date, lost_date)
            item1.append(fs)
            period_data1.append(item1)

            item2 = __segmentation(fs, flavor_name, flavor_name_datetime, delta2, prediction_start_date, start_date,
                                   end_date, lost_date)
            item2.append(fs)
            period_data2.append(item2)
        period_data = [period_data1, period_data2]

    return period_data


def data_process_oneday(ecs_lines, input_lines):
    """
    统计单天的请求数
    :param ecs_lines:
    :param input_lines:
    :return:
    """
    itp = InputTxtProcess(input_lines)
    DELTA = itp.delta()  # 预测时间段的天数
    flavor_selected = itp.flavor_selected()  # input.txt中需要预测的flavor
    prediction_start_date = itp.prediction_start_date()

    tdtp = TrainDataTxtProcess(ecs_lines)
    start_date = tdtp.start_date()  # 训练集开始日期
    end_date = tdtp.end_date()  # 训练集结束日期
    flavor_name = tdtp.flavor_name()  # 数据集中所有flavor名称
    flavor_name_datetime = tdtp.flavor_name_datetime(flavor_name)  # 数据集中所有flavor对应的日期的二维list,index与flavor_name对应
    lost_date = tdtp.find_lost_date()

    period_data = []  # [[x_axis,y_axis],[x_axis,y_axis],[x_axis,y_axis]...]
    for fs in flavor_selected:
        item = __segmentation(fs, flavor_name, flavor_name_datetime, 1, prediction_start_date, start_date, end_date,
                              lost_date)
        item.append(fs)
        period_data.append(item)

    return period_data


def data_process_oneday_accumulate(ecs_lines, input_lines):
    """
    累加统计每一天的请求数
    :param ecs_lines:
    :param input_lines:
    :return:
    """
    period_data = data_process_oneday(ecs_lines, input_lines)
    period_data_accumulate = []
    for pr in period_data:
        datetime_count_list = []
        for i in range(len(pr[1])):
            datetime_count_list.append(sum(pr[1][:i + 1]))
        period_data_accumulate.append([pr[0], datetime_count_list, pr[2]])
        # print datetime_count_list
        # print pr[1]
    return period_data_accumulate


def data_compare(flavor_prediction_numbers, input_lines, ecs_lines):
    """
    预测值与实际值作比较
    :param flavor_prediction_numbers:
    :param input_lines:
    :param ecs_lines:
    :return:
    """
    itp = InputTxtProcess(input_lines)
    flavor_selected = itp.flavor_selected()  # input.txt中需要预测的flavor
    prediction_start_date = itp.prediction_start_date()
    prediction_end_date = itp.prediction_end_date()

    tdtp = TrainDataTxtProcess(ecs_lines)
    flavor_name = tdtp.flavor_name()
    flavor_name_datetime = tdtp.flavor_name_datetime(flavor_name)

    flavor_real_numbers = []
    for fs in flavor_selected:
        index = flavor_name.index(fs)
        datetime_list = flavor_name_datetime[index]
        count = 0
        for dl in datetime_list:
            if prediction_start_date <= str_to_date(dl.split(' ')[0]) < prediction_end_date:
                count = count + 1
        flavor_real_numbers.append(count)
    print "实际值：", flavor_real_numbers
    print "预测值：", flavor_prediction_numbers
    n = len(flavor_real_numbers)
    a = list(map(lambda x: x[0] - x[1], zip(flavor_real_numbers, flavor_prediction_numbers)))
    c = pow(sum([pow(i, 2) for i in a]) / float(n), 0.5)
    d = pow(sum([pow(i, 2) for i in flavor_real_numbers]) / float(n), 0.5) + \
        pow(sum([pow(i, 2) for i in flavor_prediction_numbers]) / float(n), 0.5)
    score = round((1 - c / d) * 100, 2)
    print "得分：", score, "/ 100"
    return score
