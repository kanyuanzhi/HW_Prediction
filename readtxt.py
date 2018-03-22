# *coding=utf8
from string_tools import str_to_date


class InputTxtProcess():
    """
    处理input.txt文件
    """
    __f_input = open("input_5flavors_cpu_7days.txt")
    __input_data = __f_input.readlines()
    __f_input.close()

    __prediction_start = __input_data[-2:-1][0].split(' ')[0]
    __prediction_start_date = str_to_date(__prediction_start)
    __prediction_end = __input_data[-1:][0].split(' ')[0]
    __prediction_end_date = str_to_date(__prediction_end)

    def flavor_selected(self):
        flavor_selected = []  # input.txt中需要预测的flavor
        for id in self.__input_data:
            if id[:6] == "flavor":
                flavor_selected.append(id.split(' ')[0])
        return flavor_selected

    def delta(self):
        prediction_delta = (self.__prediction_end_date - self.__prediction_start_date).days  # 预测时间段的天数
        operator = {7: 7, 14: 7}
        DELTA = operator[prediction_delta]  # 切分统计的时间段
        return DELTA

    def prediction_start_date(self):
        return self.__prediction_start_date


class TrainDataTxtProcess():
    """
    处理TrainData.txt文件
    """
    __f_train = open("TrainData.txt")
    __train_data = __f_train.readlines()
    __f_train.close()
    __data_matrix = []
    __flavor_name = []  # ['flavor1', 'flavor2', 'flavor3', 'flavor4', 'flavor5', ...]
    __flavor_name_datetime = []
    for d in __train_data:
        __data_matrix.append(d.split('\t'))

    def start_date(self):
        """
        获取数据集的最早日期
        :return:
        """
        return str_to_date(self.__data_matrix[0][2].split(' ')[0])

    def flavor_name(self):
        """
        获取数据集中出现的flavor名称
        :return:
        """
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
                    self.__flavor_name.append(fnt)
        return self.__flavor_name

    def flavor_name_datetime(self, flavor_name):
        """
        获取各flavor对应的所有时间点
        :param flavor_name:
        :return:
        """
        for fn in flavor_name:
            fnd_item = []
            for dm in self.__data_matrix:
                if dm[1] == fn:
                    fnd_item.append(dm[2])
            self.__flavor_name_datetime.append(fnd_item)
        return self.__flavor_name_datetime
