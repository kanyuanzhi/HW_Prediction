# coding=utf-8
from string_tools import str_to_date
from datetime import timedelta


class InputTxtProcess():
    """
    处理input.txt文件
    """
    __input_lines = []

    def __init__(self, input_lines):
        self.__input_lines = input_lines

    def flavor_selected(self):
        flavor_selected = []  # input.txt中需要预测的flavor
        for id in self.__input_lines:
            if id[:6] == "flavor":
                flavor_selected.append(id.split(' ')[0])
        return flavor_selected

    def prediction_start_date(self):
        prediction_start = self.__input_lines[-2:-1][0].split(' ')[0]
        prediction_start_date = str_to_date(prediction_start)
        return prediction_start_date

    def prediction_end_date(self):
        prediction_end = self.__input_lines[-1:][0].split(' ')[0]
        prediction_end_date = str_to_date(prediction_end)
        return prediction_end_date

    def delta(self):
        prediction_delta = (self.prediction_end_date() - self.prediction_start_date()).days  # 预测时间段的天数
        # operator = {7: 7, 14: 7}
        # delta = operator[prediction_delta]  # 切分统计的时间段
        return prediction_delta

    def flavor_specification(self):
        """
        各flavor的配置信息
        :return:
        """
        flavor_specification = []
        for id in self.__input_lines:
            if id[:6] == "flavor":
                flavor_specification.append(id.split(' '))
        return flavor_specification

    def physical_server_specification(self):
        """
        物理服务器配置信息CPU，内存大小GB，硬盘大小GB
        :return:
        """
        return self.__input_lines[0].split(' ')

    def resource_name(self):
        """
        需要优化的资源名称CPU或MEM
        :return:
        """
        return self.__input_lines[-4:-3][0][0:3]


class TrainDataTxtProcess():
    """
    处理TrainData.txt文件
    """
    __data_matrix = []

    def __init__(self, ecs_lines):
        self.__data_matrix = []
        for d in ecs_lines:
            self.__data_matrix.append(d.split('\t'))
        self.find_lost_date()

    def start_date(self):
        """
        获取数据集的开始日期
        :return:
        """
        return str_to_date(self.__data_matrix[0][2].split(' ')[0])

    def end_date(self):
        """
        获取数据集的结尾日期
        :return:
        """
        return str_to_date(self.__data_matrix[len(self.__data_matrix) - 1][2].split(' ')[0])

    def find_lost_date(self):
        lost_date = []
        start_date = self.start_date()
        end_date = self.end_date()
        all_date = []
        for dm in self.__data_matrix:
            temp = str_to_date(dm[2].split(' ')[0])
            if temp not in all_date:
                all_date.append(temp)
        current_date = start_date
        while current_date <= end_date:
            if current_date not in all_date:
                lost_date.append(current_date)
            current_date = current_date + timedelta(1)
        return lost_date

    def flavor_name(self):
        """
        获取数据集中出现的flavor名称
        :return:
        """
        flavor_name = []  # ['flavor1', 'flavor2', 'flavor3', 'flavor4', 'flavor5', ...]
        flavor_name_temp = []
        flavor_id = []
        for dm in self.__data_matrix:
            if dm[1] not in flavor_name_temp:
                flavor_name_temp.append(dm[1])
                flavor_id.append(int(dm[1][6:]))
        flavor_id.sort()
        for fi in flavor_id:
            for fnt in flavor_name_temp:
                if int(fnt[6:]) == fi:
                    flavor_name.append(fnt)
        return flavor_name

    def flavor_name_datetime(self, flavor_name):
        """
        获取各flavor对应的所有时间点
        :param flavor_name:
        :return:
        """
        flavor_name_datetime = []
        for fn in flavor_name:
            fnd_item = []
            for dm in self.__data_matrix:
                if dm[1] == fn:
                    fnd_item.append(dm[2])
            flavor_name_datetime.append(fnd_item)
        return flavor_name_datetime
