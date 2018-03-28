# coding=utf-8
import random
import math


def __dot(A, B):
    """
    计算矩阵乘法
    :param A:
    :param B:
    :return:
    """
    A_rows = len(A)
    A_cols = len(A[0])
    B_rows = len(B)
    B_cols = len(B[0])
    if A_cols != B_rows:
        print "矩阵无法相乘！"
        return
    C = [[0 for j in range(B_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(B_cols):
            for k in range(B_rows):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C


def __transpose(A):
    A_rows = len(A)
    A_cols = len(A[0])
    B = [[0 for j in range(A_rows)] for i in range(A_cols)]
    for i in range(A_cols):
        for j in range(A_rows):
            B[i][j] = A[j][i]
    return B


def __normalized(array):
    max_a = max(array)
    if max_a != 0:
        new_array = [a / max_a for a in array]
    return new_array


def adaline(prediction_numbers, related_numbers):
    """
    a1 = __tansig(w1 * p + b1)
    a2 = w2 * a1 + b2
    :param prediction_numbers:
    :param related_numbers:
    :return:
    """
    s = len(prediction_numbers)
    p_test = []  # 用以计算预测结果的矩阵
    # for pn in prediction_numbers[-related_numbers:]:
    #     p_test.append([pn])

    t = []  # 切分后的输出实际值
    for pn in prediction_numbers[related_numbers:]:
        t.append(float(pn))

    p = [[] for i in range(related_numbers)]  # 切分后的输入数组
    for i in range(0, len(prediction_numbers) - related_numbers + 1):
        for j in range(related_numbers):
            p[j].append(float(prediction_numbers[i + j]))

    # for i in range(related_numbers):
    #     print p[i]

    new_p = []
    for row in p:
        new_row = __normalized(row)
        new_p.append(new_row)

    for i in range(len(new_p)):
        p_test.append([new_p[i].pop()])

    p = new_p

    w1 = [[random.randint(-10000, 10000) / 10000.0 for i in range(related_numbers)]]
    b1 = random.randint(-10000, 10000) / 10000.0
    eta = 0.02  # 学习速率
    max_epoch = 100000
    error_goal = 0.01

    # print "w1:", w1
    # print __dot(w1, p)
    # print "b1:", b1

    a = [i + b1 for i in __dot(w1, p)[0]]
    e = [t[i] - a[i] for i in range(len(t))]
    sse = sum([i ** 2 for i in e]) / 2
    # print "a:", a
    # print "e:", e
    # print "sse:", sse
    SSETemp = sse
    for epoch in range(max_epoch):
        # print "sse:", epoch, sse
        if sse <= error_goal:
            break
        # if (sse < SSETemp):
        #     eta = 1.05 * eta
        # elif (sse > SSETemp):
        #     eta = 0.8 * eta
        # else:
        #     eta = eta
        # print eta
        # SSETemp = sse
        e_multiply_p = __dot([e], __transpose(p))
        dw1 = [[ep * eta for ep in e_multiply_p[0]]]
        # print "dw1:", dw1

        db1 = sum(e_multiply_p[0]) * eta
        # print "db1:", db1

        w1 = [[w1[0][i] + dw1[0][i] for i in range(len(w1[0]))]]
        b1 = b1 + db1
        a = [i + b1 for i in __dot(w1, p)[0]]
        e = [t[i] - a[i] for i in range(len(t))]
        sse = sum([i ** 2 for i in e]) / 2

    w1_multiply_p_test = __dot(w1, p_test)
    num = int(1.1*round(w1_multiply_p_test[0][0] + b1))
    if num < 0:
        num = 0
    a = [i + b1 for i in __dot(w1, p)[0]]
    print "a:", a
    print "t", t
    # # print "p_test:", p_test
    # # print "w1:", w1
    # print "b1:", b1
    # print "w1_multiply_p_test:", w1_multiply_p_test

    return num
