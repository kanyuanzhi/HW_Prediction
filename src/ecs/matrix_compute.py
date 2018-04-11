# coding=utf-8
import random
import math


def dot(A, B):
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


def mat(a, n):
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


def matrix_add(A, B):
    """
    矩阵加法B可以是矩阵或一个常数,对应位相加
    :param A:
    :param B:
    :return:
    """
    if isinstance(A, list):
        A_rows = len(A)
        A_cols = len(A[0])
        if isinstance(B, list):
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
        else:
            C = [[B for j in range(A_cols)] for i in range(A_rows)]
            return matrix_add(A, C)
    else:
        return A + B


def matrix_arithmetic_multiply(A, B):
    """
    矩阵对应位相乘，B可为一个常数
    :param A:
    :param B:
    :return:
    """
    if isinstance(A, list):
        A_rows = len(A)
        A_cols = len(A[0])
        if isinstance(B, list):
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
        else:
            C = [[B for j in range(A_cols)] for i in range(A_rows)]
            return matrix_arithmetic_multiply(A, C)
    else:
        return A * B


# def __matrix_arithmetic_multiply(A, con):
#     """
#     矩阵每位乘一个常数
#     :param A:
#     :param con:
#     :return:
#     """
#     A_rows = len(A)
#     A_cols = len(A[0])
#     B = [[0 for j in range(A_cols)] for i in range(A_rows)]
#     for i in range(A_rows):
#         for j in range(A_cols):
#             B[i][j] = A[i][j] * con
#     return B


def transpose(A):
    A_rows = len(A)
    A_cols = len(A[0])
    B = [[0 for j in range(A_rows)] for i in range(A_cols)]
    for i in range(A_cols):
        for j in range(A_rows):
            B[i][j] = A[j][i]
    return B


def normalized(array):
    average = sum(array) / float(len(array))
    s = 0
    for a in array:
        s = s + pow(a - average, 2)
    standard_deviation = pow(s, 0.5)
    new_array = []
    for a in array:
        new_array.append((a - average) / standard_deviation)
    return new_array
