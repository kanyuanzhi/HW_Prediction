# coding=utf-8
import math
import time


def package01(w, v, n, bagsize):
    """
    01背包
    :param w:
    :param v:
    :param n:
    :param bagsize:
    :return:
    """
    matrix = [[0 for i in range(bagsize + 1)] for j in range(len(w))]
    for i in range(len(matrix[0])):
        if i < w[0]:
            matrix[0][i] = 0
        else:
            matrix[0][i] = v[0]
    for i in range(1, len(matrix)):  # 第i件物品
        for j in range(len(matrix[0])):  # j背包大小
            ww = w[i]
            if j < w[i]:
                matrix[i][j] = matrix[i - 1][j]
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - w[i]] + v[i])

    no_used = []
    used = []
    bs = bagsize
    i = len(w) - 1
    while i > 0:
        # if matrix[i][bs] == matrix[i - 1][bs]:
        #     no_used.append(n[i])
        if matrix[i][bs] == matrix[i - 1][bs - w[i]] + v[i]:
            used.append(n[i])
            bs = bs - w[i]
        i = i - 1
    if bs != 0:
        used.append(n[i])
    # else:
    #     no_used.append(n[i])

    print "used:", used
    # print "no_used:", no_used

    return matrix


def package_complete(w, v, n, bagsize):
    """
    完全背包
    :param w:
    :param v:
    :param n:
    :param bagsize:
    :return:
    """
    counts = []
    new_counts = []
    for item in w:
        counts.append(bagsize / item)
        new_counts.append(math.log(bagsize / item, 2))
    print "counts:", counts
    print "new_counts:", new_counts
    w_new = []
    v_new = []
    n_new = []
    for i in range(len(w)):
        w_new = w_new + [w[i]] * counts[i]
        v_new = v_new + [v[i]] * counts[i]
        n_new = n_new + [n[i]] * counts[i]

    return package01(w_new, v_new, n_new, bagsize)


def package_multiple(w, v, n, c, bagsize):
    """
    多重背包
    :param w:
    :param v:
    :param n:
    :param c:
    :param bagsize:
    :return:
    """
    w_new = []
    v_new = []
    n_new = []
    for i in range(len(w)):
        w_new = w_new + [w[i]] * c[i]
        v_new = v_new + [v[i]] * c[i]
        n_new = n_new + [n[i]] * c[i]

    return package01(w_new, v_new, n_new, bagsize)


def two_package01(w1, w2, v, n, bagsize1, bagsize2):
    num = len(w1)  # 物品数量
    matrix = [[[0 for i in range(bagsize2 + 1)] for j in range(bagsize1 + 1)] for k in range(num)]
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0][0])):
            if i < w1[0] or j < w2[0]:
                matrix[0][i][j] = 0
            else:
                matrix[0][i][j] = v[0]

    for k in range(1, len(matrix)):  # c第k件物品
        for i in range(len(matrix[0])):
            for j in range(len(matrix[0][0])):
                if i < w1[k] or j < w2[k]:
                    matrix[k][i][j] = matrix[k - 1][i][j]
                else:
                    matrix[k][i][j] = max(matrix[k - 1][i][j], matrix[k - 1][i - w1[k]][j - w2[k]] + v[k])

    used = []
    bs1 = bagsize1
    bs2 = bagsize2
    i = num - 1
    while i > 0:
        # if matrix[i][bs] == matrix[i - 1][bs]:
        #     no_used.append(n[i])
        if matrix[i][bs1][bs2] == matrix[i - 1][bs1 - w1[i]][bs2 - w2[i]] + v[i]:
            used.append(n[i])
            bs1 = bs1 - w1[i]
            bs2 = bs2 - w2[i]
        i = i - 1
    if bs1 != 0 and bs2 != 0:
        used.append(n[i])
    # print "used:", used
    print "highest value:", matrix[num - 1][bagsize1][bagsize2]
    return [used, matrix[num - 1][bagsize1][bagsize2]]


def two_package_multiple(w1, w2, v, n, bagsize1, bagsize2, c):
    w1_new = []
    w2_new = []
    v_new = []
    n_new = []
    for i in range(len(w1)):
        w1_new = w1_new + [w1[i]] * c[i]
        w2_new = w2_new + [w2[i]] * c[i]
        v_new = v_new + [v[i]] * c[i]
        n_new = n_new + [n[i]] * c[i]
    return two_package01(w1_new, w2_new, v_new, n_new, bagsize1, bagsize2)


class PackageItem:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


def placement_algorithm_DP(flavor_queue, physical_server_CPU, physical_server_MEM, CPU_dict, MEM_dict, resource,
                           flavor_name_test, flavor_prediction_numbers_test):
    flavor_prediction_numbers_temp = flavor_prediction_numbers_test[:]
    flavor_information = []
    for i in range(len(flavor_name_test)):
        item = {'name': flavor_name_test[i], 'numbers': flavor_prediction_numbers_test[i],
                'cpu': CPU_dict[flavor_name_test[i]], 'mem': MEM_dict[flavor_name_test[i]]}
        flavor_information.append(item)
    flavor_queue = []
    for i, fn in enumerate(flavor_prediction_numbers_test):
        current_flavor_name = flavor_name_test[i]
        flavor_queue = flavor_queue + [current_flavor_name] * fn
    name = flavor_queue[:]
    bagsize1 = physical_server_CPU
    bagsize2 = physical_server_MEM
    weight1 = []
    weight2 = []
    for fq in name:
        weight1.append(CPU_dict[fq])
        weight2.append(MEM_dict[fq])
    if resource == "CPU":
        value = weight1[:]
    else:
        value = weight2[:]

    result = []
    highest_value = []
    while len(name) != 0:
        time_start = time.clock()
        flavors = two_package01(weight1, weight2, value, name, bagsize1, bagsize2)
        print time.clock() - time_start
        result.append(flavors[0])
        highest_value.append(flavors[1])

        flavor_numbers = {}
        for flavor in flavors[0]:
            if flavor in flavor_numbers:
                flavor_numbers[flavor] = flavor_numbers[flavor] + 1
            else:
                flavor_numbers[flavor] = 1

        for key in flavor_numbers:
            i = flavor_name_test.index(key)
            flavor_prediction_numbers_temp[i] = flavor_prediction_numbers_temp[i] - flavor_numbers[key]
        flag = True
        while flag:
            for key in flavor_numbers:
                i = flavor_name_test.index(key)
                if flavor_prediction_numbers_temp[i] < flavor_numbers[key]:
                    flag = False
                    break
            if not flag:
                break
            for key in flavor_numbers:
                i = flavor_name_test.index(key)
                flavor_prediction_numbers_temp[i] = flavor_prediction_numbers_temp[i] - flavor_numbers[key]
            result.append(flavors[0])
            highest_value.append(flavors[1])

        name = []
        for i, fn in enumerate(flavor_prediction_numbers_temp):
            current_flavor_name = flavor_name_test[i]
            name = name + [current_flavor_name] * fn
        weight1 = []
        weight2 = []
        for fq in name:
            weight1.append(CPU_dict[fq])
            weight2.append(MEM_dict[fq])
        if resource == "CPU":
            value = weight1[:]
        else:
            value = weight2[:]
        print len(name)
    print len(result)
    print highest_value


if __name__ == "__main__":
    name = ['a', 'b', 'c', 'd', 'e']
    weight = [2, 2, 6, 5, 4]
    # value = [6, 3, 5, 4, 6]
    # weight = [4, 2, 3, 5, 5, 7, 6]
    # value = [5, 3, 4, 6, 6, 4, 3]
    bag_items = []
    # array = package01(weight, value, name, 10)
    # for a in array:
    #     print a
    weight1 = [2, 2, 6, 5, 4]
    weight2 = [1, 1, 4, 6, 4]
    value = [1, 1, 4, 6, 4]
    count = [3, 5, 6, 8, 2]
    # array2 = two_package01(weight1, weight2, value, name, 20, 30)
    array2 = two_package_multiple(weight1, weight2, value, name, 20, 30, count)
    print array2
    # for a in array2:
    #     print a
