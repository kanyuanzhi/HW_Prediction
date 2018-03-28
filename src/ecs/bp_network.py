# coding=utf-8
import random
import math


def __tansig(x):  # 双曲正切S型函数
    try:
        result = (1 - math.exp(-x)) / (1 + math.exp(-x))
    except OverflowError:
        result = -1
    return result


def __dtansig(x):  # 双曲正切S型函数的导数
    result = 2 / (math.exp(x) + math.exp(-x) + 2)
    return result


def __matrix_tansig(A):
    A_rows = len(A)
    A_cols = len(A[0])
    B = [[0 for j in range(A_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(A_cols):
            B[i][j] = __tansig(A[i][j])
    return B


def __matrix_dtansig(A):
    A_rows = len(A)
    A_cols = len(A[0])
    B = [[0 for j in range(A_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(A_cols):
            B[i][j] = __tansig(A[i][j])
    return B


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


def __mat(a, n):
    """
    把m*1矩阵扩展成m*n矩阵，每行值相同
    :param b:
    :param n:
    :return:
    """
    b = [[0 for i in range(n)] for j in range(len(a))]
    for i in range(len(b)):
        for j in range(len(b[0])):
            b[i][j] = a[i][0]
    return b


def __matrix_add(A, B):
    """
    矩阵加法
    :param A:
    :param B:
    :return:
    """
    A_rows = len(A)
    A_cols = len(A[0])
    B_rows = len(B)
    B_cols = len(B[0])
    if A_rows != B_rows and A_cols != B_cols:
        print "矩阵无法相加！"
        return
    C = [[0 for j in range(A_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(A_cols):
            C[i][j] = A[i][j] + B[i][j]
    return C


def __matrix_arithmetic_multiply(A, B):
    """
    矩阵对应位相乘
    :param A:
    :param B:
    :return:
    """
    A_rows = len(A)
    A_cols = len(A[0])
    B_rows = len(B)
    B_cols = len(B[0])
    if A_rows != B_rows and A_cols != B_cols:
        print "矩阵无法相对应位相乘"
        return
    C = [[0 for j in range(A_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(A_cols):
            C[i][j] = A[i][j] * B[i][j]
    return C


def __matrix_multiply_constant(A, con):
    A_rows = len(A)
    A_cols = len(A[0])
    B = [[0 for j in range(A_cols)] for i in range(A_rows)]
    for i in range(A_rows):
        for j in range(A_cols):
            B[i][j] = A[i][j] * con
    return B


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


def bp_network(prediction_numbers, related_numbers, flavor_name):
    """
    a1 = __tansig(w1 * p + b1)
    a2 = w2 * a1 + b2
    :param prediction_numbers:
    :param related_numbers:
    :return:
    """

    s = related_numbers
    p_test = []  # 用以计算预测结果的矩阵
    # for pn in prediction_numbers[-related_numbers:]:
    #     p_test.append([pn])

    t = []  # 切分后的输出实际值
    for pn in prediction_numbers[related_numbers:]:
        t.append(float(pn))
    t = [t]
    # print t

    p = [[] for i in range(related_numbers)]  # 切分后的输入数组
    for i in range(0, len(prediction_numbers) - related_numbers + 1):
        for j in range(related_numbers):
            p[j].append(float(prediction_numbers[i + j]))

    new_p = []
    for row in p:
        new_row = __normalized(row)
        new_p.append(new_row)

    for i in range(len(new_p)):
        p_test.append([new_p[i].pop()])

    p = new_p
    # print p

    # for i in range(related_numbers):
    #     print p[i]
    #
    print "len(p):", len(p)
    print "len(p[0]):", len(p[0])

    w1 = [[random.randint(-10000, 10000) / 10000.0 for i in range(s)] for j in range(related_numbers)]
    b1 = [[random.randint(-10000, 10000) / 10000.0] for j in range(s)]
    b1_matrix = __mat(b1, len(p[0]))
    w2 = [[random.randint(-10000, 10000) / 10000.0] for i in range(s)]
    b2 = [[random.randint(-10000, 10000) / 10000.0]]
    b2_matrix = __mat(b2, len(p[0]))
    eta = 0.017  # 学习速率
    max_epoch = 1000000
    error_goal = 0.01

    # print "w1:", w1
    # print __transpose(w1)
    # print "b1_matrix:", b1_matrix
    # print "b1:", b1
    # print "w2:", w2
    # print "b2_matrix:", b2_matrix

    a1_origin = __matrix_add(__dot(__transpose(w1), p), b1_matrix)
    # print "a1_origin:", a1_origin
    a1 = __matrix_tansig(a1_origin)
    # print "a1:", a1

    a2 = __matrix_add(__dot(__transpose(w2), a1), b2_matrix)

    # print "a2", a2

    e = [[t[0][i] - a2[0][i] for i in range(len(t[0]))]]
    # print "e:", e
    sse = sum([i ** 2 for i in e[0]]) / 2
    SSETemp = sse
    for epoch in range(max_epoch):
        print flavor_name,"_sse:", sse
        if sse < error_goal:
            break
        # if (sse < SSETemp):
        #     eta = 1.05 * eta
        # elif (sse > SSETemp):
        #     eta = 0.8 * eta
        # else:
        #     eta = eta
        # print eta
        SSETemp = sse
        dw2 = __matrix_multiply_constant(__dot(a1, __transpose(e)), eta)
        # print "dw2:", dw2
        db2 = __matrix_multiply_constant(__transpose(e), eta)
        # print "db2:", db2

        w2 = __matrix_add(w2, dw2)
        b2 = [[b2[0][0] + sum(__transpose(db2)[0])]]
        b2_matrix = __mat(b2, len(p[0]))

        # print "w2:", w2

        a1_d = __matrix_dtansig(a1_origin)

        e0 = __dot(w2, e)
        delta = __matrix_arithmetic_multiply(e0, a1_d)
        dw1 = __matrix_multiply_constant(__dot(p, __transpose(delta)), eta)
        w1 = __matrix_add(w1, dw1)

        db1_delta = []
        for d in delta:
            db1_delta.append([sum(d)])
        db1 = __matrix_multiply_constant(db1_delta, eta)

        b1 = __matrix_add(b1, db1)
        b1_matrix = __mat(b1, len(p[0]))

        a1_origin = __matrix_add(__dot(__transpose(w1), p), b1_matrix)
        a1 = __matrix_tansig(a1_origin)
        # print "a1:", a1
        a2 = __matrix_add(__dot(__transpose(w2), a1), b2_matrix)
        # print "a2", a2
        e = [[t[0][i] - a2[0][i] for i in range(len(t[0]))]]
        # print "e:", e
        sse = sum([i ** 2 for i in e[0]]) / 2
        # for i in range(len(a1)):
        #     print a1[i]

        # print "delta rows:", len(delta)
        # print "delta cols:", len(delta[0])
    a1_origin = __matrix_add(__dot(__transpose(w1), p), b1_matrix)
    a1 = __matrix_tansig(a1_origin)
    a2 = __matrix_add(__dot(__transpose(w2), a1), b2_matrix)
    # print "a2:", a2
    # print "t", t

    num = int(round(
        __matrix_add(__dot(__transpose(w2), __matrix_tansig(__matrix_add(__dot(__transpose(w1), p_test), b1_matrix))),
                     b2_matrix)[0][0]))
    if num < 0:
        num = 0
    # print "num:", num
    return num