# coding=utf-8
from datetime import date


def str_to_date(str):
    """将字符串转换为标准日期
    example: '2015-02-20'->2015-02-20
    :param str:
    :return: Date格式日期
    """
    str_array = str.split('-')
    try:
        standardized_date = date(int(str_array[0]), int(str_array[1]), int(str_array[2]))
    except ValueError:
        print str_array
    return standardized_date
