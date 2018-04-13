# coding=utf-8


def package01(w, v, bagsize):
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
    i = len(w)-1
    while i>0:
        if matrix[i][bs] == matrix[i - 1][bs]:
            no_used.append(i)
        if matrix[i][bs] == matrix[i - 1][bs - w[i]] + v[i]:
            used.append(i)
            bs = bs - w[i]
        i = i-1
    print bs

    print "used:", used
    print "no_used:", no_used

    return matrix


def get_answer(bag_items, bag_size):
    bag_matrix = [[0 for i in range(bag_size)] for j in range(len(bag_items))]

    for i in range(bag_size):
        for j in range(len(bag_items)):
            item = bag_items[j]
            if item.weight > i:
                if j == 0:
                    bag_matrix[j][i] = 0
                else:
                    bag_matrix[j][i] = bag_matrix[j - 1][i]
            else:
                if j == 0:
                    bag_matrix[j][i] = item.value
                    continue
                else:
                    item_in_bag = bag_matrix[j - 1][i - item.weight] + item.value
                if bag_matrix[j - 1][i] > item_in_bag:
                    bag_matrix[j][i] = bag_matrix[j - 1][i]
                else:
                    bag_matrix[j][i] = item_in_bag

    answers = []
    cur_size = bag_size
    for i in range(len(bag_items[::-1])):
        item = bag_items[i]
        if cur_size == 0:
            break
        if i == 0 and cur_size > 0:
            answers.append(item.name)
            break
        if bag_matrix[i][cur_size] - bag_matrix[i - 1][cur_size - item.weight] == item.value:
            answers.append(item.name)
            cur_size = cur_size - item.weight

    return answers


class PackageItem:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


if __name__ == "__main__":
    name = ['a', 'b', 'c', 'd', 'e']
    # weight = [2, 2, 6, 5, 4]
    # value = [6, 3, 5, 4, 6]
    weight = [3, 2, 4, 5]
    value = [4, 3, 5, 6]
    bag_items = []
    array = package01(weight, value, 8)
    # for i in range(len(name)):
    #     bag_items.append(PackageItem(name[i], weight[i], value[i]))
    # array = get_answer(bag_items, 10)
    for a in array:
        print a
