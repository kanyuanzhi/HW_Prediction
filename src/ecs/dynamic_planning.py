# coding=utf-8
import math


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

def two_package01(w1,w2,v,n,bagsize):
    pass

class PackageItem:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


if __name__ == "__main__":
    name = ['a', 'b', 'c', 'd', 'e']
    weight = [2, 2, 6, 5, 4]
    value = [6, 3, 5, 4, 6]
    # weight = [4, 2, 3, 5, 5, 7, 6]
    # value = [5, 3, 4, 6, 6, 4, 3]
    bag_items = []
    # array = package01(weight, value, name, 10)
    # for a in array:
    #     print a
    array2 = package_complete(weight, value, name, 10)
    for a in array2:
        print a
